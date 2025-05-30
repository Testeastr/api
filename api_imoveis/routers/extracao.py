from fastapi import APIRouter, UploadFile, File
import shutil
import os
from api_imoveis.services.extrator_pdf import extrair_e_salvar_todos

router = APIRouter()

CAMINHO_PDFTOTEXT = r"C:\Users\Eduarda.Amorim\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin\pdftotext.exe"

@router.post("/extrair-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        dados_extraidos = extrair_e_salvar_todos(temp_path, CAMINHO_PDFTOTEXT)
        return {"mensagem": "Dados extraídos e salvos", "dados": dados_extraidos}
    finally:
        os.remove(temp_path)
