from decimal import Decimal
import streamlit as st
from pydantic import ValidationError

from src.repositories.cartoes_repository import (
    listar_cartoes,
    inserir_cartao,
    excluir_cartao,
    atualizar_cartao
)
from src.schemas.cartao_schema import CartaoCreate


# =========================
# KEYS DOS FORMULÁRIOS
# =========================
KEYS_FORM_CARTAO = (
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
    if "df_cartoes" not in st.session_state:
        st.session_state.df_cartoes = listar_cartoes()

    if "cartoes" not in st.session_state:
        st.session_state.cartoes = listar_cartoes()

    if "mostrar_form_adicionar_cartao" not in st.session_state:
        st.session_state.mostrar_form_adicionar_cartao = False

    if "mostrar_form_editar_cartao" not in st.session_state:
        st.session_state.mostrar_form_editar_cartao = False


def refresh_cartoes():
    st.session_state.df_cartoes = listar_cartoes()


# =========================
# CONTROLE DOS DIALOGS — CARTAO
# =========================
def abrir_formulario_adicionar_cartao():
    reset_keys(*KEYS_FORM_CARTAO)
    st.session_state.mostrar_form_adicionar_cartao = True

def abrir_formulario_editar_cartao():
    reset_keys(*KEYS_FORM_CARTAO, "parc_despesa_select")
    st.session_state.mostrar_form_editar_cartao = True

# =========================
# BOTÕES — CARTAO
# =========================
def fechar_formulario_adicionar_cartao():
    st.session_state.mostrar_form_adicionar_cartao = False
    reset_keys(*KEYS_FORM_CARTAO)


def fechar_formulario_editar_cartao():
    st.session_state.mostrar_form_editar_cartao = False
    reset_keys(*KEYS_FORM_CARTAO)


def carregar_botao_adicionar_cartao(col):
    if col.button("Adicionar novo cartão", width="stretch"):
        st.session_state.cartoes = listar_cartoes()
        abrir_formulario_adicionar_cartao()


def carregar_botao_editar_cartao(col):
    if col.button("Editar cartão", width="stretch"):
        st.session_state.cartoes = listar_cartoes()
        abrir_formulario_editar_cartao()


# =========================
# DIALOG ADICIONAR — CARTAO
# =========================
@st.dialog("Adicionar novo cartão", dismissible=True, on_dismiss=fechar_formulario_adicionar_cartao)
def renderizar_formulario_adicionar_cartao():
    nome = st.text_input("Nome", key="fixa_nome_input", placeholder="Nome do cartão")
    vencimento = st.number_input("Vencimento", min_value=1, step=1, key="fixa_vencimento_input")
    limite = st.number_input("Limite", min_value=0.01, step=0.01, format="%.2f", key="fixa_limite_input")
    tipo = st.selectbox("Tipo", options=["débito", "crédito"], key="fixa_tipo_input", index=None, placeholder="Selecione o tipo")

    col_confirmar, col_cancelar = st.columns(2)

    if col_cancelar.button("Cancelar", width="stretch", key="fixa_add_cancelar"):
        fechar_formulario_adicionar_cartao()
        st.rerun()

    if col_confirmar.button("Confirmar", width="stretch", key="fixa_add_confirmar"):
        try:
            cartao = CartaoCreate(
                nome=nome,
                vencimento=vencimento,
                limite=Decimal(str(limite)),
                tipo=tipo,
            )

            inserir_cartao(cartao)
            refresh_cartoes()
            fechar_formulario_adicionar_cartao()

            st.success("Cartão adicionado com sucesso.")
            st.rerun()

        except ValidationError as e:
            for erro in e.errors():
                st.error(erro["msg"])
        except Exception as e:
            st.error(f"Erro ao salvar cartão: {e}")


# =========================
# DIALOG EDITAR — CARTAO
# =========================
@st.dialog("Editar cartão", dismissible=True, on_dismiss=fechar_formulario_editar_cartao)
def renderizar_formulario_editar_cartao():
    df = st.session_state.df_cartoes.sort_values(by=["ID"]).reset_index(drop=True)

    if df.empty:
        st.warning("Nenhuma cartão cadastrado.")
        return

    ids = df["ID"].tolist()

    cartao_id = st.selectbox(
        "Cartão (ID)",
        options=[None] + ids,
        format_func=lambda x: "Selecione um cartão" if x is None else f"ID {x}",
        key="fixa_cartao_select",
    )

    if cartao_id:
        cartao = df[df["ID"] == cartao_id].iloc[0]

        opcoes_tipo = ["débito", "crédito"]
        nome = st.text_input("Nome", value=cartao["Nome"], key="fixa_nome_input", placeholder="Nome do cartão")
        vencimento = st.number_input("Vencimento", value=cartao["Vencimento"], key="fixa_vencimento_input")
        limite = st.number_input("Limite", value=float(cartao["Limite"]), key="fixa_valor_input")
        tipo = st.selectbox(
            "Tipo",
            options=opcoes_tipo,
            index=opcoes_tipo.index(cartao["Tipo"]),
            key="fixa_tipo_input",
        )

        col_editar, col_cancelar = st.columns(2)

        if col_editar.button("Salvar alterações", width="stretch", key="fixa_edit_salvar"):
            atualizar_cartao(cartao_id, nome, vencimento, Decimal(str(limite)), tipo)
            refresh_cartoes()
            fechar_formulario_editar_cartao()
            st.success("Cartão atualizado com sucesso.")
            st.rerun()

        if col_cancelar.button("Cancelar", width="stretch", key="fixa_edit_cancelar"):
            fechar_formulario_editar_cartao()
            st.rerun()

        if st.button("Excluir cartão", width="stretch", type="primary", key="fixa_edit_excluir"):
            excluir_cartao(cartao_id)
            refresh_cartoes()
            fechar_formulario_editar_cartao()
            st.success("Cartão excluído com sucesso.")
            st.rerun()


def carregar_pagina():
    st.dataframe(
        st.session_state.df_cartoes,
        hide_index=True,
        width="stretch",
    )

    col_adicionar, col_editar = st.columns(2)
    carregar_botao_adicionar_cartao(col_adicionar)
    carregar_botao_editar_cartao(col_editar)

    if st.session_state.mostrar_form_adicionar_cartao:
        renderizar_formulario_adicionar_cartao()

    if st.session_state.mostrar_form_editar_cartao:
        renderizar_formulario_editar_cartao()


def renderizar_pagina():
    inicializar_estados()
    st.title("Cartões")
    st.write("Cadastre e gerencie seus cartões de crédito e débito para controlar limites e datas de vencimento.")
    carregar_pagina()
