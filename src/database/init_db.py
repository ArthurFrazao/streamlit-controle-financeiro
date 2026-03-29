from pathlib import Path
from src.database.connection import get_connection
from src.core.logging import get_logger

logger = get_logger(__name__)

def init_db():
    logger.info("Inicializando banco de dados")
    conn = get_connection()
    cursor = conn.cursor()

    schema_path = Path(__file__).resolve().parent / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
        logger.info("Tabelas criadas no banco")

    conn.commit()
    conn.close()