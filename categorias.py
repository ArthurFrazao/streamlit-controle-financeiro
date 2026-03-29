from decimal import Decimal
import streamlit as st
from pydantic import ValidationError

from src.repositories.categorias_repository import (
    listar_categorias,
    inserir_categoria,
)
from src.schemas.categoria_schema import CategoriaCreate


def inicializar_estados():
    if "df_categorias" not in st.session_state:
        st.session_state.df_categorias = listar_categorias()

    if "mostrar_form_categoria" not in st.session_state:
        st.session_state.mostrar_form_categoria = False


def refresh_categorias():
    st.session_state.df_categorias = listar_categorias()


def abrir_formulario_categoria():
    st.session_state.mostrar_form_categoria = True


def fechar_formulario_categoria():
    st.session_state.mostrar_form_categoria = False


def carregar_botao_adicionar_categoria():
    if st.button("Adicionar nova categoria", width="stretch"):
        abrir_formulario_categoria()


def renderizar_formulario_categoria():
    with st.container():
        st.markdown("### Nova categoria")

        with st.form("form_nova_categoria", clear_on_submit=True):
            categoria = st.text_input("Categoria")

            orcamento_mensal = st.number_input(
                "Orçamento mensal (opcional)",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                value=0.0,
            )

            essencial = st.checkbox("Essencial")

            col_confirmar, col_cancelar = st.columns(2)
            confirmar = col_confirmar.form_submit_button("Confirmar", width="stretch")
            cancelar = col_cancelar.form_submit_button("Cancelar", width="stretch")

        if cancelar:
            fechar_formulario_categoria()
            st.rerun()

        if confirmar:
            try:
                nova_categoria = CategoriaCreate(
                    categoria=categoria,
                    orcamento_mensal=Decimal(str(orcamento_mensal)) if orcamento_mensal > 0 else None,
                    essencial=essencial,
                )

                inserir_categoria(nova_categoria)
                refresh_categorias()
                fechar_formulario_categoria()
                st.success("Categoria adicionada com sucesso.")
                st.rerun()

            except ValidationError as e:
                for erro in e.errors():
                    st.error(erro["msg"])
            except Exception as e:
                st.error(f"Erro ao salvar categoria: {e}")


def carregar_pagina():
    st.dataframe(
        st.session_state.df_categorias,
        hide_index=True,
        width="stretch",
    )

    carregar_botao_adicionar_categoria()

    if st.session_state.mostrar_form_categoria:
        renderizar_formulario_categoria()


def renderizar_pagina():
    inicializar_estados()
    st.title("Categorias")
    carregar_pagina()
