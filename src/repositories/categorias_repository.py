from decimal import Decimal
from src.database.connection import get_connection
from src.schemas.categoria_schema import CategoriaCreate
from src.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def listar_nomes_categorias() -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info("Buscando nomes das categorias no banco de dados")

    cursor.execute("""
        SELECT categoria
        FROM categorias
        WHERE categoria IS NOT NULL
          AND TRIM(categoria) <> ''
        ORDER BY categoria
    """)

    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


def listar_categorias() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info("Buscando categorias completas no banco de dados")

    cursor.execute("""
        SELECT id, categoria, orcamento_mensal, essencial
        FROM categorias
        WHERE categoria IS NOT NULL
          AND TRIM(categoria) <> ''
        ORDER BY categoria
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "ID": row[0],
            "Categoria": row[1],
            "Orçamento Mensal": row[2],
            "Essencial": bool(row[3]),
        }
        for row in rows
    ]


def inserir_categoria(categoria: CategoriaCreate) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Inserindo nova categoria: {categoria.categoria}")

    cursor.execute(
        """
        INSERT INTO categorias (categoria, orcamento_mensal, essencial)
        VALUES (?, ?, ?)
        """,
        (
            categoria.categoria,
            float(categoria.orcamento_mensal) if categoria.orcamento_mensal is not None else None,
            int(categoria.essencial),
        ),
    )

    conn.commit()
    conn.close()
