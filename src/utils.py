from resumo import renderizar_pagina as renderizar_pagina_resumo
from despesas import renderizar_pagina as renderizar_pagina_despesas
from categorias import renderizar_pagina as renderizar_pagina_categorias
import streamlit as st

def carregar_pagina(nome_pagina: str):
    paginas = {
        "Resumo": renderizar_pagina_resumo,
        "Despesas": renderizar_pagina_despesas,
        "Categorias": renderizar_pagina_categorias
    }

    pagina = paginas.get(nome_pagina)

    if pagina is None:
        st.error("Página não encontrada.")
        return

    pagina()