import sqlite3
from contextlib import contextmanager
from datetime import datetime

DB_PATH = "clinica.db"

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tutor TEXT NOT NULL,
                pet TEXT NOT NULL,
                data TEXT NOT NULL,
                hora TEXT NOT NULL,
                criado_em TEXT NOT NULL,
                UNIQUE(data, hora)
            )
        """)
        conn.execute("PRAGMA journal_mode=WAL")

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def horarios_disponiveis(data: str) -> list[str]:
    slots = [f"{h:02d}:00" for h in range(8, 18)]
    with get_conn() as conn:
        ocupados = {r[0] for r in conn.execute(
            "SELECT hora FROM agendamentos WHERE data = ?", (data,)
        )}
    return [s for s in slots if s not in ocupados]

def agendar(tutor: str, pet: str, data: str, hora: str) -> tuple[bool, str]:
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO agendamentos (tutor, pet, data, hora, criado_em) VALUES (?,?,?,?,?)",
                (tutor, pet, data, hora, datetime.now().isoformat())
            )
        return True, "Agendamento confirmado."
    except sqlite3.IntegrityError:
        return False, "Esse horário acabou de ser ocupado."