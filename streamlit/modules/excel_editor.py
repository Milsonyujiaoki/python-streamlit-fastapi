"""
Módulo de Edição de Excel
Editor completo para planilhas Excel com funcionalidades avançadas
"""

import streamlit as st
import pandas as pd
import io
from typing import Dict, List, Any, Optional
from core.base import BaseModule, UIComponents

class ExcelModule(BaseModule):
    """Módulo completo para edição e manipulação de arquivos Excel"""
    
    def __init__(self):
        super().__init__(
            name="Editor de Excel",
            icon="📊", 
            description="Editor completo para planilhas Excel com funcionalidades avançadas"
        )
    
    def render(self) -> None:
        """Renderiza o módulo completo de edição de Excel"""
        self.show_header()
        
        # Configuração de abas principais
        tab_configs = [
            {'name': '📁 Upload & Dados', 'key': 'upload'},
            {'name': '✏️ Editor Avançado', 'key': 'editor'},
            {'name': '🔄 Operações de Dados', 'key': 'operations'},
            {'name': '📊 Análise', 'key': 'analysis'},
            {'name': '⚙️ Configurações', 'key': 'config'}
        ]
        
        tabs = UIComponents.tabs(tab_configs)
        
        # Aba 1: Upload de arquivo Excel
        with tabs['upload']['tab']:
            self._render_upload_tab()
        
        # Aba 2: Editor avançado
        with tabs['editor']['tab']:
            self._render_editor_tab()
        
        # Aba 3: Operações de dados (NOVO!)
        with tabs['operations']['tab']:
            self._render_operations_tab()
        
        # Aba 4: Análise de dados
        with tabs['analysis']['tab']:
            self._render_analysis_tab()
        
        # Aba 5: Configurações
        with tabs['config']['tab']:
            self._render_config_tab()
    
    def _render_upload_tab(self) -> None:
        """Renderiza aba de upload de múltiplos arquivos Excel"""
        st.subheader("📁 Gerenciamento de Dados")
        
        # Inicializar armazenamento de múltiplas tabelas
        if 'datasets' not in st.session_state:
            st.session_state['datasets'] = {}
        
        # Sub-abas para organizar melhor
        upload_tabs = st.tabs(["📤 Upload Arquivos", "📋 Tabelas Carregadas", "🆕 Nova Tabela"])
        
        # Upload de múltiplos arquivos
        with upload_tabs[0]:
            st.subheader("📤 Upload de Múltiplos Arquivos")
            
            # Upload de múltiplos arquivos
            arquivos_excel = st.file_uploader(
                "Selecione um ou mais arquivos:",
                ['xlsx', 'xls', 'csv'],
                accept_multiple_files=True,
                help="Formatos suportados: .xlsx, .xls, .csv. Você pode selecionar múltiplos arquivos."
            )
            
            if arquivos_excel:
                for arquivo in arquivos_excel:
                    try:
                        # Processar cada arquivo
                        dataset_name = st.text_input(
                            f"Nome para a tabela '{arquivo.name}':",
                            value=arquivo.name.split('.')[0],
                            key=f"name_{arquivo.name}"
                        )
                        
                        if st.button(f"📤 Processar {arquivo.name}", key=f"process_{arquivo.name}"):
                            # Determinar tipo de arquivo e ler
                            if arquivo.name.endswith('.csv'):
                                df = pd.read_csv(arquivo)
                                sheet_info = {'sheets': ['CSV']}
                            else:
                                # Ler arquivo Excel e obter nomes das abas
                                excel_file = pd.ExcelFile(arquivo)
                                sheet_names = excel_file.sheet_names
                                
                                if len(sheet_names) > 1:
                                    # Para múltiplas sheets, vamos carregar a primeira por padrão
                                    df = pd.read_excel(arquivo, sheet_name=sheet_names[0])
                                    sheet_info = {'sheets': sheet_names, 'selected': sheet_names[0]}
                                else:
                                    df = pd.read_excel(arquivo, sheet_name=sheet_names[0])
                                    sheet_info = {'sheets': sheet_names, 'selected': sheet_names[0]}
                            
                            # Salvar dataset no session state
                            st.session_state['datasets'][dataset_name] = {
                                'data': df,
                                'original': df.copy(),
                                'filename': arquivo.name,
                                'sheet_info': sheet_info,
                                'size': arquivo.size
                            }
                            
                            # Armazenar arquivo original para permitir troca de planilhas (apenas para Excel)
                            if not arquivo.name.endswith('.csv'):
                                arquivo.seek(0)  # Voltar ao início do arquivo
                                st.session_state[f"original_file_{dataset_name}"] = arquivo.read()
                                arquivo.seek(0)  # Voltar ao início novamente
                            
                            self.show_success(f"Dataset '{dataset_name}' adicionado com sucesso!")
                            st.rerun()
                            
                    except Exception as e:
                        self.show_error(f"Erro ao processar '{arquivo.name}': {str(e)}")
        
        # Visualizar tabelas carregadas
        with upload_tabs[1]:
            st.subheader("� Tabelas Carregadas")
            
            if not st.session_state['datasets']:
                st.info("Nenhuma tabela carregada ainda. Faça upload de arquivos na aba anterior.")
            else:
                # Mostrar informações de cada dataset
                for name, dataset_info in st.session_state['datasets'].items():
                    with st.expander(f"📊 {name} ({dataset_info['filename']})"):
                        df = dataset_info['data']
                        
                        # Métricas
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("📄 Linhas", len(df))
                        with col2:
                            st.metric("📊 Colunas", len(df.columns))
                        with col3:
                            sheet_info = dataset_info.get('sheet_info', {'sheets': ['Dados']})
                            sheet_count = len(sheet_info['sheets'])
                            st.metric("📋 Planilhas", sheet_count)
                        with col4:
                            st.metric("💾 Tamanho", f"{dataset_info['size'] / 1024:.1f} KB")
                        
                        # Mostrar planilhas disponíveis se houver mais de uma
                        sheet_info = dataset_info.get('sheet_info', {'sheets': ['Dados']})
                        if len(sheet_info['sheets']) > 1:
                            st.write(f"**📋 Planilhas disponíveis:** {', '.join(sheet_info['sheets'])}")
                            current_sheet = sheet_info.get('selected', sheet_info['sheets'][0])
                            st.write(f"**📌 Planilha atual:** {current_sheet}")
                        
                        # Preview
                        st.dataframe(df.head(5))
                        
                        # Botões de ação
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"🗑️ Remover {name}", key=f"remove_{name}"):
                                del st.session_state['datasets'][name]
                                st.rerun()
                        with col2:
                            if st.button(f"✏️ Editar {name}", key=f"edit_{name}"):
                                st.session_state['current_dataset'] = name
                                st.info(f"Dataset '{name}' selecionado para edição!")
        
        # Criar nova tabela vazia
        with upload_tabs[2]:
            st.subheader("🆕 Criar Nova Tabela")
            
            # Nome da nova tabela
            new_table_name = st.text_input("Nome da nova tabela:", value="Nova_Tabela")
            
            col1, col2 = st.columns(2)
            with col1:
                rows = st.number_input("Número de linhas:", min_value=1, max_value=1000, value=10)
            with col2:
                cols = st.number_input("Número de colunas:", min_value=1, max_value=50, value=5)
            
            # Definir nomes das colunas
            st.write("**Nomes das colunas:**")
            column_names = []
            cols_per_row = 3
            for i in range(0, cols, cols_per_row):
                columns = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    col_idx = i + j
                    if col_idx < cols:
                        with columns[j]:
                            col_name = st.text_input(
                                f"Col {col_idx + 1}:",
                                value=f"Coluna_{col_idx + 1}",
                                key=f"col_name_{col_idx}"
                            )
                            column_names.append(col_name)
            
            if st.button("🆕 Criar Tabela", width="stretch"):
                if new_table_name and new_table_name not in st.session_state['datasets']:
                    # Criar DataFrame vazio
                    df = pd.DataFrame(
                        index=range(rows),
                        columns=column_names[:cols]
                    )
                    
                    # Adicionar ao datasets
                    st.session_state['datasets'][new_table_name] = {
                        'data': df,
                        'original': df.copy(),
                        'filename': f"{new_table_name}.xlsx",
                        'sheet_info': {'sheets': ['Dados'], 'selected': 'Dados'},
                        'size': 0
                    }
                    
                    self.show_success(f"Tabela '{new_table_name}' criada com sucesso!")
                    st.rerun()
                elif new_table_name in st.session_state['datasets']:
                    self.show_error(f"Já existe uma tabela com o nome '{new_table_name}'")
                else:
                    self.show_warning("Por favor, digite um nome para a tabela")
                
                self.show_success("Nova planilha criada!")
                st.rerun()
    
    def _render_editor_tab(self) -> None:
        """Renderiza aba de edição dos dados"""
        if not st.session_state['datasets']:
            st.info("📋 Faça upload de arquivos na aba 'Upload & Dados' para começar a editar.")
            return
        
        st.subheader("✏️ Editor Avançado")
        
        # Seletor de tabela para editar
        dataset_names = list(st.session_state['datasets'].keys())
        selected_dataset = st.selectbox(
            "Selecione a tabela para editar:",
            dataset_names,
            index=0,
            key="editor_dataset_selector"
        )
        
        if selected_dataset:
            dataset_info = st.session_state['datasets'][selected_dataset]
            
            # Seleção de planilha (se o arquivo Excel tiver múltiplas abas)
            sheet_info = dataset_info.get('sheet_info', {'sheets': ['Dados'], 'selected': 'Dados'})
            if len(sheet_info['sheets']) > 1:
                st.write("**Selecionar Planilha:**")
                selected_sheet = st.selectbox(
                    "Escolha a planilha:",
                    sheet_info['sheets'],
                    index=sheet_info['sheets'].index(sheet_info['selected']) if sheet_info['selected'] in sheet_info['sheets'] else 0,
                    key=f"sheet_selector_{selected_dataset}"
                )
                
                # Se mudou de planilha, recarregar os dados
                if selected_sheet != sheet_info['selected']:
                    try:
                        # Recarregar dados da planilha selecionada
                        filename = dataset_info['filename']
                        # Precisamos do arquivo original para recarregar uma planilha diferente
                        # Vamos armazenar o arquivo original no session_state quando fazer upload
                        if f"original_file_{selected_dataset}" in st.session_state:
                            file_bytes = st.session_state[f"original_file_{selected_dataset}"]
                            file_buffer = io.BytesIO(file_bytes)
                            new_df = pd.read_excel(file_buffer, sheet_name=selected_sheet)
                            
                            # Atualizar dados
                            st.session_state['datasets'][selected_dataset]['data'] = new_df
                            st.session_state['datasets'][selected_dataset]['original'] = new_df.copy()
                            st.session_state['datasets'][selected_dataset]['sheet_info']['selected'] = selected_sheet
                            
                            self.show_success(f"Planilha '{selected_sheet}' carregada!")
                            st.rerun()
                        else:
                            self.show_warning("Arquivo original não encontrado. Faça upload novamente para trocar de planilha.")
                    
                    except Exception as e:
                        self.show_error(f"Erro ao carregar planilha '{selected_sheet}': {str(e)}")
            
            df = dataset_info['data']
            current_sheet = sheet_info['selected']
            
            # Informações da tabela
            sheet_display = f" (Planilha: {current_sheet})" if len(sheet_info['sheets']) > 1 else ""
            st.info(f"📄 Editando: **{selected_dataset}**{sheet_display} ({len(df)} linhas, {len(df.columns)} colunas)")
            
            # Operações rápidas de colunas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Adicionar Coluna:**")
                new_col_name = st.text_input("Nome da nova coluna:", key=f"new_col_{selected_dataset}")
                if st.button("➕ Adicionar", key=f"add_col_{selected_dataset}"):
                    if new_col_name and new_col_name not in df.columns:
                        df[new_col_name] = ""
                        st.session_state['datasets'][selected_dataset]['data'] = df
                        self.show_success(f"Coluna '{new_col_name}' adicionada!")
                        st.rerun()
                    elif new_col_name in df.columns:
                        self.show_warning("Coluna já existe!")
            
            with col2:
                st.write("**Remover Coluna:**")
                if len(df.columns) > 0:
                    col_to_remove = st.selectbox(
                        "Selecione coluna:",
                        df.columns,
                        key=f"remove_col_selector_{selected_dataset}"
                    )
                    if st.button("🗑️ Remover", key=f"remove_col_{selected_dataset}"):
                        if col_to_remove in df.columns:
                            df = df.drop(columns=[col_to_remove])
                            st.session_state['datasets'][selected_dataset]['data'] = df
                            self.show_success(f"Coluna '{col_to_remove}' removida!")
                            st.rerun()
            
            with col3:
                st.write("**Operações:**")
                if st.button("🔄 Restaurar Original", key=f"restore_{selected_dataset}"):
                    st.session_state['datasets'][selected_dataset]['data'] = dataset_info['original'].copy()
                    self.show_success("Dados restaurados ao original!")
                    st.rerun()
            
            # Editor de dados principal
            edited_df = UIComponents.data_editor(
                df,
                key=f"excel_editor_{selected_dataset}"
            )
            
            # Atualizar dados no session state
            st.session_state['datasets'][selected_dataset]['data'] = edited_df
            
            # Botões de ação
            st.markdown("---")
            buttons_config = [
                {'label': '💾 Salvar', 'key': f'save_{selected_dataset}'},
                {'label': '📥 Download Excel', 'key': f'download_excel_{selected_dataset}'},
                {'label': '📄 Download CSV', 'key': f'download_csv_{selected_dataset}'}
            ]
            
            button_states = UIComponents.action_buttons(buttons_config, columns=3)
            
            if button_states[f'save_{selected_dataset}']:
                self.show_success("✅ Alterações salvas na sessão!")
            
            if button_states[f'download_excel_{selected_dataset}']:
                filename = dataset_info['filename']
                self._download_excel(edited_df, filename)
            
            if button_states[f'download_csv_{selected_dataset}']:
                filename = dataset_info['filename']
                csv_data = edited_df.to_csv(index=False)
                st.download_button(
                    "📄 Baixar CSV",
                    csv_data,
                    filename.replace('.xlsx', '.csv').replace('.xls', '.csv'),
                    "text/csv",
                    key=f"csv_download_{selected_dataset}"
                )
    
    def _get_dataset_with_sheet_selection(self, key_prefix: str, label: str = "Selecione a tabela:") -> tuple:
        """
        Helper para seleção de dataset e planilha
        Retorna: (dataset_name, dataframe, sheet_name) ou (None, None, None)
        """
        dataset_names = list(st.session_state['datasets'].keys())
        
        if not dataset_names:
            return None, None, None
        
        # Seleção do dataset
        selected_dataset = st.selectbox(
            label,
            dataset_names,
            key=f"{key_prefix}_dataset"
        )
        
        if not selected_dataset:
            return None, None, None
        
        dataset_info = st.session_state['datasets'][selected_dataset]
        sheet_info = dataset_info.get('sheet_info', {'sheets': ['Dados'], 'selected': 'Dados'})
        
        # Se há múltiplas planilhas, mostrar seletor
        if len(sheet_info['sheets']) > 1:
            selected_sheet = st.selectbox(
                f"Planilha de '{selected_dataset}':",
                sheet_info['sheets'],
                index=sheet_info['sheets'].index(sheet_info['selected']) if sheet_info['selected'] in sheet_info['sheets'] else 0,
                key=f"{key_prefix}_sheet"
            )
            
            # Se mudou de planilha, recarregar dados
            if selected_sheet != sheet_info['selected']:
                try:
                    if f"original_file_{selected_dataset}" in st.session_state:
                        file_bytes = st.session_state[f"original_file_{selected_dataset}"]
                        file_buffer = io.BytesIO(file_bytes)
                        new_df = pd.read_excel(file_buffer, sheet_name=selected_sheet)
                        
                        # Atualizar dados
                        st.session_state['datasets'][selected_dataset]['data'] = new_df
                        st.session_state['datasets'][selected_dataset]['sheet_info']['selected'] = selected_sheet
                        st.rerun()
                    else:
                        st.warning(f"Arquivo original não encontrado para '{selected_dataset}'.")
                        return selected_dataset, dataset_info['data'], sheet_info['selected']
                
                except Exception as e:
                    st.error(f"Erro ao trocar planilha: {str(e)}")
                    return selected_dataset, dataset_info['data'], sheet_info['selected']
        else:
            selected_sheet = sheet_info['selected']
        
        return selected_dataset, dataset_info['data'], selected_sheet
    
    def _render_operations_tab(self) -> None:
        """Renderiza aba de operações de dados (joins, merges, etc.)"""
        if not st.session_state['datasets']:
            st.info("📋 Carregue pelo menos uma tabela para realizar operações.")
            return
        
        st.subheader("🔧 Operações de Dados")
        
        # Tabs para diferentes operações
        operations_tabs = st.tabs([
            "🔗 Joins/Merge",
            "🔍 PROCV/Lookup", 
            "📋 DE/PARA",
            "🧮 Operações Matemáticas"
        ])
        
        # Tab 1: Joins/Merge
        with operations_tabs[0]:
            st.subheader("🔗 Juntar Tabelas (JOIN/MERGE)")
            
            dataset_names = list(st.session_state['datasets'].keys())
            
            if len(dataset_names) < 2:
                st.warning("Você precisa ter pelo menos 2 tabelas para realizar um join.")
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Tabela Principal (Esquerda)**")
                left_table, left_df, left_sheet = self._get_dataset_with_sheet_selection(
                    "left_join", "Selecione a tabela principal:"
                )
                
                if left_table and left_df is not None:
                    left_columns = list(left_df.columns)
                    left_key = st.selectbox(
                        "Coluna chave (esquerda):",
                        left_columns,
                        key="left_key_join"
                    )
            
            with col2:
                st.write("**Tabela Secundária (Direita)**")
                available_right_tables = [name for name in dataset_names if name != left_table] if left_table else dataset_names
                
                if available_right_tables:
                    right_table = st.selectbox(
                        "Selecione a tabela secundária:",
                        available_right_tables,
                        key="right_table_join_selector"
                    )
                    
                    if right_table:
                        # Usar seleção manual para a segunda tabela para evitar conflitos de key
                        dataset_info = st.session_state['datasets'][right_table]
                        sheet_info = dataset_info.get('sheet_info', {'sheets': ['Dados'], 'selected': 'Dados'})
                        
                        if len(sheet_info['sheets']) > 1:
                            right_sheet = st.selectbox(
                                f"Planilha de '{right_table}':",
                                sheet_info['sheets'],
                                index=sheet_info['sheets'].index(sheet_info['selected']) if sheet_info['selected'] in sheet_info['sheets'] else 0,
                                key="right_sheet_join"
                            )
                            
                            # Recarregar se necessário
                            if right_sheet != sheet_info['selected']:
                                try:
                                    if f"original_file_{right_table}" in st.session_state:
                                        file_bytes = st.session_state[f"original_file_{right_table}"]
                                        file_buffer = io.BytesIO(file_bytes)
                                        new_df = pd.read_excel(file_buffer, sheet_name=right_sheet)
                                        
                                        st.session_state['datasets'][right_table]['data'] = new_df
                                        st.session_state['datasets'][right_table]['sheet_info']['selected'] = right_sheet
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao trocar planilha: {str(e)}")
                        
                        right_df = dataset_info['data']
                        right_columns = list(right_df.columns)
                        right_key = st.selectbox(
                            "Coluna chave (direita):",
                            right_columns,
                            key="right_key_join"
                        )
                else:
                    right_table = None
                    right_df = None
                    right_key = None
            
            # Tipo de join
            join_type = st.selectbox(
                "Tipo de JOIN:",
                ["inner", "left", "right", "outer"],
                index=1,  # left como padrão
                key="join_type"
            )
            
            # Nome da nova tabela
            new_table_name = st.text_input(
                "Nome da tabela resultante:",
                value=f"{left_table}_join_{right_table}",
                key="join_result_name"
            )
            
            if st.button("🔗 Executar JOIN", key="execute_join"):
                if left_table and right_table and left_key and right_key and new_table_name:
                    try:
                        left_df = st.session_state['datasets'][left_table]['data']
                        right_df = st.session_state['datasets'][right_table]['data']
                        
                        # Executar merge
                        result_df = pd.merge(
                            left_df, 
                            right_df, 
                            left_on=left_key, 
                            right_on=right_key, 
                            how=join_type,
                            suffixes=('_x', '_y')
                        )
                        
                        # Salvar resultado
                        if new_table_name not in st.session_state['datasets']:
                            st.session_state['datasets'][new_table_name] = {
                                'data': result_df,
                                'original': result_df.copy(),
                                'filename': f"{new_table_name}.xlsx",
                                'sheet_info': {'sheets': ['Dados'], 'selected': 'Dados'},
                                'size': len(result_df)
                            }
                            
                            self.show_success(f"✅ JOIN executado com sucesso! Tabela '{new_table_name}' criada com {len(result_df)} linhas.")
                            st.rerun()
                        else:
                            self.show_error(f"❌ Já existe uma tabela com o nome '{new_table_name}'")
                    
                    except Exception as e:
                        self.show_error(f"❌ Erro ao executar JOIN: {str(e)}")
        
        # Tab 2: PROCV/Lookup
        with operations_tabs[1]:
            st.subheader("🔍 PROCV/Lookup")
            
            if len(dataset_names) < 2:
                st.warning("Você precisa ter pelo menos 2 tabelas para realizar um PROCV.")
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Tabela de Origem**")
                source_table, source_df, source_sheet = self._get_dataset_with_sheet_selection(
                    "source_lookup", "Tabela onde buscar valores:"
                )
                
                if source_table and source_df is not None:
                    source_columns = list(source_df.columns)
                    lookup_column = st.selectbox(
                        "Coluna para buscar:",
                        source_columns,
                        key="lookup_column"
                    )
            
            with col2:
                st.write("**Tabela de Referência**")
                available_ref_tables = [name for name in dataset_names if name != source_table] if source_table else dataset_names
                
                if available_ref_tables:
                    ref_table = st.selectbox(
                        "Tabela de referência:",
                        available_ref_tables,
                        key="ref_table_lookup_selector"
                    )
                    
                    if ref_table:
                        # Seleção manual para evitar conflitos
                        dataset_info = st.session_state['datasets'][ref_table]
                        sheet_info = dataset_info.get('sheet_info', {'sheets': ['Dados'], 'selected': 'Dados'})
                        
                        if len(sheet_info['sheets']) > 1:
                            ref_sheet = st.selectbox(
                                f"Planilha de '{ref_table}':",
                                sheet_info['sheets'],
                                index=sheet_info['sheets'].index(sheet_info['selected']) if sheet_info['selected'] in sheet_info['sheets'] else 0,
                                key="ref_sheet_lookup"
                            )
                            
                            if ref_sheet != sheet_info['selected']:
                                try:
                                    if f"original_file_{ref_table}" in st.session_state:
                                        file_bytes = st.session_state[f"original_file_{ref_table}"]
                                        file_buffer = io.BytesIO(file_bytes)
                                        new_df = pd.read_excel(file_buffer, sheet_name=ref_sheet)
                                        
                                        st.session_state['datasets'][ref_table]['data'] = new_df
                                        st.session_state['datasets'][ref_table]['sheet_info']['selected'] = ref_sheet
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao trocar planilha: {str(e)}")
                        
                        ref_df = dataset_info['data']
                
                if ref_table:
                    ref_df = st.session_state['datasets'][ref_table]['data']
                    ref_columns = list(ref_df.columns)
                    
                    ref_key_column = st.selectbox(
                        "Coluna chave (referência):",
                        ref_columns,
                        key="ref_key_column"
                    )
                    
                    value_column = st.selectbox(
                        "Coluna de valores a retornar:",
                        ref_columns,
                        key="value_column"
                    )
            
            new_column_name = st.text_input(
                "Nome da nova coluna:",
                value="PROCV_Result",
                key="procv_column_name"
            )
            
            if st.button("🔍 Executar PROCV", key="execute_lookup"):
                if all([source_table, ref_table, lookup_column, ref_key_column, value_column, new_column_name]):
                    try:
                        source_df = st.session_state['datasets'][source_table]['data'].copy()
                        ref_df = st.session_state['datasets'][ref_table]['data']
                        
                        # Criar dicionário de lookup
                        lookup_dict = dict(zip(ref_df[ref_key_column], ref_df[value_column]))
                        
                        # Aplicar lookup
                        source_df[new_column_name] = source_df[lookup_column].map(lookup_dict)
                        
                        # Atualizar dados
                        st.session_state['datasets'][source_table]['data'] = source_df
                        
                        self.show_success(f"✅ PROCV executado! Coluna '{new_column_name}' adicionada à tabela '{source_table}'.")
                        st.rerun()
                    
                    except Exception as e:
                        self.show_error(f"❌ Erro ao executar PROCV: {str(e)}")
        
        # Tab 3: DE/PARA
        with operations_tabs[2]:
            st.subheader("📋 Tabela DE/PARA")
            
            if len(dataset_names) < 1:
                st.warning("Você precisa ter pelo menos 1 tabela para criar DE/PARA.")
                return
            
            # Seleção da tabela e planilha
            selected_table, df, selected_sheet = self._get_dataset_with_sheet_selection(
                "depara", "Selecione a tabela:"
            )
            
            if selected_table and df is not None:
                columns = list(df.columns)
                
                target_column = st.selectbox(
                    "Coluna para aplicar DE/PARA:",
                    columns,
                    key="depara_column"
                )
                
                # Mostrar valores únicos
                if target_column:
                    unique_values = df[target_column].unique()
                    st.write(f"**Valores únicos encontrados:** {len(unique_values)}")
                    
                    # Interface para DE/PARA
                    st.write("**Definir substituições:**")
                    
                    # Upload de arquivo DE/PARA ou criação manual
                    depara_method = st.radio(
                        "Método:",
                        ["Upload arquivo DE/PARA", "Criar manualmente"],
                        key="depara_method"
                    )
                    
                    if depara_method == "Upload arquivo DE/PARA":
                        depara_file = st.file_uploader(
                            "Upload arquivo DE/PARA (CSV ou Excel):",
                            type=['csv', 'xlsx', 'xls'],
                            key="depara_upload"
                        )
                        
                        if depara_file:
                            try:
                                if depara_file.name.endswith('.csv'):
                                    depara_df = pd.read_csv(depara_file)
                                else:
                                    depara_df = pd.read_excel(depara_file)
                                
                                if len(depara_df.columns) >= 2:
                                    st.write("**Preview da tabela DE/PARA:**")
                                    st.dataframe(depara_df.head())
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        de_column = st.selectbox(
                                            "Coluna DE (valores originais):",
                                            depara_df.columns,
                                            key="de_column"
                                        )
                                    with col2:
                                        para_column = st.selectbox(
                                            "Coluna PARA (novos valores):",
                                            depara_df.columns,
                                            key="para_column"
                                        )
                                    
                                    if st.button("🔄 Aplicar DE/PARA", key="apply_depara_file"):
                                        try:
                                            # Criar dicionário de substituição
                                            replacement_dict = dict(zip(depara_df[de_column], depara_df[para_column]))
                                            
                                            # Aplicar substituições
                                            df_updated = df.copy()
                                            df_updated[target_column] = df_updated[target_column].replace(replacement_dict)
                                            
                                            # Atualizar dados
                                            st.session_state['datasets'][selected_table]['data'] = df_updated
                                            
                                            replaced_count = (df[target_column] != df_updated[target_column]).sum()
                                            self.show_success(f"✅ DE/PARA aplicado! {replaced_count} valores substituídos.")
                                            st.rerun()
                                        
                                        except Exception as e:
                                            self.show_error(f"❌ Erro ao aplicar DE/PARA: {str(e)}")
                                else:
                                    st.error("Arquivo deve ter pelo menos 2 colunas")
                            
                            except Exception as e:
                                self.show_error(f"❌ Erro ao ler arquivo: {str(e)}")
                    
                    else:  # Criar manualmente
                        st.write("**Criar substituições manualmente:**")
                        
                        # Formulário para adicionar substituições
                        with st.form("manual_depara"):
                            col1, col2 = st.columns(2)
                            with col1:
                                from_value = st.text_input("Valor DE (original):")
                            with col2:
                                to_value = st.text_input("Valor PARA (novo):")
                            
                            add_replacement = st.form_submit_button("➕ Adicionar Substituição")
                        
                        # Armazenar substituições no session state
                        if 'manual_replacements' not in st.session_state:
                            st.session_state['manual_replacements'] = {}
                        
                        if add_replacement and from_value and to_value:
                            st.session_state['manual_replacements'][from_value] = to_value
                            st.success(f"Substituição adicionada: '{from_value}' → '{to_value}'")
                        
                        # Mostrar substituições atuais
                        if st.session_state['manual_replacements']:
                            st.write("**Substituições definidas:**")
                            replacements_df = pd.DataFrame([
                                {'DE': k, 'PARA': v} 
                                for k, v in st.session_state['manual_replacements'].items()
                            ])
                            st.dataframe(replacements_df)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("🔄 Aplicar Todas", key="apply_manual_depara"):
                                    try:
                                        df_updated = df.copy()
                                        df_updated[target_column] = df_updated[target_column].replace(
                                            st.session_state['manual_replacements']
                                        )
                                        
                                        # Atualizar dados
                                        st.session_state['datasets'][selected_table]['data'] = df_updated
                                        
                                        replaced_count = (df[target_column] != df_updated[target_column]).sum()
                                        self.show_success(f"✅ DE/PARA aplicado! {replaced_count} valores substituídos.")
                                        st.rerun()
                                    
                                    except Exception as e:
                                        self.show_error(f"❌ Erro ao aplicar DE/PARA: {str(e)}")
                            
                            with col2:
                                if st.button("🗑️ Limpar Substituições", key="clear_replacements"):
                                    st.session_state['manual_replacements'] = {}
                                    st.rerun()
        
        # Tab 4: Operações Matemáticas
        with operations_tabs[3]:
            st.subheader("🧮 Operações Matemáticas")
            
            if len(dataset_names) < 1:
                st.warning("Você precisa ter pelo menos 1 tabela para realizar operações matemáticas.")
                return
            
            # Seleção da tabela e planilha
            selected_table, df, selected_sheet = self._get_dataset_with_sheet_selection(
                "math", "Selecione a tabela:"
            )
            
            if selected_table and df is not None:
                numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
                
                if not numeric_columns:
                    st.warning("Não foram encontradas colunas numéricas nesta tabela.")
                    return
                
                # Tipo de operação
                operation_type = st.selectbox(
                    "Tipo de operação:",
                    ["Soma de colunas", "Subtração", "Multiplicação", "Divisão", "Estatísticas"],
                    key="math_operation"
                )
                
                if operation_type in ["Soma de colunas", "Subtração", "Multiplicação", "Divisão"]:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        column1 = st.selectbox(
                            "Primeira coluna:",
                            numeric_columns,
                            key="math_col1"
                        )
                    
                    with col2:
                        column2 = st.selectbox(
                            "Segunda coluna:",
                            numeric_columns,
                            key="math_col2"
                        )
                    
                    new_column_name = st.text_input(
                        "Nome da nova coluna:",
                        value=f"{column1}_{operation_type.lower().replace(' ', '_')}_{column2}",
                        key="math_new_column"
                    )
                    
                    if st.button(f"🧮 Executar {operation_type}", key="execute_math"):
                        if column1 and column2 and new_column_name:
                            try:
                                df_updated = df.copy()
                                
                                if operation_type == "Soma de colunas":
                                    df_updated[new_column_name] = df_updated[column1] + df_updated[column2]
                                elif operation_type == "Subtração":
                                    df_updated[new_column_name] = df_updated[column1] - df_updated[column2]
                                elif operation_type == "Multiplicação":
                                    df_updated[new_column_name] = df_updated[column1] * df_updated[column2]
                                elif operation_type == "Divisão":
                                    df_updated[new_column_name] = df_updated[column1] / df_updated[column2]
                                
                                # Atualizar dados
                                st.session_state['datasets'][selected_table]['data'] = df_updated
                                
                                self.show_success(f"✅ {operation_type} executada! Coluna '{new_column_name}' criada.")
                                st.rerun()
                            
                            except Exception as e:
                                self.show_error(f"❌ Erro na operação: {str(e)}")
                
                elif operation_type == "Estatísticas":
                    selected_columns = st.multiselect(
                        "Selecione as colunas para calcular estatísticas:",
                        numeric_columns,
                        key="stats_columns"
                    )
                    
                    if selected_columns:
                        stats_df = df[selected_columns].describe()
                        st.write("**Estatísticas Descritivas:**")
                        st.dataframe(stats_df)
                        
                        # Opção de salvar como nova tabela
                        if st.button("💾 Salvar Estatísticas como Nova Tabela", key="save_stats"):
                            stats_table_name = f"{selected_table}_estatisticas"
                            
                            if stats_table_name not in st.session_state['datasets']:
                                st.session_state['datasets'][stats_table_name] = {
                                    'data': stats_df.reset_index(),
                                    'original': stats_df.reset_index().copy(),
                                    'filename': f"{stats_table_name}.xlsx",
                                    'sheet_info': {'sheets': ['Estatísticas'], 'selected': 'Estatísticas'},
                                    'size': len(stats_df)
                                }
                                
                                self.show_success(f"✅ Tabela de estatísticas '{stats_table_name}' criada!")
                                st.rerun()
                            else:
                                self.show_error("❌ Tabela de estatísticas já existe!")
    
    def _render_analysis_tab(self) -> None:
        """Renderiza aba de análise dos dados"""
        if not st.session_state['datasets']:
            st.info("📋 Carregue uma ou mais tabelas para ver as análises.")
            return
        
        st.subheader("📊 Análise dos Dados")
        
        # Seletor de tabela e planilha para análise
        selected_dataset, df, selected_sheet = self._get_dataset_with_sheet_selection(
            "analysis", "Selecione a tabela para analisar:"
        )
        
        if selected_dataset and df is not None:
            
            # Estatísticas básicas
            st.subheader("📈 Estatísticas Gerais")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📄 Total de Linhas", len(df))
            with col2:  
                st.metric("📊 Total de Colunas", len(df.columns))
            with col3:
                st.metric("❌ Valores Nulos", df.isnull().sum().sum())
            with col4:
                st.metric("📝 Células Preenchidas", df.notna().sum().sum())
            
            # Análise por colunas
            st.subheader("🔍 Análise por Colunas")
            
            # Selecionar coluna para análise
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if numeric_cols:
            st.subheader("📊 Colunas Numéricas")
            selected_numeric = st.selectbox("Escolha uma coluna numérica:", numeric_cols)
            
            if selected_numeric:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Estatísticas:**")
                    stats = df[selected_numeric].describe()
                    st.dataframe(stats)
                
                with col2:
                    st.write("**Gráfico:**")
                    st.bar_chart(df[selected_numeric].value_counts().head(10))
        
        if text_cols:
            st.subheader("📝 Colunas de Texto")
            selected_text = st.selectbox("Escolha uma coluna de texto:", text_cols)
            
            if selected_text:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Valores mais frequentes:**")
                    value_counts = df[selected_text].value_counts().head(10)
                    st.dataframe(value_counts)
                
                with col2:
                    st.write("**Distribuição:**")
                    st.bar_chart(value_counts)
    
    def _render_config_tab(self) -> None:
        """Renderiza aba de configurações"""
        st.subheader("⚙️ Configurações do Excel Editor")
        
        # Configurações de display
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Configurações Gerais")
            auto_save = st.checkbox("💾 Salvamento Automático", value=True)
            show_stats = st.checkbox("📊 Mostrar Estatísticas", value=True)
            max_rows_display = st.slider("📄 Máx. linhas exibidas:", 10, 1000, 100)
        
        with col2:
            st.subheader("🎨 Aparência")
            column_width = st.selectbox("📏 Largura das colunas:", ["Pequena", "Média", "Grande"], index=1)
            show_index = st.checkbox("🔢 Mostrar índice", value=True)
            highlight_changes = st.checkbox("✨ Destacar alterações", value=True)
        
        # Configurações de exportação
        st.subheader("📤 Configurações de Exportação")
        
        col3, col4 = st.columns(2)
        with col3:
            export_format = st.selectbox("📋 Formato padrão:", ["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"])
            include_index = st.checkbox("🔢 Incluir índices na exportação", value=False)
        
        with col4:
            date_format = st.selectbox("📅 Formato de data:", ["DD/MM/AAAA", "MM/DD/AAAA", "AAAA-MM-DD"])
            decimal_separator = st.selectbox("🔢 Separador decimal:", [",", "."], index=1)
        
        # Salvar configurações
        if st.button("💾 Salvar Configurações", width="stretch"):
            config = {
                'auto_save': auto_save,
                'show_stats': show_stats,
                'max_rows_display': max_rows_display,
                'column_width': column_width,
                'show_index': show_index,
                'highlight_changes': highlight_changes,
                'export_format': export_format,
                'include_index': include_index,
                'date_format': date_format,
                'decimal_separator': decimal_separator
            }
            st.session_state['excel_config'] = config
            self.show_success("Configurações salvas!")
            
            # Mostrar configurações salvas
            with st.expander("👀 Configurações Atuais"):
                st.json(config)
    
    def _download_excel(self, df: pd.DataFrame, filename: str) -> None:
        """Gera download do arquivo Excel"""
        try:
            # Criar buffer em memória
            buffer = io.BytesIO()
            
            # Escrever DataFrame no buffer como Excel
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Dados', index=False)
            
            buffer.seek(0)
            
            # Botão de download
            st.download_button(
                label="📥 Baixar Excel",
                data=buffer.getvalue(),
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch"
            )
            
        except Exception as e:
            self.show_error(f"Erro ao gerar arquivo Excel: {str(e)}")