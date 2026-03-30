from decimal import Decimal
import streamlit as st
import pandas as pd
from pydantic import ValidationError
from src.repositories.lancamentos_repository import (
    listar_lancamentos,
    inserir_lancamento,
    atualizar_lancamento,
    excluir_lancamento
)
from src.repositories.categorias_repository import listar_nomes_categorias
from src.repositories.cartoes_repository import listar_nomes_cartoes
from src.repositories.formas_repository import listar_formas
from src.schemas.lancamento_schema import LancamentoCreate

# =========================
# KEYS DOS FORMULÁRIOS
# =========================
KEYS_FORM_LANCAMENTO = (
    "lanc_tipo_input",
    "lanc_data_input",
    "lanc_descricao_input",
    "lanc_categoria_input",
    "lanc_valor_input",
    "lanc_forma_input",
    "lanc_cartao_input",
    "lanc_observacoes_input",
    "lanc_recorrente_input",
    "lanc_status_input",
)


def reset_keys(*keys):
    for key in keys:
        st.session_state.pop(key, None)


def safe_index(lista, valor, default=0):
    return lista.index(valor) if valor and valor in lista else default


def filtra_dataframe(dataframe, data_inicio, data_fim, tipo, categoria, status) -> pd.DataFrame:
    df_filtrado = dataframe.copy()

    if data_inicio:
        df_filtrado = df_filtrado[df_filtrado["Data"] >= data_inicio]
    if data_fim:
        df_filtrado = df_filtrado[df_filtrado["Data"] <= data_fim]
    if tipo != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo]
    if categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria]
    if status != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Status"] == status]

    return df_filtrado


# =========================
# ESTADOS
# =========================
def inicializar_estados():
    if "df_lancamentos" not in st.session_state:
        st.session_state.df_lancamentos = listar_lancamentos()

    if "mostrar_form_adicionar_lancamento" not in st.session_state:
        st.session_state.mostrar_form_adicionar_lancamento = False

    if "mostrar_form_editar_lancamento" not in st.session_state:
        st.session_state.mostrar_form_editar_lancamento = False

    if "categorias_lancamento" not in st.session_state:
        st.session_state.categorias_lancamento = listar_nomes_categorias()

    if "cartoes_lancamento" not in st.session_state:
        st.session_state.cartoes_lancamento = listar_nomes_cartoes()

    if "formas_lancamento" not in st.session_state:
        st.session_state.formas_lancamento = listar_formas()

    if "filtro_reset_counter_lancamento" not in st.session_state:
        st.session_state.filtro_reset_counter_lancamento = 0


def refresh_lancamentos():
    st.session_state.df_lancamentos = listar_lancamentos()


# =========================
# FILTROS
# =========================
def aplicar_filtros_lancamentos(df, col):
    counter = st.session_state.filtro_reset_counter_lancamento

    with col.expander("🔍 Filtros", expanded=False):
        col1, col2, col3, col4 = st.columns(4)

        data_inicio = col1.date_input(
            "Data inicial", value=None, key=f"lanc_filtro_data_inicio_{counter}"
        )
        data_fim = col2.date_input(
            "Data final", value=None, key=f"lanc_filtro_data_fim_{counter}"
        )

        tipos = ["Todos", "receita", "despesa"]
        tipo = col3.selectbox(
            "Tipo", tipos, key=f"lanc_filtro_tipo_{counter}"
        )

        categorias = ["Todas"] + st.session_state.categorias_lancamento
        categoria = col4.selectbox(
            "Categoria", categorias, key=f"lanc_filtro_categoria_{counter}"
        )

        col5, col6 = st.columns(2)

        status_opcoes = ["Todos", "confirmado", "pendente", "cancelado"]
        status = col5.selectbox(
            "Status", status_opcoes, key=f"lanc_filtro_status_{counter}"
        )

        if col6.button("Limpar filtros", use_container_width=True, key="lanc_limpar_filtros"):
            st.session_state.filtro_reset_counter_lancamento += 1
            st.rerun()

    df_filtrado = filtra_dataframe(df, data_inicio, data_fim, tipo, categoria, status)

    return df_filtrado


