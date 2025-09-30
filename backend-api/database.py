import sqlite3

DB_NAME = "motos.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabela de eventos de visão computacional
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos_visao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        frame_id INTEGER,
        qtd_motos INTEGER,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tabela de eventos RFID
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos_rfid (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        moto_id TEXT,
        zona TEXT,
        tipo_evento TEXT,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
