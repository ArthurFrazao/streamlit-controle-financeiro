import sqlite3
from src.core.config import DB_PATH
from src.core.logging import get_logger

logger = get_logger(__name__)

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn