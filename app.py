import streamlit as st 
from streamlit_option_menu import option_menu
from src.utils import carregar_pagina
from src.database.init_db import init_db
from src.core.logging import setup_logging, get_logger

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="💰",
    layout="wide"
)

setup_logging()
logger = get_logger(__name__)

if "app_iniciada" not in st.session_state:
    logger.info("Aplicação iniciada")
    st.session_state.app_iniciada = True
    
@st.cache_resource
def setup_database():
    init_db()  

setup_database()

with st.sidebar:
    opcao_selecionada = option_menu(
        None,
        options=["Resumo", "Despesas", "Categorias"],
        icons=["justify", "cash", "info-lg"],
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "15px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"},
        }
    )

logger.info(f"Página selecionada: {opcao_selecionada}")
carregar_pagina(opcao_selecionada)