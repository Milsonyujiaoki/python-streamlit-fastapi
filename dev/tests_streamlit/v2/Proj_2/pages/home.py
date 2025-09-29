import streamlit as st
import pandas as pd
import numpy as np

st.title("🏠 Home")
st.write("Esta é a página inicial do sistema multipáginas!")

# Métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Usuários", "1,234", "+12%")
with col2:
    st.metric("Vendas", "R$ 56.789", "+5%")
with col3:
    st.metric("Conversão", "3.4%", "-0.2%")

# Gráfico
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)