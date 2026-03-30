import pandas as pd
from decimal import Decimal
from datetime import date
from src.database.connection import get_connection
from src.schemas.despesa_fixa_schema import DespesaFixaCreate
from src.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def listar_despesas_fixas() -> pd.DataFrame:
    conn = get_connection()

    query = """
        SELECT
            id AS "ID",
            data AS "Data",
            descricao AS "Descrição",
            categoria AS "Categoria",
            valor AS "Valor",
            cartao AS "Cartao",
            forma AS "Forma"
        FROM despesas_fixas
        ORDER BY data DESC, id DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date

    return df.sort_values(by=["ID"]).reset_index(drop=True)


def inserir_despesa_fixa(despesa: DespesaFixaCreate) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Inserindo despesa fixa={despesa.descricao}")
    cursor.execute(
        """
        INSERT INTO despesas_fixas (data, descricao, categoria, valor, cartao, forma)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            despesa.data.isoformat() if despesa.data else None,
            despesa.descricao,
            despesa.categoria,
            float(despesa.valor),
            despesa.cartao,
            despesa.forma
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Despesa fixa={despesa.descricao} inserida com sucesso")


def atualizar_despesa_fixa(
    despesa_id: int,
    descricao: str,
    categoria: str,
    valor: Decimal,
    data: date,
    cartao: str,
    forma: str
):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Atualizando despesa fixa ID={despesa_id}")

    cursor.execute(
        """
        UPDATE despesas_fixas
        SET
            descricao = ?,
            categoria = ?,
            valor = ?,
            data = ?,
            cartao = ?,
            forma = ?
        WHERE id = ?
        """,
        (
            descricao,
            categoria,
            float(valor),
            data.isoformat() if data else None,
            cartao,
            forma,
            despesa_id,
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Despesa fixa ID={despesa_id} atualizada com sucesso")


def excluir_despesa_fixa(despesa_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Excluindo despesa fixa ID={despesa_id}")

    cursor.execute(
        "DELETE FROM despesas_fixas WHERE id = ?",
        (despesa_id,),
    )

    conn.commit()
    conn.close()
    logger.info(f"Despesa fixa ID={despesa_id} excluída com sucesso")
