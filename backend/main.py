from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from motor_ia import procesar_plano_ia
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calcular")
async def calcular(
    file: UploadFile = File(...), 
    referencia_metros: float = Form(...),
    sistema_muro: str = Form("ladrillo_hueco_12"),
    tipo_plano: str = Form("muros") # <-- 'muros', 'agua', 'luz', 'techo'
):
    contenido = await file.read()
    resultados = procesar_plano_ia(contenido, referencia_metros, sistema_muro, tipo_plano)
    return resultados

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)