from pydantic import BaseModel

# Dados enviados pela visão computacional
class VisaoData(BaseModel):
    frame_id: int
    qtd_motos: int

# Dados enviados pelo sensor RFID
class RFIDData(BaseModel):
    moto_id: str
    zona: str
    tipo_evento: str  # exemplo: "entrada", "saida", "reparo"