# =========================
# CONTROLE DOS DIALOGS — LANCAMENTO
# =========================
def abrir_formulario_adicionar_lancamento():
    reset_keys(*KEYS_FORM_LANCAMENTO)
    st.session_state.categorias_lancamento = listar_nomes_categorias()
    st.session_state.cartoes_lancamento = listar_nomes_cartoes()
    st.session_state.formas_lancamento = listar_formas()
    st.session_state.mostrar_form_adicionar_lancamento = True


def abrir_formulario_editar_lancamento():
    reset_keys(*KEYS_FORM_LANCAMENTO, "lancamento_select")
    st.session_state.categorias_lancamento = listar_nomes_categorias()
    st.session_state.cartoes_lancamento = listar_nomes_cartoes()
    st.session_state.formas_lancamento = listar_formas()
    st.session_state.mostrar_form_editar_lancamento = True


def fechar_formulario_adicionar_lancamento():
    st.session_state.mostrar_form_adicionar_lancamento = False
    reset_keys(*KEYS_FORM_LANCAMENTO)


def fechar_formulario_editar_lancamento():
    st.session_state.mostrar_form_editar_lancamento = False
    reset_keys(*KEYS_FORM_LANCAMENTO, "lancamento_select")


# =========================
# BOTÕES — LANCAMENTO
# =========================
def carregar_botao_adicionar_lancamento(col):
    if col.button("Adicionar novo lançamento", width="stretch"):
        abrir_formulario_adicionar_lancamento()


def carregar_botao_editar_lancamento(col):
    if col.button("Editar lançamento", width="stretch"):
        abrir_formulario_editar_lancamento()


# =========================
# DIALOG ADICIONAR — LANCAMENTO
# =========================
@st.dialog("Adicionar novo lançamento", dismissible=True, on_dismiss=fechar_formulario_adicionar_lancamento)
def renderizar_formulario_adicionar_lancamento():
    categorias = st.session_state.categorias_lancamento
    cartoes = st.session_state.cartoes_lancamento
    formas = st.session_state.formas_lancamento

    # Tipo (Receita ou Despesa)
    tipo = st.radio("Tipo", options=["receita", "despesa"], key="lanc_tipo_input", horizontal=True)

    # Data e Descrição
    col1, col2 = st.columns(2)
    data = col1.date_input("Data", value=None, key="lanc_data_input")
    descricao = col2.text_input("Descrição", key="lanc_descricao_input", placeholder="Descrição do lançamento")

    # Categoria e Valor
    col3, col4 = st.columns(2)
    categoria = col3.selectbox(
        "Categoria",
        options=categorias,
        key="lanc_categoria_input",
        index=None,
        placeholder="Selecione a categoria"
    )
    valor = col4.number_input("Valor", min_value=0.01, step=0.01, format="%.2f", key="lanc_valor_input")

    # Forma de Pagamento e Cartão
    col5, col6 = st.columns(2)
    forma = col5.selectbox(
        "Forma de Pagamento",
        options=formas,
        key="lanc_forma_input",
        index=None,
        placeholder="Selecione a forma"
    )

    # Bloquear cartão se forma for PIX
    if len(cartoes) > 0:
        cartao_desabilitado = forma == "PIX"
        cartao = col6.selectbox(
            "Cartão",
            options=cartoes,
            key="lanc_cartao_input",
            index=None,
            placeholder="Não aplicável" if cartao_desabilitado else "Selecione o cartão",
            disabled=cartao_desabilitado
        )
        if cartao_desabilitado:
            cartao = None
    else:
        col6.warning("Nenhum cartão cadastrado")
        cartao = None

    # Observações
    observacoes = st.text_area(
        "Observações (opcional)",
        key="lanc_observacoes_input",
        placeholder="Detalhes adicionais sobre o lançamento",
        max_chars=500
    )

    # Recorrente e Status
    col7, col8 = st.columns(2)
    recorrente = col7.checkbox("Lançamento recorrente (mensal)", key="lanc_recorrente_input")
    status = col8.selectbox(
        "Status",
        options=["confirmado", "pendente", "cancelado"],
        key="lanc_status_input"
    )

    col_confirmar, col_cancelar = st.columns(2)

    if col_cancelar.button("Cancelar", width="stretch", key="lanc_add_cancelar"):
        fechar_formulario_adicionar_lancamento()
        st.rerun()

    if col_confirmar.button("Confirmar", width="stretch", key="lanc_add_confirmar"):
        try:
            lancamento = LancamentoCreate(
                tipo=tipo,
                data=data,
                descricao=descricao,
                categoria=categoria,
                valor=Decimal(str(valor)),
                forma_pagamento=forma,
                cartao=cartao,
                observacoes=observacoes if observacoes else None,
                recorrente=recorrente,
                status=status
            )

            inserir_lancamento(lancamento)
            refresh_lancamentos()
            fechar_formulario_adicionar_lancamento()

            st.success("Lançamento adicionado com sucesso.")
            st.rerun()

        except ValidationError as e:
            for erro in e.errors():
                st.error(erro["msg"])
        except Exception as e:
            st.error(f"Erro ao salvar lançamento: {e}")


