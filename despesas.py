from decimal import Decimal
import streamlit as st
from pydantic import ValidationError

from src.repositories.categorias_repository import listar_nomes_categorias
from src.repositories.despesas_fixas_repository import (
    listar_despesas_fixas,
    inserir_despesa_fixa,
    atualizar_despesa_fixa,
    excluir_despesa_fixa,
)
from src.repositories.despesas_parceladas_repository import (
    listar_despesas_parceladas,
    inserir_despesa_parcelada,
    atualizar_despesa_parcelada,
    excluir_despesa_parcelada,
)
from src.schemas.despesa_fixa_schema import DespesaFixaCreate
from src.schemas.despesa_parcelada_schema import DespesaParceladaCreate


# =========================
# HELPERS
# =========================
def reset_keys(*keys):
    for key in keys:
        st.session_state.pop(key, None)


# =========================
# KEYS DOS FORMULÁRIOS
# =========================
KEYS_FORM_DESPESA_FIXA = (
    "fixa_data_input",
    "fixa_vencimento_input",
    "fixa_descricao_input",
    "fixa_categoria_input",
    "fixa_valor_input",
)

KEYS_FORM_DESPESA_PARCELADA = (
    "parc_data_input",
    "parc_vencimento_input",
    "parc_descricao_input",
    "parc_categoria_input",
    "parc_valor_total_input",
    "parc_valor_parcela_input",
    "parc_qtd_parcelas_input",
    "parc_parcela_atual_input",
)


# =========================
# ESTADOS
# =========================
def inicializar_estados():
    if "df_despesas_fixas" not in st.session_state:
        st.session_state.df_despesas_fixas = listar_despesas_fixas()

    if "df_despesas_parceladas" not in st.session_state:
        st.session_state.df_despesas_parceladas = listar_despesas_parceladas()

    if "mostrar_form_adicionar_despesa_fixa" not in st.session_state:
        st.session_state.mostrar_form_adicionar_despesa_fixa = False

    if "mostrar_form_editar_despesa_fixa" not in st.session_state:
        st.session_state.mostrar_form_editar_despesa_fixa = False

    if "mostrar_form_adicionar_despesa_parcelada" not in st.session_state:
        st.session_state.mostrar_form_adicionar_despesa_parcelada = False

    if "mostrar_form_editar_despesa_parcelada" not in st.session_state:
        st.session_state.mostrar_form_editar_despesa_parcelada = False

    if "categorias_despesa" not in st.session_state:
        st.session_state.categorias_despesa = listar_nomes_categorias()

    if "filtro_reset_counter_fixa" not in st.session_state:
        st.session_state.filtro_reset_counter_fixa = 0

    if "filtro_reset_counter_parcelada" not in st.session_state:
        st.session_state.filtro_reset_counter_parcelada = 0


def refresh_despesas_fixas():
    st.session_state.df_despesas_fixas = listar_despesas_fixas()


def refresh_despesas_parceladas():
    st.session_state.df_despesas_parceladas = listar_despesas_parceladas()


# =========================
# FILTROS
# =========================
def aplicar_filtros_fixas(df, col):
    counter = st.session_state.filtro_reset_counter_fixa

    with col.expander("🔍 Filtros", expanded=False):
        col1, col2, col3 = st.columns(3)

        data_inicio = col1.date_input(
            "Data inicial", value=None, key=f"fixa_filtro_data_inicio_{counter}"
        )
        data_fim = col2.date_input(
            "Data final", value=None, key=f"fixa_filtro_data_fim_{counter}"
        )

        categorias = ["Todas"] + st.session_state.categorias_despesa
        categoria = col3.selectbox(
            "Categoria", categorias, key=f"fixa_filtro_categoria_{counter}"
        )

        if st.button("Limpar filtros", use_container_width=True, key="fixa_limpar_filtros"):
            st.session_state.filtro_reset_counter_fixa += 1
            st.rerun()

    df_filtrado = df.copy()

    if data_inicio:
        df_filtrado = df_filtrado[df_filtrado["Data"] >= data_inicio]
    if data_fim:
        df_filtrado = df_filtrado[df_filtrado["Data"] <= data_fim]
    if categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria]

    return df_filtrado


