import pandas as pd
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

    cursor.execute("SELECT categoria FROM categorias")
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


def listar_categorias() -> pd.DataFrame:
    conn = get_connection()

    query = """
        SELECT 
            id AS "ID",
            categoria AS "Categoria", 
            orcamento_mensal AS "Orçamento Mensal", 
            essencial AS "Essencial"
        FROM categorias
    """

    df = pd.read_sql_query(query, conn)
    df["Essencial"] = df["Essencial"].astype("bool")
    conn.close()

    return df.sort_values(by=["ID"]).reset_index(drop=True)


def inserir_categoria(categoria: CategoriaCreate) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Inserindo categoria={categoria.categoria}")

    cursor.execute(
        """
        INSERT INTO categorias (categoria, orcamento_mensal, essencial)
        VALUES (?, ?, ?)
        """,
        (
            categoria.categoria,
            float(categoria.orcamento_mensal),
            int(categoria.essencial),
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Categoria={categoria.categoria} inserida com sucesso")


def atualizar_categoria(
    categoria_id: int,
    categoria: str,
    orcamento_mensal: Decimal,
    essencial: bool
):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Atualizando categoria ID={categoria_id}")

    cursor.execute(
        """
        UPDATE categorias
        SET
            categoria = ?,
            orcamento_mensal = ?,
            essencial = ?
        WHERE id = ?
        """,
        (
            categoria,
            float(orcamento_mensal),
            essencial,
            categoria_id,
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Categoria ID={categoria_id} atualizada com sucesso")


def excluir_categoria(categoria_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Excluindo categoria ID={categoria_id}")

    cursor.execute(
        "DELETE FROM categorias WHERE id = ?",
        (categoria_id,),
    )

    conn.commit()
    conn.close()
    logger.info(f"Categoria ID={categoria_id} excluída com sucesso")