# =========================
# DIALOG EDITAR — LANCAMENTO
# =========================
@st.dialog("Editar lançamento", dismissible=True, on_dismiss=fechar_formulario_editar_lancamento)
def renderizar_formulario_editar_lancamento():
    df = st.session_state.df_lancamentos.sort_values(by=["ID"]).reset_index(drop=True)
    categorias = st.session_state.categorias_lancamento
    cartoes = st.session_state.cartoes_lancamento
    formas = st.session_state.formas_lancamento

    if df.empty:
        st.warning("Nenhum lançamento cadastrado.")
        return

    ids = df["ID"].tolist()

    lancamento_id = st.selectbox(
        "Lançamento (ID)",
        options=[None] + ids,
        format_func=lambda x: "Selecione um lançamento" if x is None else f"ID {x}",
        key="lancamento_select",
    )

    if lancamento_id:
        lancamento = df[df["ID"] == lancamento_id].iloc[0]

        # Tipo (Receita ou Despesa)
        tipo_opcoes = ["receita", "despesa"]
        tipo = st.radio(
            "Tipo",
            options=tipo_opcoes,
            index=tipo_opcoes.index(lancamento["Tipo"]),
            key="lanc_tipo_input",
            horizontal=True
        )

        # Data e Descrição
        col1, col2 = st.columns(2)
        data = col1.date_input("Data", value=lancamento["Data"], key="lanc_data_input")
        descricao = col2.text_input(
            "Descrição",
            value=lancamento["Descrição"],
            key="lanc_descricao_input",
            placeholder="Descrição do lançamento"
        )

        # Categoria e Valor
        col3, col4 = st.columns(2)
        categoria = col3.selectbox(
            "Categoria",
            options=categorias,
            index=safe_index(categorias, lancamento["Categoria"]),
            key="lanc_categoria_input"
        )
        valor = col4.number_input(
            "Valor",
            min_value=0.01,
            step=0.01,
            format="%.2f",
            value=float(lancamento["Valor"]),
            key="lanc_valor_input"
        )

        # Forma de Pagamento e Cartão
        col5, col6 = st.columns(2)
        forma_atual = lancamento.get("Forma de Pagamento")
        forma = col5.selectbox(
            "Forma de Pagamento",
            options=formas,
            index=safe_index(formas, forma_atual),
            key="lanc_forma_input"
        )

        # Bloquear cartão se forma for PIX
        if len(cartoes) > 0:
            cartao_atual = lancamento.get("Cartão")
            cartao_desabilitado = forma == "PIX"
            cartao = col6.selectbox(
                "Cartão",
                options=cartoes,
                index=safe_index(cartoes, cartao_atual),
                key="lanc_cartao_input",
                disabled=cartao_desabilitado
            )
            if cartao_desabilitado:
                cartao = None
        else:
            col6.warning("Nenhum cartão cadastrado")
            cartao = None

        # Observações
        obs_atual = lancamento.get("Observações")
        observacoes = st.text_area(
            "Observações (opcional)",
            value=obs_atual if obs_atual else "",
            key="lanc_observacoes_input",
            placeholder="Detalhes adicionais sobre o lançamento",
            max_chars=500
        )

        # Recorrente e Status
        col7, col8 = st.columns(2)
        recorrente_atual = lancamento.get("Recorrente", 0)
        recorrente = col7.checkbox(
            "Lançamento recorrente (mensal)",
            value=bool(recorrente_atual),
            key="lanc_recorrente_input"
        )

        status_opcoes = ["confirmado", "pendente", "cancelado"]
        status = col8.selectbox(
            "Status",
            options=status_opcoes,
            index=safe_index(status_opcoes, lancamento["Status"]),
            key="lanc_status_input"
        )

        col_editar, col_cancelar = st.columns(2)

        if col_editar.button("Salvar alterações", width="stretch", key="lanc_edit_salvar"):
            atualizar_lancamento(
                lancamento_id,
                tipo,
                data,
                descricao,
                categoria,
                Decimal(str(valor)),
                forma,
                cartao,
                observacoes if observacoes else None,
                recorrente,
                status
            )
            refresh_lancamentos()
            fechar_formulario_editar_lancamento()
            st.success("Lançamento atualizado com sucesso.")
            st.rerun()

        if col_cancelar.button("Cancelar", width="stretch", key="lanc_edit_cancelar"):
            fechar_formulario_editar_lancamento()
            st.rerun()

        if st.button("Excluir lançamento", width="stretch", type="primary", key="lanc_edit_excluir"):
            excluir_lancamento(lancamento_id)
            refresh_lancamentos()
            fechar_formulario_editar_lancamento()
            st.success("Lançamento excluído com sucesso.")
            st.rerun()


