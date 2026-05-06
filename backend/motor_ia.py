import cv2
import numpy as np
import base64
import urllib.request
import csv
import codecs
import pytesseract
import re

# RUTA DE TESSERACT (Tu disco D:)
pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

def obtener_precios_en_vivo():
    url_csv = "https://docs.google.com/spreadsheets/d/1fmULPVz8YeKJT9jLyGRy6ZBOLpXz-wfgJSaF_Br5s28/export?format=csv"
    P = {
        'mat_cemento_50kg': 9000, 'mat_cal_25kg': 4500, 'mat_arena_m3': 22000, 
        'mat_escombro_m3': 15000, 'mat_ladrillo_hueco': 600, 'mat_ladrillo_comun': 120, 
        'mat_ceramico_m2': 15000, 'mat_pegamento_30kg': 12000, 'mat_abertura_promedio': 150000,
        'mo_muro_hueco_m2': 12000, 'mo_muro_comun_m2': 13000, 'mo_revoque_doble_m2': 20000,
        'mo_contrapiso_m2': 13000, 'mo_carpeta_m2': 12000, 'mo_ceramico_m2': 15000, 'mo_abertura_unid': 70000,
        'mat_agua_fria_m': 1500, 'mat_agua_caliente_m': 2500, 'mat_cloaca_110_m': 4000,
        'mo_boca_agua': 15000, 'mo_boca_luz': 12000, 'mat_corrugado_m': 800
    }
    try:
        response = urllib.request.urlopen(url_csv)
        reader = csv.reader(codecs.iterdecode(response, 'utf-8'))
        next(reader, None)
        for row in reader:
            if len(row) >= 3:
                try: P[row[0].strip()] = float(row[2].strip().replace('$', '').replace('.', '').replace(',', ''))
                except: pass
    except: pass
    return P

def extraer_numero_escala(img, mask_verde):
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
    
    # 1. Intentamos leer normal (Horizontal)
    texto = pytesseract.image_to_string(binario, config='--psm 11')
    numeros = re.findall(r'\d+[.,]?\d*', texto)
    if numeros: return float(numeros[0].replace(',', '.'))

    # 2. IA "Gira la cabeza" (Vertical 90 grados derecha)
    binario_rotado1 = cv2.rotate(binario, cv2.ROTATE_90_CLOCKWISE)
    texto1 = pytesseract.image_to_string(binario_rotado1, config='--psm 11')
    numeros1 = re.findall(r'\d+[.,]?\d*', texto1)
    if numeros1: return float(numeros1[0].replace(',', '.'))

    # 3. IA "Gira la cabeza" (Vertical 90 grados izquierda)
    binario_rotado2 = cv2.rotate(binario, cv2.ROTATE_90_COUNTERCLOCKWISE)
    texto2 = pytesseract.image_to_string(binario_rotado2, config='--psm 11')
    numeros2 = re.findall(r'\d+[.,]?\d*', texto2)
    if numeros2: return float(numeros2[0].replace(',', '.'))

    return None

