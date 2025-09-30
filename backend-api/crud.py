import sqlite3
from .database import DB_NAME

def salvar_evento_visao(frame_id: int, qtd_motos: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eventos_visao (frame_id, qtd_motos) VALUES (?, ?)", 
                   (frame_id, qtd_motos))
    conn.commit()
    conn.close()

def listar_eventos_visao():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos_visao ORDER BY data_hora DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def salvar_evento_rfid(moto_id: str, zona: str, tipo_evento: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eventos_rfid (moto_id, zona, tipo_evento) VALUES (?, ?, ?)", 
                   (moto_id, zona, tipo_evento))
    conn.commit()
    conn.close()

def listar_eventos_rfid():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos_rfid ORDER BY data_hora DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
