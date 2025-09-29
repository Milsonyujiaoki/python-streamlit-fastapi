import streamlit as st

# Configurar página
st.set_page_config(
    page_title="Sistema Multipáginas",
    page_icon="🚀",
    layout="wide"
)

# Criar páginas
home_page = st.Page("pages/home.py", title="Home", icon="🏠")
analytics_page = st.Page("pages/analytics.py", title="Analytics", icon="📊")
settings_page = st.Page("pages/settings.py", title="Configurações", icon="⚙️")

# Navegação
pg = st.navigation([home_page, analytics_page, settings_page])

# Executar página selecionada
pg.run()