def aplicar_filtros_parceladas(df, col):
    counter = st.session_state.filtro_reset_counter_parcelada

    with col.expander("🔍 Filtros", expanded=False):
        col1, col2, col3 = st.columns(3)

        data_inicio = col1.date_input(
            "Data inicial", value=None, key=f"parc_filtro_data_inicio_{counter}"
        )
        data_fim = col2.date_input(
            "Data final", value=None, key=f"parc_filtro_data_fim_{counter}"
        )

        categorias = ["Todas"] + st.session_state.categorias_despesa
        categoria = col3.selectbox(
            "Categoria", categorias, key=f"parc_filtro_categoria_{counter}"
        )

        if st.button("Limpar filtros", use_container_width=True, key="parc_limpar_filtros"):
            st.session_state.filtro_reset_counter_parcelada += 1
            st.rerun()

    df_filtrado = df.copy()

    if data_inicio:
        df_filtrado = df_filtrado[df_filtrado["Data"] >= data_inicio]
    if data_fim:
        df_filtrado = df_filtrado[df_filtrado["Data"] <= data_fim]
    if categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria]

    return df_filtrado


# =========================
# CONTROLE DOS DIALOGS — DESPESAS FIXAS
# =========================
def abrir_formulario_adicionar_despesa_fixa():
    reset_keys(*KEYS_FORM_DESPESA_FIXA)
    st.session_state.mostrar_form_adicionar_despesa_fixa = True


def abrir_formulario_editar_despesa_fixa():
    reset_keys(*KEYS_FORM_DESPESA_FIXA, "fixa_despesa_select")
    st.session_state.mostrar_form_editar_despesa_fixa = True


def fechar_formulario_adicionar_despesa_fixa():
    reset_keys(*KEYS_FORM_DESPESA_FIXA)
    st.session_state.mostrar_form_adicionar_despesa_fixa = False


def fechar_formulario_editar_despesa_fixa():
    reset_keys(*KEYS_FORM_DESPESA_FIXA, "fixa_despesa_select")
    st.session_state.mostrar_form_editar_despesa_fixa = False


# =========================
# CONTROLE DOS DIALOGS — DESPESAS PARCELADAS
# =========================
def abrir_formulario_adicionar_despesa_parcelada():
    reset_keys(*KEYS_FORM_DESPESA_PARCELADA)
    st.session_state.mostrar_form_adicionar_despesa_parcelada = True


def abrir_formulario_editar_despesa_parcelada():
    reset_keys(*KEYS_FORM_DESPESA_PARCELADA, "parc_despesa_select")
    st.session_state.mostrar_form_editar_despesa_parcelada = True


def fechar_formulario_adicionar_despesa_parcelada():
    reset_keys(*KEYS_FORM_DESPESA_PARCELADA)
    st.session_state.mostrar_form_adicionar_despesa_parcelada = False


def fechar_formulario_editar_despesa_parcelada():
    reset_keys(*KEYS_FORM_DESPESA_PARCELADA, "parc_despesa_select")
    st.session_state.mostrar_form_editar_despesa_parcelada = False


# =========================
# BOTÕES — DESPESAS FIXAS
# =========================
def carregar_botao_adicionar_despesa_fixa(col):
    if col.button("Adicionar despesa fixa", width="stretch"):
        st.session_state.categorias_despesa = listar_nomes_categorias(tipo="fixa")
        abrir_formulario_adicionar_despesa_fixa()


def carregar_botao_editar_despesa_fixa(col):
    if col.button("Editar despesa fixa", width="stretch"):
        st.session_state.categorias_despesa = listar_nomes_categorias(tipo="fixa")
        abrir_formulario_editar_despesa_fixa()


# =========================
# BOTÕES — DESPESAS PARCELADAS
# =========================
def carregar_botao_adicionar_despesa_parcelada(col):
    if col.button("Adicionar despesa parcelada", width="stretch"):
        st.session_state.categorias_despesa = listar_nomes_categorias(tipo="parcelada")
        abrir_formulario_adicionar_despesa_parcelada()


