import streamlit as st

st.title("⚙️ Configurações")
st.write("Configure suas preferências")

# Configurações
with st.form("settings_form"):
    theme = st.selectbox("Tema", ["Claro", "Escuro"])
    notifications = st.checkbox("Notificações")
    auto_save = st.checkbox("Salvamento Automático")
    
    if st.form_submit_button("Salvar"):
        st.success("Configurações salvas!")
        st.balloons()