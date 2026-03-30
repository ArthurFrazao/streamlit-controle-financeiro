from resumo import renderizar_pagina as renderizar_pagina_resumo
from despesas import renderizar_pagina as renderizar_pagina_despesas
from categorias import renderizar_pagina as renderizar_pagina_categorias
from cartoes import renderizar_pagina as renderizar_pagina_cartoes
from lancamentos import renderizar_pagina as renderizar_pagina_lancamentos
import streamlit as st


def carregar_pagina(nome_pagina: str):
    paginas = {
        "Resumo": renderizar_pagina_resumo,
        "Lançamentos": renderizar_pagina_lancamentos,
        "Despesas": renderizar_pagina_despesas,
        "Categorias": renderizar_pagina_categorias,
        "Cartões": renderizar_pagina_cartoes
    }

    pagina = paginas.get(nome_pagina)

    if pagina is None:
        st.error("Página não encontrada.")
        return

    pagina()