def procesar_plano_ia(bytes_imagen, referencia_metros_manual, sistema_muro="ladrillo_hueco_12", tipo_plano="muros"):
    nparr = np.frombuffer(bytes_imagen, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    altura = 2.60
    
    # --- ESCALA VERDE Y OCR ---
    mask_v = cv2.inRange(hsv, np.array([40, 150, 50]), np.array([80, 255, 255]))
    px_v = np.sum(cv2.ximgproc.thinning(mask_v) > 0)
    
    escala_leida = extraer_numero_escala(img, mask_v)
    metros_reales = escala_leida if escala_leida else float(referencia_metros_manual)
    escala = (metros_reales / px_v) if px_v > 0 else 0.02

    P = obtener_precios_en_vivo()
    res = {"tipo": tipo_plano, "items": [], "total": 0, "imagen": "", "escala_detectada": escala_leida}
    img_audit = img.copy()

    # --- MÓDULO 1: ESTRUCTURA, MUROS, PISOS Y ABERTURAS (COMPLETO) ---
    if tipo_plano == "muros":
        mask_rojo = cv2.inRange(hsv, np.array([0, 150, 50]), np.array([10, 255, 255]))
        m2_muros = (np.sum(cv2.ximgproc.thinning(mask_rojo) > 0) * escala) * altura
        m2_revoques = m2_muros * 2 
        
        mask_cian = cv2.inRange(hsv, np.array([85, 150, 50]), np.array([105, 255, 255]))
        contornos_cian, _ = cv2.findContours(mask_cian, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        unid_aberturas = len(contornos_cian)

        mask_gris = cv2.inRange(hsv, np.array([0, 0, 180]), np.array([179, 30, 230]))
        mask_naranja = cv2.inRange(hsv, np.array([10, 150, 150]), np.array([25, 255, 255]))
        m2_pisos = (np.sum(mask_gris > 0) + np.sum(mask_naranja > 0)) * (escala ** 2)

        precio_cemento_kg = P.get('mat_cemento_50kg', 0) / 50
        precio_cal_kg = P.get('mat_cal_25kg', 0) / 25
        precio_pegamento_kg = P.get('mat_pegamento_30kg', 0) / 30

        mat_muro = (15 * P.get('mat_ladrillo_hueco',0)) + (4 * precio_cemento_kg) + (0.015 * P.get('mat_arena_m3',0))
        mat_revoque = (5 * precio_cemento_kg) + (3 * precio_cal_kg) + (0.02 * P.get('mat_arena_m3',0))
        mat_contrapiso = (7.5 * precio_cemento_kg) + (3.5 * precio_cal_kg) + (0.035 * P.get('mat_arena_m3',0)) + (0.07 * P.get('mat_escombro_m3',0))
        mat_carpeta = (10.5 * precio_cemento_kg) + (0.03 * P.get('mat_arena_m3',0))
        mat_ceramico = (1.05 * P.get('mat_ceramico_m2',0)) + (4 * precio_pegamento_kg)

        res["items"].append({"nom": "Mano Obra: Muros", "val": m2_muros * P.get('mo_muro_hueco_m2', 0)})
        res["items"].append({"nom": "Mano Obra: Revoques", "val": m2_revoques * P.get('mo_revoque_doble_m2',0)})
        res["items"].append({"nom": "Mano Obra: Pisos Completos", "val": m2_pisos * (P.get('mo_contrapiso_m2',0) + P.get('mo_carpeta_m2',0) + P.get('mo_ceramico_m2',0))})
        res["items"].append({"nom": "Mano Obra: Aberturas", "val": unid_aberturas * P.get('mo_abertura_unid',0)})
        
        res["items"].append({"nom": "Materiales: Muros", "val": m2_muros * mat_muro})
        res["items"].append({"nom": "Materiales: Revoques", "val": m2_revoques * mat_revoque})
        res["items"].append({"nom": "Materiales: Pisos Completos", "val": m2_pisos * (mat_contrapiso + mat_carpeta + mat_ceramico)})
        res["items"].append({"nom": "Materiales: Aberturas", "val": unid_aberturas * P.get('mat_abertura_promedio',0)})

        img_audit[mask_gris > 0] = [255, 150, 200] 
        img_audit[mask_naranja > 0] = [150, 200, 255] 
        kernel = np.ones((15, 15), np.uint8)
        img_audit[cv2.bitwise_and(cv2.dilate(cv2.ximgproc.thinning(mask_rojo), kernel, iterations=1), mask_rojo) > 0] = [0, 255, 255]
        cv2.drawContours(img_audit, contornos_cian, -1, (255, 0, 0), 3)

    # --- MÓDULO 2 Y 3: AGUA Y LUZ (Acá mantengo el código IRAM que sumamos recién) ---
    elif tipo_plano == "agua":
        mask_azul = cv2.inRange(hsv, np.array([100, 150, 50]), np.array([130, 255, 255]))
        mask_magenta = cv2.inRange(hsv, np.array([140, 150, 50]), np.array([170, 255, 255]))
        mask_marron = cv2.inRange(hsv, np.array([10, 100, 20]), np.array([20, 255, 200]))
        
        ml_azul = np.sum(cv2.ximgproc.thinning(mask_azul) > 0) * escala
        ml_magenta = np.sum(cv2.ximgproc.thinning(mask_magenta) > 0) * escala
        ml_marron = np.sum(cv2.ximgproc.thinning(mask_marron) > 0) * escala
        
        if ml_azul > 0: res["items"].append({"nom": "Mat: Caño Termo Azul", "val": ml_azul * P.get('mat_agua_fria_m', 1500)})
        if ml_magenta > 0: res["items"].append({"nom": "Mat: Caño Termo Carmín", "val": ml_magenta * P.get('mat_agua_caliente_m', 2500)})
        if ml_marron > 0: res["items"].append({"nom": "Mat: Caño PVC 110 Sepia", "val": ml_marron * P.get('mat_cloaca_110_m', 4000)})
        
        img_audit[mask_azul > 0] = [255, 0, 0]; img_audit[mask_magenta > 0] = [255, 0, 255]; img_audit[mask_marron > 0] = [0, 100, 255]

    elif tipo_plano == "luz":
        mask_amarilla = cv2.inRange(hsv, np.array([20, 150, 50]), np.array([35, 255, 255]))
        conts, _ = cv2.findContours(mask_amarilla, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ml_corrugado = np.sum(cv2.ximgproc.thinning(mask_amarilla) > 0) * escala
        
        if len(conts) > 0: res["items"].append({"nom": f"M.O: Bocas Eléctricas ({len(conts)})", "val": len(conts) * P.get('mo_boca_luz', 12000)})
        if ml_corrugado > 0: res["items"].append({"nom": "Mat: Caño Corrugado", "val": ml_corrugado * P.get('mat_corrugado_m', 800)})
        cv2.drawContours(img_audit, conts, -1, (0, 165, 255), -1)

    # Terminamos de pintar la línea verde
    if px_v > 0:
        kernel = np.ones((15,15), np.uint8)
        img_audit[cv2.bitwise_and(cv2.dilate(cv2.ximgproc.thinning(mask_v), kernel, iterations=1), mask_v) > 0] = [0, 255, 0]
    
    _, buf = cv2.imencode('.png', img_audit)
    res["imagen"] = base64.b64encode(buf).decode('utf-8')
    res["total"] = sum(i["val"] for i in res["items"])
    
    return res