import pandas as pd
from src.database.connection import get_connection
from src.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def listar_formas() -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info("Buscando nomes de formas no banco de dados")

    cursor.execute("""
        SELECT forma
        FROM formas
    """)

    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]