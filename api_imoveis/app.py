from fastapi import FastAPI
from api_imoveis.routers import imoveis, extracao

app = FastAPI(title="API de Imóveis")

app.include_router(imoveis.router)
app.include_router(extracao.router)

@app.get("/")
def root():
    return {"message": "API Imóveis rodando com sucesso!"}
