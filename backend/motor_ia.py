import cv2
import numpy as np
import base64
import urllib.request
import csv
import codecs
import pytesseract
import re
import os

# RUTA DE TESSERACT (Mantené la tuya)
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD", "tesseract")

def obtener_precios_en_vivo():
    # Asegurate de que esta URL sea la correcta y esté publicada como CSV
    url_csv = "https://docs.google.com/spreadsheets/d/1fmULPVz8YeKJT9jLyGRy6ZBOLpXz-wfgJSaF_Br5s28/export?format=csv"
    
    # DICCIONARIO BASE ACTUALIZADO (Por si falla internet, usa estos)
    P = {
        # Base Muros y Pisos
        'mat_cemento_25kg': 8000, 'mat_cal_25kg': 5500, 'mat_arena_m3': 15000, 
        'mat_escombro_m3': 8500, 'mat_ladrillo_hueco_18cm': 1600, 'mat_ladrillo_hueco_12cm': 1000,
        'mat_ladrillo_comun_12cm': 400, 'mat_ceramico_m2': 8500, 'mat_pegamento_30kg': 15600, 
        'mat_abertura_promedio': 100000, 'mo_muro_hueco_m2': 12000, 'mo_muro_comun_m2': 13000, 
        'mo_revoque_doble_m2': 20000, 'mo_contrapiso_m2': 13000, 'mo_carpeta_m2': 12000, 
        'mo_ceramico_m2': 15000, 'mo_abertura_unid': 70000,
        
        # NUEVOS IDs - AGUA
        'AGUA-MAT-01': 1298, 'AGUA-ACC-CODO': 258, 'AGUA-ACC-TE': 793, 
        'AGUA-MO-01': 38000, 'AGUA-BOCA-01': 50000,
        'CLOA-MAT-01': 6070, 'CLOA-MO-01': 32000,
        
        # NUEVOS IDs - LUZ
        'LUZ-MAT-01': 1200, 'LUZ-MO-01': 38000, 
        'LUZ-MAT-02': 5000, 'LUZ-MO-02': 49000,
        
        # NUEVOS IDs - TECHOS
        'TECH-CHAP-01': 22000, 'TECH-PERF-01': 21000, 'TECH-AISL-01': 12000, 
        'TECH-TORN-01': 1100, 'TECH-MO-01': 30000
    }
    
    try:
        response = urllib.request.urlopen(url_csv)
        reader = csv.reader(codecs.iterdecode(response, 'utf-8'))
        next(reader, None) # Saltar cabecera
        for row in reader:
            if len(row) >= 4: # Ahora verificamos ID y PRECIO en la col 4
                try: 
                    # El ID está en la col 0, el precio en la col 3 (índice 3 en python)
                    P[row[0].strip()] = float(row[3].strip().replace('$', '').replace('.', '').replace(',', ''))
                except: pass
    except Exception as e: 
        print(f"Error leyendo Sheets (usando precios offline): {e}")
    return P