# =========================
# RESUMO FINANCEIRO
# =========================
def exibir_resumo_financeiro(df):
    if df.empty:
        st.info("Nenhum lançamento cadastrado ainda.")
        return

    # Calcular totais
    total_receitas = df[df["Tipo"] == "receita"]["Valor"].sum() if not df[df["Tipo"] == "receita"].empty else 0
    total_despesas = df[df["Tipo"] == "despesa"]["Valor"].sum() if not df[df["Tipo"] == "despesa"].empty else 0
    saldo = total_receitas - total_despesas

    # Exibir cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="💰 Receitas",
            value=f"R$ {total_receitas:,.2f}",
            delta=None
        )

    with col2:
        st.metric(
            label="💸 Despesas",
            value=f"R$ {total_despesas:,.2f}",
            delta=None
        )

    with col3:
        delta_color = "normal" if saldo >= 0 else "inverse"
        st.metric(
            label="📊 Saldo",
            value=f"R$ {saldo:,.2f}",
            delta="Positivo" if saldo >= 0 else "Negativo",
            delta_color=delta_color
        )


# =========================
# PÁGINA
# =========================
def carregar_pagina():
    df = st.session_state.df_lancamentos

    # Exibir resumo financeiro
    exibir_resumo_financeiro(df)

    st.markdown("---")

    # Aplicar filtros
    df_filtrado = aplicar_filtros_lancamentos(df, st)

    # Exibir tabela
    st.dataframe(
        df_filtrado,
        hide_index=True,
        width="stretch",
    )

    # Botões de ação
    col_adicionar, col_editar = st.columns(2)
    carregar_botao_adicionar_lancamento(col_adicionar)
    carregar_botao_editar_lancamento(col_editar)

    # Renderizar formulários se necessário
    if st.session_state.mostrar_form_adicionar_lancamento:
        renderizar_formulario_adicionar_lancamento()

    if st.session_state.mostrar_form_editar_lancamento:
        renderizar_formulario_editar_lancamento()


def renderizar_pagina():
    inicializar_estados()
    st.title("Lançamentos")
    st.write(
        "Registre receitas e despesas do dia a dia - movimentações pontuais e variáveis que não se encaixam em despesas fixas ou parceladas.")
    carregar_pagina()