def carregar_botao_editar_despesa_parcelada(col):
    if col.button("Editar despesa parcelada", width="stretch"):
        st.session_state.categorias_despesa = listar_nomes_categorias(tipo="parcelada")
        abrir_formulario_editar_despesa_parcelada()


# =========================
# DIALOG ADICIONAR — DESPESA FIXA
# =========================
@st.dialog("Adicionar nova despesa fixa", dismissible=True, on_dismiss=fechar_formulario_adicionar_despesa_fixa)
def renderizar_formulario_adicionar_despesa_fixa():
    categorias = st.session_state.categorias_despesa

    if not categorias:
        st.warning("Nenhuma categoria cadastrada.")
        return

    descricao = st.text_input("Descrição", key="fixa_descricao_input")
    categoria = st.selectbox("Categoria", options=categorias, key="fixa_categoria_input")
    valor = st.number_input("Valor", min_value=0.01, step=0.01, format="%.2f", key="fixa_valor_input")
    data = st.date_input("Data", value=None, key="fixa_data_input")
    vencimento = st.date_input("Vencimento", value=None, key="fixa_vencimento_input")

    col_confirmar, col_cancelar = st.columns(2)

    if col_cancelar.button("Cancelar", width="stretch", key="fixa_add_cancelar"):
        fechar_formulario_adicionar_despesa_fixa()
        st.rerun()

    if col_confirmar.button("Confirmar", width="stretch", key="fixa_add_confirmar"):
        try:
            despesa = DespesaFixaCreate(
                data=data,
                vencimento=vencimento,
                descricao=descricao,
                categoria=categoria,
                valor=Decimal(str(valor)),
            )

            inserir_despesa_fixa(despesa)
            refresh_despesas_fixas()
            fechar_formulario_adicionar_despesa_fixa()

            st.success("Despesa fixa adicionada com sucesso.")
            st.rerun()

        except ValidationError as e:
            for erro in e.errors():
                st.error(erro["msg"])
        except Exception as e:
            st.error(f"Erro ao salvar despesa fixa: {e}")


# =========================
# DIALOG EDITAR — DESPESA FIXA
# =========================
@st.dialog("Editar despesa fixa", dismissible=True, on_dismiss=fechar_formulario_editar_despesa_fixa)
def renderizar_formulario_editar_despesa_fixa():
    df = st.session_state.df_despesas_fixas.sort_values(by=["ID"]).reset_index(drop=True)
    categorias = st.session_state.categorias_despesa

    if df.empty:
        st.warning("Nenhuma despesa fixa cadastrada.")
        return

    ids = df["ID"].tolist()

    despesa_id = st.selectbox(
        "Despesa fixa (ID)",
        options=[None] + ids,
        format_func=lambda x: "Selecione uma despesa" if x is None else f"ID {x}",
        key="fixa_despesa_select",
    )

    if despesa_id:
        despesa = df[df["ID"] == despesa_id].iloc[0]

        descricao = st.text_input("Descrição", value=despesa["Descrição"], key="fixa_descricao_input")
        categoria = st.selectbox(
            "Categoria",
            categorias,
            index=categorias.index(despesa["Categoria"]),
            key="fixa_categoria_input",
        )
        valor = st.number_input("Valor", value=float(despesa["Valor"]), key="fixa_valor_input")
        data = st.date_input("Data", value=despesa["Data"], key="fixa_data_input")
        vencimento = st.date_input("Vencimento", value=despesa["Vencimento"], key="fixa_vencimento_input")

        col_editar, col_cancelar = st.columns(2)

        if col_editar.button("Salvar alterações", width="stretch", key="fixa_edit_salvar"):
            atualizar_despesa_fixa(despesa_id, descricao, categoria, Decimal(str(valor)), data)
            refresh_despesas_fixas()
            fechar_formulario_editar_despesa_fixa()
            st.success("Despesa fixa atualizada com sucesso.")
            st.rerun()

        if col_cancelar.button("Cancelar", width="stretch", key="fixa_edit_cancelar"):
            fechar_formulario_editar_despesa_fixa()
            st.rerun()

        if st.button("Excluir despesa fixa", width="stretch", type="primary", key="fixa_edit_excluir"):
            excluir_despesa_fixa(despesa_id)
            refresh_despesas_fixas()
            fechar_formulario_editar_despesa_fixa()
            st.success("Despesa fixa excluída com sucesso.")
            st.rerun()


