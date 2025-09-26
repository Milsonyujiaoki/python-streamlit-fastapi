"""
Exemplo de como criar um novo módulo para a aplicação

Este arquivo demonstra como criar um módulo simples que pode ser
facilmente integrado à aplicação principal.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any
from core.base import BaseModule, UIComponents

class ExampleModule(BaseModule):
    """Módulo de exemplo - Template para novos módulos"""
    
    def __init__(self):
        super().__init__(
            name="Módulo de Exemplo",
            icon="🚀",
            description="Este é um exemplo de como criar novos módulos"
        )
    
    def render(self) -> None:
        """Renderiza o módulo de exemplo"""
        self.show_header()
        
        # Exemplo de abas
        tab_configs = [
            {'name': '🎯 Funcionalidade 1', 'key': 'func1'},
            {'name': '📊 Funcionalidade 2', 'key': 'func2'},
            {'name': '⚙️ Configurações', 'key': 'config'}
        ]
        
        tabs = UIComponents.tabs(tab_configs)
        
        # Aba 1: Entrada de dados
        with tabs['func1']['tab']:
            st.subheader("🎯 Entrada de Dados")
            
            # Formulário de exemplo
            with st.form("exemplo_form"):
                nome = st.text_input("Nome:", placeholder="Digite seu nome")
                idade = st.number_input("Idade:", min_value=0, max_value=120, value=25)
                opcoes = st.selectbox("Escolha uma opção:", ["Opção 1", "Opção 2", "Opção 3"])
                
                if st.form_submit_button("🚀 Processar Dados", width="stretch"):
                    if nome:
                        self._process_example_data(nome, idade, opcoes)
                    else:
                        self.show_warning("Por favor, digite um nome")
        
        # Aba 2: Visualização
        with tabs['func2']['tab']:
            st.subheader("📊 Visualização de Dados")
            
            # Exemplo de DataFrame
            sample_data = self._get_sample_dataframe()
            
            st.write("**Dados de exemplo:**")
            edited_data = UIComponents.data_editor(
                sample_data,
                key="example_editor"
            )
            
            # Botões de ação
            buttons_config = [
                {'label': '💾 Salvar', 'key': 'save'},
                {'label': '📥 Exportar', 'key': 'export'},
                {'label': '🔄 Atualizar', 'key': 'refresh'}
            ]
            
            button_states = UIComponents.action_buttons(buttons_config)
            
            if button_states['save']:
                st.session_state['example_data'] = edited_data.to_dict('records')
                self.show_success("Dados salvos!")
            
            if button_states['export']:
                csv = edited_data.to_csv(index=False)
                st.download_button(
                    "📥 Baixar CSV",
                    csv,
                    "dados_exemplo.csv",
                    "text/csv",
                    width="stretch"
                )
            
            if button_states['refresh']:
                st.rerun()
        
        # Aba 3: Configurações
        with tabs['config']['tab']:
            st.subheader("⚙️ Configurações do Módulo")
            
            # Configurações de exemplo
            col1, col2 = st.columns(2)
            
            with col1:
                debug_mode = st.checkbox("🐛 Modo Debug", value=False)
                max_items = st.slider("📊 Máximo de itens:", 10, 100, 50)
            
            with col2:
                theme = st.selectbox("🎨 Tema:", ["Claro", "Escuro", "Auto"])
                language = st.selectbox("🌐 Idioma:", ["Português", "English", "Español"])
            
            if st.button("💾 Salvar Configurações", width="stretch"):
                config = {
                    'debug_mode': debug_mode,
                    'max_items': max_items,
                    'theme': theme,
                    'language': language
                }
                st.session_state['example_config'] = config
                self.show_success("Configurações salvas!")
                
                # Mostrar configurações salvas
                with st.expander("👀 Configurações Atuais"):
                    st.json(config)
    
    def _process_example_data(self, nome: str, idade: int, opcoes: str) -> None:
        """Processa dados de exemplo"""
        # Simular processamento
        with st.spinner("🔄 Processando..."):
            import time
            time.sleep(1)  # Simular tempo de processamento
        
        # Exibir resultado
        result = {
            'nome': nome,
            'idade': idade,
            'opcao_escolhida': opcoes,
            'categoria': 'Jovem' if idade < 30 else 'Adulto' if idade < 60 else 'Sênior'
        }
        
        self.show_success("Dados processados com sucesso!")
        
        # Mostrar resultado em colunas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👤 Nome", nome)
        with col2:
            st.metric("🎂 Idade", f"{idade} anos")
        with col3:
            st.metric("📋 Opção", opcoes)
        with col4:
            st.metric("🏷️ Categoria", result['categoria'])
        
        # Salvar no session state
        if 'example_results' not in st.session_state:
            st.session_state['example_results'] = []
        
        st.session_state['example_results'].append(result)
        
        # Mostrar histórico
        if st.session_state['example_results']:
            with st.expander(f"📈 Histórico ({len(st.session_state['example_results'])} registros)"):
                df_historico = pd.DataFrame(st.session_state['example_results'])
                st.dataframe(df_historico, width=700)
    
    def _get_sample_dataframe(self) -> pd.DataFrame:
        """Retorna DataFrame de exemplo"""
        return pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'Nome': ['João', 'Maria', 'Pedro', 'Ana', 'Carlos'],
            'Valor': [100.50, 250.30, 180.75, 300.00, 150.25],
            'Status': ['Ativo', 'Inativo', 'Ativo', 'Pendente', 'Ativo'],
            'Data': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
        })

# Para adicionar este módulo à aplicação principal:
# 
# 1. Importe no arquivo modules/__init__.py:
#    from .example import ExampleModule
#    __all__ = ['SocietaryModule', 'LyricsModule', 'ExampleModule']
#
# 2. Registre no app.py:
#    app.register_module(ExampleModule())
#
# 3. Pronto! O módulo estará disponível na sidebar.