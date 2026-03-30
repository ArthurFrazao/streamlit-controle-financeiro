import pandas as pd
from decimal import Decimal
from datetime import date
from src.database.connection import get_connection
from src.schemas.lancamento_schema import LancamentoCreate
from src.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def listar_lancamentos() -> pd.DataFrame:
    conn = get_connection()

    query = """
        SELECT
            id AS "ID",
            tipo AS "Tipo",
            data AS "Data",
            descricao AS "Descrição",
            categoria AS "Categoria",
            valor AS "Valor",
            forma_pagamento AS "Forma de Pagamento",
            cartao AS "Cartão",
            observacoes AS "Observações",
            recorrente AS "Recorrente",
            status AS "Status"
        FROM lancamentos
        ORDER BY id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.sort_values(by=["ID"]).reset_index(drop=True)


def inserir_lancamento(lancamento: LancamentoCreate) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Inserindo lancamento={lancamento.tipo}")
    cursor.execute(
        """
        INSERT INTO lancamentos (tipo, data, descricao, categoria, valor, forma_pagamento, cartao, observacoes, recorrente, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            lancamento.tipo,
            lancamento.data.isoformat() if lancamento.data else None,
            lancamento.descricao,
            lancamento.categoria,
            float(lancamento.valor),
            lancamento.forma_pagamento,
            lancamento.cartao,
            lancamento.observacoes,
            lancamento.recorrente,
            lancamento.status
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Lancamento={lancamento.tipo} inserido com sucesso")


def atualizar_lancamento(
    lancamento_id: int,
    tipo: str,
    data: date,
    descricao: str,
    categoria: str,
    valor: Decimal,
    forma_pagamento: str,
    cartao: str,
    observacoes: str,
    recorrente: str,
    status: str,
):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Atualizando lançamento ID={lancamento_id}")

    cursor.execute(
        """
        UPDATE lancamentos
        SET
            tipo = ?, 
            data = ?, 
            descricao = ?, 
            categoria = ?, 
            valor = ?, 
            forma_pagamento = ?, 
            cartao = ?, 
            observacoes = ?, 
            recorrente = ?, 
            status = ?
        WHERE id = ?
        """,
        (
            tipo,
            data.isoformat() if data else None,
            descricao,
            categoria,
            float(valor),
            forma_pagamento,
            cartao,
            observacoes,
            recorrente,
            status,
            lancamento_id
        ),
    )

    conn.commit()
    conn.close()
    logger.info(f"Lançamento ID={lancamento_id} atualizado com sucesso")


def excluir_lancamento(lancamento_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    logger.info(f"Excluindo lançamento ID={lancamento_id}")

    cursor.execute(
        "DELETE FROM lancamentos WHERE id = ?",
        (lancamento_id,),
    )

    conn.commit()
    conn.close()
    logger.info(f"Lançamento ID={lancamento_id} excluído com sucesso")