# =========================
# DIALOG ADICIONAR — DESPESA PARCELADA
# =========================
@st.dialog("Adicionar nova despesa parcelada", dismissible=True, on_dismiss=fechar_formulario_adicionar_despesa_parcelada)
def renderizar_formulario_adicionar_despesa_parcelada():
    categorias = st.session_state.categorias_despesa

    if not categorias:
        st.warning("Nenhuma categoria cadastrada.")
        return

    descricao = st.text_input("Descrição", key="parc_descricao_input")
    categoria = st.selectbox("Categoria", options=categorias, key="parc_categoria_input")

    col1, col2 = st.columns(2)
    qtd_parcelas = col1.number_input("Qtd. de parcelas", min_value=1, step=1, key="parc_qtd_parcelas_input")
    parcela_atual = col2.number_input("Parcela atual", min_value=1, step=1, key="parc_parcela_atual_input")

    col3, col4 = st.columns(2)
    valor_total = col3.number_input("Valor total", min_value=0.01, step=0.01, format="%.2f", key="parc_valor_total_input")
    valor_parcela = col4.number_input("Valor da parcela", min_value=0.01, step=0.01, format="%.2f", key="parc_valor_parcela_input")

    data = st.date_input("Data", value=None, key="parc_data_input")
    vencimento = st.date_input("Vencimento", value=None, key="parc_vencimento_input")

    col_confirmar, col_cancelar = st.columns(2)

    if col_cancelar.button("Cancelar", width="stretch", key="parc_add_cancelar"):
        fechar_formulario_adicionar_despesa_parcelada()
        st.rerun()

    if col_confirmar.button("Confirmar", width="stretch", key="parc_add_confirmar"):
        try:
            despesa = DespesaParceladaCreate(
                data=data,
                vencimento=vencimento,
                descricao=descricao,
                categoria=categoria,
                valor_total=Decimal(str(valor_total)),
                valor_parcela=Decimal(str(valor_parcela)),
                qtd_parcelas=int(qtd_parcelas),
                parcela_atual=int(parcela_atual),
            )

            inserir_despesa_parcelada(despesa)
            refresh_despesas_parceladas()
            fechar_formulario_adicionar_despesa_parcelada()

            st.success("Despesa parcelada adicionada com sucesso.")
            st.rerun()

        except ValidationError as e:
            for erro in e.errors():
                st.error(erro["msg"])
        except Exception as e:
            st.error(f"Erro ao salvar despesa parcelada: {e}")


