import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 Analytics")
st.write("Dashboard de análise de dados")

# Gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("Vendas por Categoria")
    data = pd.DataFrame({
        'Categoria': ['A', 'B', 'C', 'D'],
        'Vendas': [100, 80, 120, 90]
    })
    st.bar_chart(data.set_index('Categoria'))

with col2:
    st.subheader("Crescimento Mensal")
    growth_data = pd.DataFrame(
        np.random.randn(12, 1).cumsum(),
        columns=['Crescimento']
    )
    st.line_chart(growth_data)