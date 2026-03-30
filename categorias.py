from decimal import Decimal
import streamlit as st
from pydantic import ValidationError

from src.repositories.categorias_repository import (
    listar_categorias,
    inserir_categoria,
    excluir_categoria,
    atualizar_categoria
)
from src.schemas.categoria_schema import CategoriaCreate

# =========================
# KEYS DOS FORMULÁRIOS
# =========================
KEYS_FORM_CATEGORIA = (
    "fixa_nome_input",
    "fixa_vencimento_input",
    "fixa_limite_input",
    "fixa_tipo_input",
)


def reset_keys(*keys):
    for key in keys:
        st.session_state.pop(key, None)


# =========================
# ESTADOS
# =========================
def inicializar_estados():
    if "df_categorias" not in st.session_state:
        st.session_state.df_categorias = listar_categorias()

    if "mostrar_form_adicionar_categoria" not in st.session_state:
        st.session_state.mostrar_form_adicionar_categoria = False

    if "mostrar_form_editar_categoria" not in st.session_state:
        st.session_state.mostrar_form_editar_categoria = False


def refresh_categorias():
    st.session_state.df_categorias = listar_categorias()


# =========================
# CONTROLE DOS DIALOGS — CATEGORIA
# =========================
def abrir_formulario_adicionar_categoria():
    reset_keys(*KEYS_FORM_CATEGORIA)
    st.session_state.mostrar_form_adicionar_categoria = True


def abrir_formulario_editar_categoria():
    reset_keys(*KEYS_FORM_CATEGORIA, "categoria_select")
    st.session_state.mostrar_form_editar_categoria = True


# =========================
# BOTÕES — CATEGORIA
# =========================
def fechar_formulario_adicionar_categoria():
    st.session_state.mostrar_form_adicionar_categoria = False
    reset_keys(*KEYS_FORM_CATEGORIA)


def fechar_formulario_editar_categoria():
    st.session_state.mostrar_form_editar_categoria = False
    reset_keys(*KEYS_FORM_CATEGORIA)


def carregar_botao_adicionar_categoria(col):
    if col.button("Adicionar nova categoria", width="stretch"):
        st.session_state.categorias = listar_categorias()
        abrir_formulario_adicionar_categoria()


def carregar_botao_editar_categoria(col):
    if col.button("Editar categoria", width="stretch"):
        st.session_state.categorias = listar_categorias()
        abrir_formulario_editar_categoria()


# =========================
# DIALOG ADICIONAR — CATEGORIA
# =========================
@st.dialog("Adicionar nova categoria", dismissible=True, on_dismiss=fechar_formulario_adicionar_categoria)
def renderizar_formulario_adicionar_categoria():
    categoria = st.text_input("Categoria", placeholder="Nome da categoria")
    orcamento_mensal = st.number_input(
        "Orçamento mensal (opcional)",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=0.0,
    )

    essencial = st.checkbox("Essencial")

    col_confirmar, col_cancelar = st.columns(2)

    if col_cancelar.button("Cancelar", width="stretch", key="categoria_add_cancelar"):
        fechar_formulario_adicionar_categoria()
        st.rerun()

    if col_confirmar.button("Confirmar", width="stretch", key="categoria_add_confirmar"):
        try:
            nova_categoria = CategoriaCreate(
                categoria=categoria,
                orcamento_mensal=Decimal(str(orcamento_mensal)),
                essencial=essencial,
            )
            inserir_categoria(nova_categoria)
            refresh_categorias()
            fechar_formulario_adicionar_categoria()
            st.success("Categoria adicionada com sucesso.")
            st.rerun()

        except ValidationError as e:
            for erro in e.errors():
                st.error(erro["msg"])
        except Exception as e:
            st.error(f"Erro ao salvar categoria: {e}")


# =========================
# DIALOG EDITAR — CATEGORIA
# =========================
@st.dialog("Editar categoria", dismissible=True, on_dismiss=fechar_formulario_editar_categoria)
def renderizar_formulario_editar_categoria():
    df = st.session_state.df_categorias.sort_values(by=["ID"]).reset_index(drop=True)

    if df.empty:
        st.warning("Nenhuma categoria cadastrada.")
        return

    ids = df["ID"].tolist()

    categoria_id = st.selectbox(
        "Categoria (ID)",
        options=[None] + ids,
        format_func=lambda x: "Selecione uma categoria" if x is None else f"ID {x}",
        key="categoria_select",
    )

    if categoria_id:
        categoria = df[df["ID"] == categoria_id].iloc[0]

        nome_categoria = st.text_input("Categoria", value=categoria["Categoria"], key="categoria_input",
                                       placeholder="Nome da categoria")
        orcamento_mensal = st.number_input("Orçamento Mensal", value=float(categoria["Orçamento Mensal"]))
        essencial = st.checkbox("Essencial", value=categoria["Essencial"])

        col_editar, col_cancelar = st.columns(2)

        if col_editar.button("Salvar alterações", width="stretch", key="fixa_edit_salvar"):
            atualizar_categoria(categoria_id, nome_categoria, orcamento_mensal, essencial)
            refresh_categorias()
            fechar_formulario_editar_categoria()
            st.success("Categoria atualizada com sucesso.")
            st.rerun()

        if col_cancelar.button("Cancelar", width="stretch", key="fixa_edit_cancelar"):
            fechar_formulario_editar_categoria()
            st.rerun()

        if st.button("Excluir categoria", width="stretch", type="primary", key="fixa_edit_excluir"):
            excluir_categoria(categoria_id)
            refresh_categorias()
            fechar_formulario_editar_categoria()
            st.success("Categoria excluída com sucesso.")
            st.rerun()


# =========================
# PÁGINA
# =========================
def carregar_pagina():
    st.dataframe(
        st.session_state.df_categorias,
        hide_index=True,
        width="stretch",
    )

    col_adicionar, col_editar = st.columns(2)
    carregar_botao_adicionar_categoria(col_adicionar)
    carregar_botao_editar_categoria(col_editar)

    if st.session_state.mostrar_form_adicionar_categoria:
        renderizar_formulario_adicionar_categoria()

    if st.session_state.mostrar_form_editar_categoria:
        renderizar_formulario_editar_categoria()


def renderizar_pagina():
    inicializar_estados()
    st.title("Categorias")
    st.write(
        "Organize suas despesas e receitas em categorias personalizadas, definindo orçamentos mensais e marcando as essenciais.")
    carregar_pagina()
