from fastapi import FastAPI
from api_imoveis.routers import imoveis, extracao

app = FastAPI(title="API de Imóveis")

# Agrupa rotas no Swagger e define prefixos
app.include_router(imoveis.router, prefix="/imovel", tags=["Imóveis"])
app.include_router(extracao.router, prefix="/extracao", tags=["Extração de PDF"])

@app.get("/")
def root():
    return {"message": "API Imóveis rodando com sucesso!"}