def extraer_numero_escala(img, mask_verde):
    # (El código de OCR queda igual, está perfecto)
    contornos, _ = cv2.findContours(mask_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos: return None
    
    c = max(contornos, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    
    margen = 40
    y1, y2 = max(0, y - margen), min(img.shape[0], y + h + margen)
    x1, x2 = max(0, x - margen), min(img.shape[1], x + w + margen)
    roi = img[y1:y2, x1:x2]
    
    gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, binario = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    texto = pytesseract.image_to_string(binario, config='--psm 11')
    numeros = re.findall(r'\d+[.,]?\d*', texto)
    if numeros: return float(numeros[0].replace(',', '.'))

    binario_rotado1 = cv2.rotate(binario, cv2.ROTATE_90_CLOCKWISE)
    texto1 = pytesseract.image_to_string(binario_rotado1, config='--psm 11')
    numeros1 = re.findall(r'\d+[.,]?\d*', texto1)
    if numeros1: return float(numeros1[0].replace(',', '.'))

    binario_rotado2 = cv2.rotate(binario, cv2.ROTATE_90_COUNTERCLOCKWISE)
    texto2 = pytesseract.image_to_string(binario_rotado2, config='--psm 11')
    numeros2 = re.findall(r'\d+[.,]?\d*', texto2)
    if numeros2: return float(numeros2[0].replace(',', '.'))

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


def procesar_plano_ia(bytes_imagen, referencia_metros_manual, sistema_muro="ladrillo_hueco_12", tipo_plano="muros"):
    nparr = np.frombuffer(bytes_imagen, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("No se pudo leer la imagen del plano.")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    altura = 2.60
    
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

        res["items"].append({"nom": "Mano Obra: Muros", "val": m2_muros * P.get('mo_muro_hueco_m2', 0)})
        res["items"].append({"nom": "Mano Obra: Revoques", "val": m2_revoques * P.get('mo_revoque_doble_m2',0)})
        res["items"].append({"nom": "Mano Obra: Pisos", "val": m2_pisos * (P.get('mo_contrapiso_m2',0) + P.get('mo_carpeta_m2',0) + P.get('mo_ceramico_m2',0))})
        res["items"].append({"nom": "Materiales: Muros", "val": m2_muros * mat_muro})
        res["items"].append({"nom": "Materiales: Revoques", "val": m2_revoques * mat_revoque})
        res["items"].append({"nom": "Materiales: Pisos", "val": m2_pisos * (mat_contrapiso + mat_carpeta + mat_ceramico)})

        img_audit[mask_gris > 0] = [255, 150, 200] 
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
            res["items"].append({"nom": f"Mat: Caño Termo ({tot_ml_agua:.1f}m)", "val": tot_ml_agua * P.get('AGUA-MAT-01', 0)})
            res["items"].append({"nom": f"Mat: Codos ({tot_codos}u)", "val": tot_codos * P.get('AGUA-ACC-CODO', 0)})
            res["items"].append({"nom": f"Mat: Tees ({tot_tees}u)", "val": tot_tees * P.get('AGUA-ACC-TE', 0)})
            res["items"].append({"nom": f"M.O: Tender Cañería ({tot_ml_agua:.1f}m)", "val": tot_ml_agua * P.get('AGUA-MO-01', 0)})
            res["items"].append({"nom": f"M.O: Armado Bocas ({tot_bocas}u)", "val": tot_bocas * P.get('AGUA-BOCA-01', 0)})
        
        if ml_marron > 0: 
            res["items"].append({"nom": f"Mat: Caño Cloaca ({ml_marron:.1f}m)", "val": ml_marron * P.get('CLOA-MAT-01', 0)})
            res["items"].append({"nom": f"M.O: Inst. Cloaca ({ml_marron:.1f}m)", "val": ml_marron * P.get('CLOA-MO-01', 0)})
        
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
            res["items"].append({"nom": f"Mat: Caño Corrugado ({ml_corrugado:.1f}m)", "val": ml_corrugado * P.get('LUZ-MAT-01', 0)})
            res["items"].append({"nom": f"M.O: Tendido Eléctrico ({ml_corrugado:.1f}m)", "val": ml_corrugado * P.get('LUZ-MO-01', 0)})
        if cant_bocas > 0:
            res["items"].append({"nom": f"Mat: Cajas y Llaves ({cant_bocas}u)", "val": cant_bocas * P.get('LUZ-MAT-02', 0)})
            res["items"].append({"nom": f"M.O: Armado Bocas ({cant_bocas}u)", "val": cant_bocas * P.get('LUZ-MO-02', 0)})

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
            
            res["items"].append({"nom": f"Mat: Chapa Cincalum ({m2_techo:.1f}m2)", "val": m2_techo * P.get('TECH-CHAP-01', 0)})
            res["items"].append({"nom": f"Mat: Aislante ({m2_techo:.1f}m2)", "val": m2_techo * P.get('TECH-AISL-01', 0)})
            res["items"].append({"nom": f"Mat: Perfilería C ({ml_perfil:.1f}m)", "val": ml_perfil * P.get('TECH-PERF-01', 0)})
            res["items"].append({"nom": f"Mat: Tornillos autoperf. ({unid_tornillos:.0f}u)", "val": unid_tornillos * P.get('TECH-TORN-01', 0)})
            res["items"].append({"nom": f"M.O: Armado de Techo ({m2_techo:.1f}m2)", "val": m2_techo * P.get('TECH-MO-01', 0)})
            
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
                
                res["items"].append({"nom": f"🟩 LOTE {numero_lote} - Área", "val": f"{area_m2:.2f} m²"})
                res["items"].append({"nom": f"📏 LOTE {numero_lote} - Perímetro", "val": f"{perimetro_m:.2f} m"})
                
                # Lados
                epsilon = 0.02 * cv2.arcLength(c_terreno, True)
                vertices = cv2.approxPolyDP(c_terreno, epsilon, True)
                
                if len(vertices) >= 3:
                    for i in range(len(vertices)):
                        pt1 = vertices[i][0]
                        pt2 = vertices[(i + 1) % len(vertices)][0]
                        dist_m = np.linalg.norm(pt1 - pt2) * escala
                        res["items"].append({"nom": f"   ↳ Lado {i+1}", "val": f"{dist_m:.2f} m"})
                
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
    
    # FIX DEL BUG 500: Solo suma plata si NO es un terreno
    if tipo_plano != "terreno":
        res["total"] = sum(i["val"] for i in res["items"])
    else:
        res["total"] = 0
        
    return res