# =========================
# DIALOG EDITAR — DESPESA PARCELADA
# =========================
@st.dialog("Editar despesa parcelada", dismissible=True, on_dismiss=fechar_formulario_editar_despesa_parcelada)
def renderizar_formulario_editar_despesa_parcelada():
    df = st.session_state.df_despesas_parceladas.sort_values(by=["ID"]).reset_index(drop=True)
    categorias = st.session_state.categorias_despesa

    if df.empty:
        st.warning("Nenhuma despesa parcelada cadastrada.")
        return

    ids = df["ID"].tolist()

    despesa_id = st.selectbox(
        "Despesa parcelada (ID)",
        options=[None] + ids,
        format_func=lambda x: "Selecione uma despesa" if x is None else f"ID {x}",
        key="parc_despesa_select",
    )

    if despesa_id:
        despesa = df[df["ID"] == despesa_id].iloc[0]

        descricao = st.text_input("Descrição", value=despesa["Descrição"], key="parc_descricao_input")
        categoria = st.selectbox(
            "Categoria",
            categorias,
            index=categorias.index(despesa["Categoria"]),
            key="parc_categoria_input",
        )

        col1, col2 = st.columns(2)
        qtd_parcelas = col1.number_input(
            "Qtd. de parcelas",
            min_value=1,
            step=1,
            value=int(despesa["Qtd. Parcelas"]),
            key="parc_qtd_parcelas_input",
        )
        parcela_atual = col2.number_input(
            "Parcela atual",
            min_value=1,
            step=1,
            value=int(despesa["Parcela Atual"]),
            key="parc_parcela_atual_input",
        )

        col3, col4 = st.columns(2)
        valor_total = col3.number_input(
            "Valor total",
            min_value=0.01,
            step=0.01,
            format="%.2f",
            value=float(despesa["Valor Total"]),
            key="parc_valor_total_input",
        )
        valor_parcela = col4.number_input(
            "Valor da parcela",
            min_value=0.01,
            step=0.01,
            format="%.2f",
            value=float(despesa["Valor Parcela"]),
            key="parc_valor_parcela_input",
        )

        data = st.date_input("Data", value=despesa["Data"], key="parc_data_input")
        vencimento = st.date_input("Vencimento", value=despesa["Vencimento"], key="parc_vencimento_input")

        col_editar, col_cancelar = st.columns(2)

        if col_editar.button("Salvar alterações", width="stretch", key="parc_edit_salvar"):
            atualizar_despesa_parcelada(
                despesa_id,
                descricao,
                categoria,
                Decimal(str(valor_total)),
                Decimal(str(valor_parcela)),
                int(qtd_parcelas),
                int(parcela_atual),
                data,
                vencimento,
            )
            refresh_despesas_parceladas()
            fechar_formulario_editar_despesa_parcelada()
            st.success("Despesa parcelada atualizada com sucesso.")
            st.rerun()

        if col_cancelar.button("Cancelar", width="stretch", key="parc_edit_cancelar"):
            fechar_formulario_editar_despesa_parcelada()
            st.rerun()

        if st.button("Excluir despesa parcelada", width="stretch", type="primary", key="parc_edit_excluir"):
            excluir_despesa_parcelada(despesa_id)
            refresh_despesas_parceladas()
            fechar_formulario_editar_despesa_parcelada()
            st.success("Despesa parcelada excluída com sucesso.")
            st.rerun()


# =========================
# COLUNAS
# =========================
def carregar_coluna_esquerda(col):
    col.markdown("## Despesas fixas")

    df_filtrado = aplicar_filtros_fixas(st.session_state.df_despesas_fixas, col)

    col.dataframe(df_filtrado, hide_index=True, width="stretch")

    col_adicionar, col_editar = col.columns(2)
    carregar_botao_adicionar_despesa_fixa(col_adicionar)
    carregar_botao_editar_despesa_fixa(col_editar)

    if st.session_state.mostrar_form_adicionar_despesa_fixa:
        renderizar_formulario_adicionar_despesa_fixa()

    if st.session_state.mostrar_form_editar_despesa_fixa:
        renderizar_formulario_editar_despesa_fixa()


def carregar_coluna_direita(col):
    col.markdown("## Despesas parceladas")

    df_filtrado = aplicar_filtros_parceladas(st.session_state.df_despesas_parceladas, col)

    col.dataframe(df_filtrado, hide_index=True, width="stretch")

    col_adicionar, col_editar = col.columns(2)
    carregar_botao_adicionar_despesa_parcelada(col_adicionar)
    carregar_botao_editar_despesa_parcelada(col_editar)

    if st.session_state.mostrar_form_adicionar_despesa_parcelada:
        renderizar_formulario_adicionar_despesa_parcelada()

    if st.session_state.mostrar_form_editar_despesa_parcelada:
        renderizar_formulario_editar_despesa_parcelada()


# =========================
# PÁGINA
# =========================
def renderizar_pagina():
    inicializar_estados()

    st.title("Despesas")

    coluna_esquerda, coluna_direita = st.columns(2)

    carregar_coluna_esquerda(coluna_esquerda)
    carregar_coluna_direita(coluna_direita)
