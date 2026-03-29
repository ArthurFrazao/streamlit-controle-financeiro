import pandas as pd
from decimal import Decimal
from src.database.connection import get_connection
from src.schemas.despesa_parcelada_schema import DespesaParceladaCreate
from src.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def listar_despesas_parceladas() -> pd.DataFrame:
    conn = get_connection()

    query = """
        SELECT
            id AS "ID",
            vencimento AS "Vencimento",
            data AS "Data",
            descricao AS "Descrição",
            categoria AS "Categoria",
            valor_total AS "Valor Total",
            valor_parcela AS "Valor Parcela",
            qtd_parcelas AS "Qtd. Parcelas",
            parcela_atual AS "Parcela Atual",
            cartao AS "cartao"
        FROM despesas_parceladas
        ORDER BY data DESC, id DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date
        df["Vencimento"] = pd.to_datetime(df["Vencimento"], errors="coerce").dt.date

    return df.sort_values(by=["ID"]).reset_index(drop=True)


def inserir_despesa_parcelada(despesa: DespesaParceladaCreate) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Inserindo despesa parcelada={despesa.descricao}")
    cursor.execute(
        """
        INSERT INTO despesas_parceladas
            (data, vencimento, descricao, categoria, valor_total, valor_parcela, qtd_parcelas, parcela_atual, cartao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            despesa.data.isoformat() if despesa.data else None,
            despesa.vencimento.isoformat() if despesa.vencimento else None,
            despesa.descricao,
            despesa.categoria,
            float(despesa.valor_total),
            float(despesa.valor_parcela),
            despesa.qtd_parcelas,
            despesa.parcela_atual,
            despesa.cartao
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Despesa parcelada={despesa.descricao} inserida com sucesso")


def atualizar_despesa_parcelada(
    despesa_id: int,
    descricao: str,
    categoria: str,
    valor_total: Decimal,
    valor_parcela: Decimal,
    qtd_parcelas: int,
    parcela_atual: int,
    data,
    vencimento,
    cartao
):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Atualizando despesa parcelada ID={despesa_id}")

    cursor.execute(
        """
        UPDATE despesas_parceladas
        SET
            descricao = ?,
            categoria = ?,
            valor_total = ?,
            valor_parcela = ?,
            qtd_parcelas = ?,
            parcela_atual = ?,
            data = ?,
            vencimento = ?,
            cartao = ?
        WHERE id = ?
        """,
        (
            descricao,
            categoria,
            float(valor_total),
            float(valor_parcela),
            qtd_parcelas,
            parcela_atual,
            data.isoformat() if data else None,
            vencimento.isoformat() if vencimento else None,
            cartao,
            despesa_id,
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Despesa parcelada ID={despesa_id} atualizada com sucesso")


def excluir_despesa_parcelada(despesa_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Excluindo despesa parcelada ID={despesa_id}")

    cursor.execute(
        "DELETE FROM despesas_parceladas WHERE id = ?",
        (despesa_id,),
    )

    conn.commit()
    conn.close()
    logger.info(f"Despesa parcelada ID={despesa_id} excluída com sucesso")
