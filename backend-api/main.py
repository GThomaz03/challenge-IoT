from fastapi import FastAPI
from .database import create_tables
from .models import VisaoData, RFIDData
from . import crud

app = FastAPI(title="Mottu IoT API", version="1.0")

# Criar tabelas ao iniciar
create_tables()

@app.get("/")
def root():
    return {"status": "API rodando 🚀"}

# ================== VISÃO COMPUTACIONAL ==================
@app.post("/visao/registrar")
def registrar_visao(dados: VisaoData):
    crud.salvar_evento_visao(dados.frame_id, dados.qtd_motos)
    return {"status": "ok", "dados": dados}

@app.get("/visao/listar")
def listar_visao():
    return crud.listar_eventos_visao()

# ================== RFID ==================
@app.post("/rfid/registrar")
def registrar_rfid(dados: RFIDData):
    crud.salvar_evento_rfid(dados.moto_id, dados.zona, dados.tipo_evento)
    return {"status": "ok", "dados": dados}

@app.get("/rfid/listar")
def listar_rfid():
    return crud.listar_eventos_rfid()
