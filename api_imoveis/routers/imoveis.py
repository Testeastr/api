from fastapi import APIRouter, Depends
from pathlib import Path
import json
import os
from api_imoveis.auth import validar_chave  # importa a função de autenticação

router = APIRouter()

@router.get("/imovel/{imovel_id:path}")
def get_imovel(imovel_id: str, chave: str = Depends(validar_chave)):  # <-- aqui
    base_dir = os.path.dirname(__file__)  # api_imoveis/routers
    json_path = os.path.join(base_dir, "..", "data", "banco_fake.json")  # api_imoveis/data/banco_fake.json
    path = Path(json_path).resolve()

    with path.open("r", encoding="utf-8") as f:
        banco = json.load(f)  # banco é lista de dicts

    # Busca imóvel pelo id na lista
    for imovel in banco:
        if str(imovel.get("id")) == imovel_id:
            return imovel

    return {"erro": "Imóvel não encontrado"}
