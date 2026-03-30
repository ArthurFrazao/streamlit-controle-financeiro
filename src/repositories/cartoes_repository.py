import pandas as pd
from decimal import Decimal
from datetime import date
from src.database.connection import get_connection
from src.schemas.cartao_schema import CartaoCreate
from src.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def listar_nomes_cartoes() -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info("Buscando nomes dos cartões no banco de dados")

    cursor.execute("SELECT nome FROM cartoes")
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


def listar_cartoes() -> pd.DataFrame:
    conn = get_connection()

    query = """
        SELECT
            id AS "ID",
            nome AS "Nome",
            vencimento AS "Vencimento",
            limite AS "Limite",
            tipo AS "Tipo"
        FROM cartoes
        ORDER BY id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.sort_values(by=["ID"]).reset_index(drop=True)


def inserir_cartao(cartao: CartaoCreate) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Inserindo cartão={cartao.nome}")
    cursor.execute(
        """
        INSERT INTO cartoes (nome, vencimento, limite, tipo)
        VALUES (?, ?, ?, ?)
        """,
        (
            cartao.nome,
            cartao.vencimento,
            float(cartao.limite),
            cartao.tipo
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Cartão={cartao.nome} inserida com sucesso")


def atualizar_cartao(
    cartao_id: int,
    nome: str,
    vencimento: int,
    limite: Decimal,
    tipo: str,
):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Atualizando cartão ID={cartao_id}")

    cursor.execute(
        """
        UPDATE cartoes
        SET
            nome = ?,
            vencimento = ?,
            limite = ?,
            tipo = ?
        WHERE id = ?
        """,
        (
            nome,
            vencimento,
            float(limite),
            tipo,
            cartao_id,
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Cartão ID={cartao_id} atualizada com sucesso")


def excluir_cartao(cartao_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Excluindo cartão ID={cartao_id}")

    cursor.execute(
        "DELETE FROM cartoes WHERE id = ?",
        (cartao_id,),
    )

    conn.commit()
    conn.close()
    logger.info(f"Cartão ID={cartao_id} excluída com sucesso")
