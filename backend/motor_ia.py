import cv2
import numpy as np
import base64
import urllib.request
import csv
import codecs
import pytesseract
import re
import os
import time
from datetime import datetime, timezone

# RUTA DE TESSERACT (Mantené la tuya)
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD", "tesseract")

PRECIOS_CACHE_SEGUNDOS = int(os.getenv("PRECIOS_CACHE_SEGUNDOS", "300"))
SHEETS_TIMEOUT_SEC = int(os.getenv("SHEETS_TIMEOUT_SEC", "12"))

_precios_cache = None
_precios_cache_ts = 0.0
LAST_PRECIO_META = {
    "actualizado_en": None,
    "fuente": "offline",
    "desde_cache": False,
}


def _precios_base_offline():
    return {
        "mat_cemento_25kg": 8000,
        "mat_cal_25kg": 5500,
        "mat_arena_m3": 15000,
        "mat_escombro_m3": 8500,
        "mat_ladrillo_hueco_18cm": 1600,
        "mat_ladrillo_hueco_12cm": 1000,
        "mat_ladrillo_comun_12cm": 400,
        "mat_ceramico_m2": 8500,
        "mat_pegamento_30kg": 15600,
        "mat_abertura_promedio": 100000,
        "mo_muro_hueco_m2": 12000,
        "mo_muro_comun_m2": 13000,
        "mo_revoque_doble_m2": 20000,
        "mo_contrapiso_m2": 13000,
        "mo_carpeta_m2": 12000,
        "mo_ceramico_m2": 15000,
        "mo_abertura_unid": 70000,
        "AGUA-MAT-01": 1298,
        "AGUA-ACC-CODO": 258,
        "AGUA-ACC-TE": 793,
        "AGUA-MO-01": 38000,
        "AGUA-BOCA-01": 50000,
        "CLOA-MAT-01": 6070,
        "CLOA-MO-01": 32000,
        "LUZ-MAT-01": 1200,
        "LUZ-MO-01": 38000,
        "LUZ-MAT-02": 5000,
        "LUZ-MO-02": 49000,
        "TECH-CHAP-01": 22000,
        "TECH-PERF-01": 21000,
        "TECH-AISL-01": 12000,
        "TECH-TORN-01": 1100,
        "TECH-MO-01": 30000,
    }


def get_precios_info():
    """Estado de la ultima lectura de precios (para UI /health)."""
    global LAST_PRECIO_META, _precios_cache_ts
    meta = {**LAST_PRECIO_META}
    if _precios_cache_ts:
        meta["cache_edad_segundos"] = int(max(0, time.time() - _precios_cache_ts))
    return meta


def obtener_precios_en_vivo():
    global _precios_cache, _precios_cache_ts, LAST_PRECIO_META
    now = time.time()
    if _precios_cache is not None and (now - _precios_cache_ts) < PRECIOS_CACHE_SEGUNDOS:
        LAST_PRECIO_META = {**LAST_PRECIO_META, "desde_cache": True}
        return _precios_cache

    url_csv = os.getenv(
        "PRECIOS_CSV_URL",
        "https://docs.google.com/spreadsheets/d/1fmULPVz8YeKJT9jLyGRy6ZBOLpXz-wfgJSaF_Br5s28/export?format=csv",
    )
    P = _precios_base_offline()
    fuente = "offline"
    try:
        response = urllib.request.urlopen(url_csv, timeout=SHEETS_TIMEOUT_SEC)
        reader = csv.reader(codecs.iterdecode(response, "utf-8"))
        next(reader, None)
        for row in reader:
            if len(row) >= 4:
                try:
                    P[row[0].strip()] = float(row[3].strip().replace("$", "").replace(".", "").replace(",", ""))
                except Exception:
                    pass
        fuente = "google_sheets"
    except Exception as e:
        print(f"Error leyendo Sheets (usando precios offline): {e}")

    _precios_cache = P
    _precios_cache_ts = now
    LAST_PRECIO_META = {
        "actualizado_en": datetime.now(timezone.utc).isoformat(),
        "fuente": fuente,
        "desde_cache": False,
    }
    return P


def _li(nom, val, origen):
    return {"nom": nom, "val": val, "origen": origen}

def _primer_float_en_texto(texto: str):
    if not texto:
        return None
    numeros = re.findall(r"\d+[.,]?\d*", texto)
    if not numeros:
        return None
    try:
        return float(numeros[0].replace(",", "."))
    except ValueError:
        return None


