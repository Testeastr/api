# api_imoveis/auth.py

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_KEY = "bbgcosnb6545dcnhvf16546jcb"  # Substitua por sua chave real
API_KEY_NAME = "chave"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def validar_chave(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Chave de API inválida.")
    return api_key