def _ocr_float_desde_gris(prep_gray):
    """Devuelve el primer numero razonable (metros de cota) leido por Tesseract."""
    if prep_gray is None or prep_gray.size == 0:
        return None
    h, w = prep_gray.shape[:2]
    if h < 6 or w < 6:
        return None
    scale = max(1.0, 140.0 / max(h, w))
    if scale > 1.02:
        prep_gray = cv2.resize(prep_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    def leer(img_gray):
        for cfg in ("--psm 8", "--psm 7", "--psm 11", "--psm 6"):
            t = pytesseract.image_to_string(img_gray, config=cfg)
            v = _primer_float_en_texto(t)
            if v is not None and 0.05 < v < 500:
                return v
        for rot in (cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE):
            r = cv2.rotate(img_gray, rot)
            for cfg in ("--psm 8", "--psm 11", "--psm 7"):
                t = pytesseract.image_to_string(r, config=cfg)
                v = _primer_float_en_texto(t)
                if v is not None and 0.05 < v < 500:
                    return v
        return None

    return leer(prep_gray)


def extraer_numero_escala(img, mask_verde):
    contornos, _ = cv2.findContours(mask_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return None

    c = max(contornos, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    margen_x = 90
    margen_y_arriba = 55
    margen_y_abajo = 200
    y1 = max(0, y - margen_y_arriba)
    y2 = min(img.shape[0], y + h + margen_y_abajo)
    x1 = max(0, x - margen_x)
    x2 = min(img.shape[1], x + w + margen_x)
    roi = img[y1:y2, x1:x2]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    preparaciones = []

    mask_amarillo = cv2.inRange(hsv_roi, np.array([10, 55, 55]), np.array([50, 255, 255]))
    k3 = np.ones((3, 3), np.uint8)
    mask_amarillo = cv2.dilate(mask_amarillo, k3, iterations=2)
    if np.sum(mask_amarillo) > 60:
        preparaciones.append(cv2.bitwise_not(mask_amarillo))

    gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    media = float(np.mean(gris))
    base = cv2.bitwise_not(gris) if media < 115 else gris
    _, otsu = cv2.threshold(base, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, otsu_inv = cv2.threshold(base, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    preparaciones.extend([otsu, otsu_inv])

    _, b0 = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    preparaciones.extend([b0, cv2.bitwise_not(b0)])

    for prep in preparaciones:
        v = _ocr_float_desde_gris(prep)
        if v is not None:
            return v
    return None

# --- FUNCIÓN DEFINITIVA: CONVOLUCIÓN DE ESQUELETOS PARA CAÑERÍAS ---
def analizar_nodos_canerias(mask_color):
    # Reducimos la tubería a 1 solo píxel de grosor exacto
    skel = cv2.ximgproc.thinning(mask_color)
    skel_bin = (skel > 0).astype(np.uint8)
    
    # Matriz 3x3 para contar cuántos "caños" se conectan a cada píxel
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]], dtype=np.uint8)
    
    vecinos = cv2.filter2D(skel_bin, -1, kernel)
    nodos = vecinos * skel_bin # Multiplicamos para mirar solo sobre la tubería
    
    # Matemáticas de grafos:
    # 1 vecino = Punta ciega (Boca, subida o bajada)
    # 3 o 4 vecinos = Bifurcación (Tee o Cruz)
    puntas = np.sum(nodos == 1)
    tees = np.sum(nodos == 3) + (np.sum(nodos == 4) * 2) 
    
    # Para los Codos, usamos un radar de esquinas sobre el esqueleto
    corners = cv2.goodFeaturesToTrack(skel, maxCorners=500, qualityLevel=0.1, minDistance=10)
    codos = 0
    if corners is not None:
        for corner in corners:
            x, y = int(corner[0][0]), int(corner[0][1])
            # Verificamos si esa esquina NO es una T ni una Punta detectada antes
            vecindad = nodos[max(0, y-2):min(nodos.shape[0], y+3), max(0, x-2):min(nodos.shape[1], x+3)]
            if not (3 in vecindad or 4 in vecindad or 1 in vecindad):
                codos += 1
                
    return int(puntas), int(codos), int(tees)


def procesar_plano_ia(
    bytes_imagen,
    referencia_metros_manual,
    sistema_muro="ladrillo_hueco_12",
    tipo_plano="muros",
    altura_muro=2.60,
):
    nparr = np.frombuffer(bytes_imagen, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("No se pudo leer la imagen del plano.")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    try:
        altura = float(altura_muro)
    except (TypeError, ValueError) as exc:
        raise ValueError("Altura de muro invalida.") from exc
    if altura < 1.8 or altura > 6.0:
        raise ValueError("Altura de muro debe estar entre 1.8 y 6.0 metros.")

    # --- ESCALA VERDE ---
    mask_v = cv2.inRange(hsv, np.array([40, 150, 50]), np.array([80, 255, 255]))
    px_v = np.sum(cv2.ximgproc.thinning(mask_v) > 0)
    
    escala_leida = extraer_numero_escala(img, mask_v)
    metros_reales = escala_leida if escala_leida else float(referencia_metros_manual)
    escala = (metros_reales / px_v) if px_v > 0 else 0.02
    escala_m2 = escala ** 2

    P = obtener_precios_en_vivo()
    res = {"tipo": tipo_plano, "items": [], "total": 0, "imagen": "", "escala_detectada": escala_leida}
    img_audit = img.copy()

    # ==========================================
    # 🧱 MÓDULO 1: MUROS Y ESTRUCTURA
    # ==========================================
    if tipo_plano == "muros":
        mask_rojo = cv2.inRange(hsv, np.array([0, 150, 50]), np.array([10, 255, 255]))
        m2_muros = (np.sum(cv2.ximgproc.thinning(mask_rojo) > 0) * escala) * altura
        m2_revoques = m2_muros * 2 
        
        mask_cian = cv2.inRange(hsv, np.array([85, 150, 50]), np.array([105, 255, 255]))
        contornos_cian, _ = cv2.findContours(mask_cian, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        unid_aberturas = len(contornos_cian)

        mask_gris = cv2.inRange(hsv, np.array([0, 0, 180]), np.array([179, 30, 230]))
        mask_naranja = cv2.inRange(hsv, np.array([10, 150, 150]), np.array([25, 255, 255]))
        m2_pisos = (np.sum(mask_gris > 0) + np.sum(mask_naranja > 0)) * escala_m2

        precio_cem_kg = P.get('mat_cemento_25kg', 0) / 25
        precio_cal_kg = P.get('mat_cal_25kg', 0) / 25
        precio_peg_kg = P.get('mat_pegamento_30kg', 0) / 30

        ladrillo_id = 'mat_ladrillo_hueco_12cm' if sistema_muro == "ladrillo_hueco_12" else 'mat_ladrillo_comun_12cm'
        cant_ladrillos = 15 if "hueco" in sistema_muro else 60

        mat_muro = (cant_ladrillos * P.get(ladrillo_id,0)) + (4 * precio_cem_kg) + (0.015 * P.get('mat_arena_m3',0))
        mat_revoque = (5 * precio_cem_kg) + (3 * precio_cal_kg) + (0.02 * P.get('mat_arena_m3',0))
        mat_contrapiso = (7.5 * precio_cem_kg) + (3.5 * precio_cal_kg) + (0.035 * P.get('mat_arena_m3',0)) + (0.07 * P.get('mat_escombro_m3',0))
        mat_carpeta = (10.5 * precio_cem_kg) + (0.03 * P.get('mat_arena_m3',0))
        mat_ceramico = (1.05 * P.get('mat_ceramico_m2',0)) + (4 * precio_peg_kg)

        mo_aberturas = unid_aberturas * P.get("mo_abertura_unid", 0)
        mat_aberturas = unid_aberturas * P.get("mat_abertura_promedio", 0)

        res["items"].append(
            _li(
                "Mano Obra: Muros",
                m2_muros * P.get("mo_muro_hueco_m2", 0),
                f"Mascara HSV rojo + thinning; m lineales x escala; x {altura:.2f} m de altura; tabla mo_muro_hueco_m2.",
            )
        )
        res["items"].append(_li("Mano Obra: Revoques", m2_revoques * P.get("mo_revoque_doble_m2", 0), "Misma superficie muro x2 (revoque doble); mo_revoque_doble_m2."))
        res["items"].append(_li("Mano Obra: Pisos", m2_pisos * (P.get("mo_contrapiso_m2", 0) + P.get("mo_carpeta_m2", 0) + P.get("mo_ceramico_m2", 0)), "Mascaras gris y naranja (pisos) en m2 reales; suma MO contrapiso+carpeta+ceramico."))
        res["items"].append(
            _li(
                "Mano Obra: Aberturas",
                mo_aberturas,
                f"Contornos cian detectados ({unid_aberturas} unid.) x mo_abertura_unid.",
            )
        )
        res["items"].append(
            _li(
                "Materiales: Muros",
                m2_muros * mat_muro,
                f"Metros lineales muro x formulas de ladrillo/cemento (sistema {sistema_muro}).",
            )
        )
        res["items"].append(_li("Materiales: Revoques", m2_revoques * mat_revoque, "Superficie revoque (2x muro) x dosificacion cemento/cal/arena."))
        res["items"].append(_li("Materiales: Pisos", m2_pisos * (mat_contrapiso + mat_carpeta + mat_ceramico), "m2 piso detectados x paquete contrapiso+carpeta+ceramico."))
        res["items"].append(
            _li(
                "Materiales: Aberturas",
                mat_aberturas,
                f"Contornos cian ({unid_aberturas} unid.) x mat_abertura_promedio.",
            )
        )

        img_audit[mask_gris > 0] = [255, 150, 200]
        if unid_aberturas:
            img_audit[mask_cian > 0] = [255, 255, 0]
        kernel = np.ones((15, 15), np.uint8)
        img_audit[cv2.bitwise_and(cv2.dilate(cv2.ximgproc.thinning(mask_rojo), kernel, iterations=1), mask_rojo) > 0] = [0, 255, 255]

    # ==========================================
    # 💧 MÓDULO 2: AGUA Y GAS (Colores Anti-Confusión)
    # ==========================================
    elif tipo_plano == "agua":
        # Agua Fría: Azul
        mask_azul = cv2.inRange(hsv, np.array([100, 100, 50]), np.array([140, 255, 255]))
        
        # Agua Caliente: Magenta / Fucsia (Totalmente separado del rojo de los muros)
        mask_magenta = cv2.inRange(hsv, np.array([140, 100, 100]), np.array([170, 255, 255]))
        
        # Cloaca: Naranja / Sepia intenso
        mask_marron = cv2.inRange(hsv, np.array([10, 150, 100]), np.array([25, 255, 255]))
        
        thin_azul = cv2.ximgproc.thinning(mask_azul)
        thin_magenta = cv2.ximgproc.thinning(mask_magenta)
        thin_marron = cv2.ximgproc.thinning(mask_marron)
        
        ml_azul = np.sum(thin_azul > 0) * escala
        ml_magenta = np.sum(thin_magenta > 0) * escala
        ml_marron = np.sum(thin_marron > 0) * escala
        
        puntas_a, codos_a, tees_a = analizar_nodos_canerias(mask_azul)
        puntas_m, codos_m, tees_m = analizar_nodos_canerias(mask_magenta)
        
        tot_codos = codos_a + codos_m
        tot_tees = tees_a + tees_m
        tot_bocas = puntas_a + puntas_m
        tot_ml_agua = ml_azul + ml_magenta

        if tot_ml_agua > 0:
            res["items"].append(_li(f"Mat: Caño Termo ({tot_ml_agua:.1f}m)", tot_ml_agua * P.get("AGUA-MAT-01", 0), "Mascaras azul+magenta, thinning; metros lineales x AGUA-MAT-01."))
            res["items"].append(_li(f"Mat: Codos ({tot_codos}u)", tot_codos * P.get("AGUA-ACC-CODO", 0), "Grafo sobre esqueleto agua fria/caliente; nodos tipo codo."))
            res["items"].append(_li(f"Mat: Tees ({tot_tees}u)", tot_tees * P.get("AGUA-ACC-TE", 0), "Grafo sobre esqueleto; bifurcaciones (tees)."))
            res["items"].append(_li(f"M.O: Tender Cañería ({tot_ml_agua:.1f}m)", tot_ml_agua * P.get("AGUA-MO-01", 0), "Metros totales agua x AGUA-MO-01."))
            res["items"].append(_li(f"M.O: Armado Bocas ({tot_bocas}u)", tot_bocas * P.get("AGUA-BOCA-01", 0), "Puntas del esqueleto (bocas) agua fria+caliente."))

        if ml_marron > 0:
            res["items"].append(_li(f"Mat: Caño Cloaca ({ml_marron:.1f}m)", ml_marron * P.get("CLOA-MAT-01", 0), "Mascara sepia/naranja cloaca + thinning x CLOA-MAT-01."))
            res["items"].append(_li(f"M.O: Inst. Cloaca ({ml_marron:.1f}m)", ml_marron * P.get("CLOA-MO-01", 0), "Metros lineales cloaca x CLOA-MO-01."))
        
        # La auditoría visual pintará Azul, Rosa Brillante y Naranja
        img_audit[mask_azul > 0] = [255, 0, 0]
        img_audit[mask_magenta > 0] = [255, 0, 255] 
        img_audit[mask_marron > 0] = [0, 100, 255]

    # ==========================================
    # ⚡ MÓDULO 3: ELECTRICIDAD (Apertura Morfológica)
    # ==========================================
    elif tipo_plano == "luz":
        mask_amarilla = cv2.inRange(hsv, np.array([15, 80, 50]), np.array([45, 255, 255]))
        
        # 1. Separamos las Bocas (Círculos gruesos) de los Caños (Líneas finas)
        # Un kernel de 5x5 borra las líneas y deja vivos los objetos gordos
        kernel_bocas = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask_solo_bocas = cv2.morphologyEx(mask_amarilla, cv2.MORPH_OPEN, kernel_bocas)
        
        # 2. Contamos las Bocas aisladas
        conts_bocas, _ = cv2.findContours(mask_solo_bocas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cant_bocas = 0
        for c in conts_bocas:
            if cv2.contourArea(c) > 10:  # Filtramos mini-píxeles basura
                cant_bocas += 1
                cv2.drawContours(img_audit, [c], -1, (0, 0, 255), 4) # Auditar bocas en rojo
                
        # 3. Calculamos los Metros de caño 
        # Usamos thinning para medir la longitud exacta por el eje central
        ml_corrugado = np.sum(cv2.ximgproc.thinning(mask_amarilla) > 0) * escala
        
        if ml_corrugado > 0:
            res["items"].append(_li(f"Mat: Caño Corrugado ({ml_corrugado:.1f}m)", ml_corrugado * P.get("LUZ-MAT-01", 0), "Mascara amarilla electrica + thinning x LUZ-MAT-01."))
            res["items"].append(_li(f"M.O: Tendido Eléctrico ({ml_corrugado:.1f}m)", ml_corrugado * P.get("LUZ-MO-01", 0), "Metros lineales tendido x LUZ-MO-01."))
        if cant_bocas > 0:
            res["items"].append(_li(f"Mat: Cajas y Llaves ({cant_bocas}u)", cant_bocas * P.get("LUZ-MAT-02", 0), "Apertura morfologica sobre amarillo; contornos gruesos (cajas)."))
            res["items"].append(_li(f"M.O: Armado Bocas ({cant_bocas}u)", cant_bocas * P.get("LUZ-MO-02", 0), "Mismo conteo de cajas x LUZ-MO-02."))

    # ==========================================
    # 🏠 MÓDULO 4: TECHOS (Color Violeta Flúor)
    # ==========================================
    elif tipo_plano == "techo":
        # Buscamos áreas Violetas o Rosas fucsia marcadas en el plano
        mask_violeta = cv2.inRange(hsv, np.array([125, 100, 100]), np.array([160, 255, 255]))
        
        # Calcular superficie pintada en m2
        m2_techo = np.sum(mask_violeta > 0) * escala_m2
        
        if m2_techo > 0:
            # Desglose matemático inteligente
            ml_perfil = m2_techo * 2.5 # 2.5 metros de perfil C por cada m2
            unid_tornillos = m2_techo * 5 # 5 tornillos por cada m2
            
            res["items"].append(_li(f"Mat: Chapa Cincalum ({m2_techo:.1f}m2)", m2_techo * P.get("TECH-CHAP-01", 0), "Mascara violeta techo en m2 reales x TECH-CHAP-01."))
            res["items"].append(_li(f"Mat: Aislante ({m2_techo:.1f}m2)", m2_techo * P.get("TECH-AISL-01", 0), "m2 techo x TECH-AISL-01."))
            res["items"].append(_li(f"Mat: Perfilería C ({ml_perfil:.1f}m)", ml_perfil * P.get("TECH-PERF-01", 0), "2,5 m lineales de perfil C por m2 de techo."))
            res["items"].append(_li(f"Mat: Tornillos autoperf. ({unid_tornillos:.0f}u)", unid_tornillos * P.get("TECH-TORN-01", 0), "5 unidades tornillo por m2 de techo."))
            res["items"].append(_li(f"M.O: Armado de Techo ({m2_techo:.1f}m2)", m2_techo * P.get("TECH-MO-01", 0), "m2 techo x TECH-MO-01."))
            
            # Auditoría visual: pinta el techo detectado de un semitransparente naranja
            img_audit[mask_violeta > 0] = [0, 150, 255]

    # ==========================================
    # 🌲 MÓDULO 5: TERRENOS E INMOBILIARIAS (Multi-Lote)
    # ==========================================
    elif tipo_plano == "terreno":
        # Usamos Gris Oscuro
        mask_lote = cv2.inRange(hsv, np.array([0, 0, 40]), np.array([179, 50, 150]))
        conts, _ = cv2.findContours(mask_lote, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if conts:
            # Filtramos basuritas (ruido del plano) y ordenamos los lotes de izquierda a derecha
            lotes_validos = [c for c in conts if cv2.contourArea(c) > 500]
            # Ordenar por la coordenada X (para que el Lote 1 sea el de la izquierda)
            lotes_validos = sorted(lotes_validos, key=lambda c: cv2.boundingRect(c)[0])
            
            for idx, c_terreno in enumerate(lotes_validos):
                numero_lote = idx + 1
                
                # Área y Perímetro
                area_m2 = cv2.contourArea(c_terreno) * escala_m2
                perimetro_m = cv2.arcLength(c_terreno, True) * escala
                
                res["items"].append(_li(f"🟩 LOTE {numero_lote} - Área", f"{area_m2:.2f} m²", "Contorno gris oscuro; area en px x escala_m2."))
                res["items"].append(_li(f"📏 LOTE {numero_lote} - Perímetro", f"{perimetro_m:.2f} m", "Perimetro del contorno x escala lineal."))
                
                # Lados
                epsilon = 0.02 * cv2.arcLength(c_terreno, True)
                vertices = cv2.approxPolyDP(c_terreno, epsilon, True)
                
                if len(vertices) >= 3:
                    for i in range(len(vertices)):
                        pt1 = vertices[i][0]
                        pt2 = vertices[(i + 1) % len(vertices)][0]
                        dist_m = np.linalg.norm(pt1 - pt2) * escala
                        res["items"].append(_li(f"   ↳ Lado {i+1}", f"{dist_m:.2f} m", "approxPolyDP sobre contorno del lote; lado i."))
                
                # Auditoría: Pinta SOLO el lote actual, bordes y vértices
                cv2.drawContours(img_audit, [c_terreno], -1, (255, 150, 0), -1) # Relleno Azul
                cv2.drawContours(img_audit, [c_terreno], -1, (255, 255, 255), 3) # Borde blanco
                for v in vertices:
                    cv2.circle(img_audit, (v[0][0], v[0][1]), 8, (0, 0, 255), -1)
                
                # Dibujar el número de lote en la imagen para identificarlo
                M = cv2.moments(c_terreno)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.putText(img_audit, str(numero_lote), (cx-10, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
                    
    # --- RENDER FINAL Y CÁLCULO DE TOTALES ---
    if px_v > 0:
        kernel = np.ones((15,15), np.uint8)
        img_audit[cv2.bitwise_and(cv2.dilate(cv2.ximgproc.thinning(mask_v), kernel, iterations=1), mask_v) > 0] = [0, 255, 0]
    
    _, buf = cv2.imencode('.png', img_audit)
    res["imagen"] = base64.b64encode(buf).decode('utf-8')

    avisos = []
    if px_v == 0:
        avisos.append("No se detecto traza verde de escala; se aplico escala por defecto en pixels (revisa linea verde).")
    if escala_leida is None:
        avisos.append("OCR no leyo un numero junto al verde; se uso la escala manual del formulario.")
    if LAST_PRECIO_META.get("fuente") == "offline":
        avisos.append("Precios en modo local (no se pudo actualizar desde el CSV publico en la ultima lectura).")

    res["avisos"] = avisos
    res["escala_modo"] = "ocr" if escala_leida is not None else ("manual" if px_v > 0 else "sin_linea")
    res["metros_referencia_usados"] = float(metros_reales)
    res["altura_muro"] = float(altura)
    res["sistema_muro"] = sistema_muro
    res["precios_info"] = get_precios_info()

    # FIX DEL BUG 500: Solo suma plata si NO es un terreno
    if tipo_plano != "terreno":
        res["total"] = sum(float(i["val"]) for i in res["items"] if isinstance(i.get("val"), (int, float)))
    else:
        res["total"] = 0

    return res
