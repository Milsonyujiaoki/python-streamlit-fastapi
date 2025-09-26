import json
import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
from core.base import BaseModule, DataProcessor, UIComponents

class SocietaryModule(BaseModule):
    """Módulo para edição de atos societários"""
    
    def __init__(self):
        super().__init__(
            name="Editor de Atos Societários",
            icon="🏢",
            description="Sistema para edição e gerenciamento de dados societários"
        )
    
    def render(self) -> None:
        """Renderiza o módulo completo"""
        self.show_header()
        
        # Configurar abas
        tab_configs = [
            {'name': '📁 Upload JSON', 'key': 'upload'},
            {'name': '✏️ Colar JSON', 'key': 'paste'},
            {'name': '📄 Exemplo', 'key': 'example'}
        ]
        
        tabs = UIComponents.tabs(tab_configs)
        
        # Processar cada aba
        self._render_upload_tab(tabs['upload']['tab'])
        self._render_paste_tab(tabs['paste']['tab'])
        self._render_example_tab(tabs['example']['tab'])
    
    def _render_upload_tab(self, tab) -> None:
        """Renderiza aba de upload"""
        with tab:
            st.subheader("Upload de arquivo JSON")
            
            arquivo_json = UIComponents.file_uploader(
                "Faça upload do arquivo JSON:",
                ['json'],
                "Selecione um arquivo JSON com dados societários"
            )
            
            if arquivo_json is not None:
                try:
                    dados_json = json.loads(arquivo_json.read().decode('utf-8'))
                    self.show_success("Arquivo carregado com sucesso!")
                    self._process_societary_data(dados_json)
                except Exception as e:
                    self.show_error(f"Erro ao carregar arquivo: {str(e)}")
    
    def _render_paste_tab(self, tab) -> None:
        """Renderiza aba de colar JSON"""
        with tab:
            st.subheader("Colar dados JSON")
            
            json_text = st.text_area(
                "Cole aqui o JSON com dados societários:",
                height=200,
                help="Cole o conteúdo JSON completo na área de texto"
            )
            
            if st.button("📝 Processar JSON Colado", width="stretch"):
                if json_text.strip():
                    try:
                        dados_json = json.loads(json_text)
                        self.show_success("JSON processado com sucesso!")
                        self._process_societary_data(dados_json)
                    except json.JSONDecodeError as e:
                        self.show_error(f"JSON inválido: {str(e)}")
                else:
                    self.show_warning("Por favor, cole um JSON válido na área de texto")
    
    def _render_example_tab(self, tab) -> None:
        """Renderiza aba de exemplo"""
        with tab:
            st.subheader("Exemplo de Ato Societário")
            
            exemplo = self._get_sample_data()
            
            st.code(json.dumps(exemplo, indent=2, ensure_ascii=False), language='json')
            
            if st.button("📋 Usar Este Exemplo", width="stretch"):
                self.show_success("Exemplo carregado!")
                self._process_societary_data(exemplo)
    
    def _process_societary_data(self, dados_json: Dict) -> None:
        """Processa dados societários e exibe interface de edição"""
        try:
            processor = SocietaryDataProcessor()
            data_frames = processor.process_json(dados_json)
            
            self._render_editing_interface(data_frames)
            
        except Exception as e:
            self.show_error(f"Erro ao processar dados: {str(e)}")
    
    def _render_editing_interface(self, data_frames: Dict) -> None:
        """Renderiza interface de edição dos dados"""
        df_empresa = data_frames['empresa']
        df_socios = data_frames['socios'] 
        df_novos = data_frames['novos']
        df_saindo = data_frames['saindo']
        dados_originais = data_frames['originais']
        
        if df_empresa is not None and not df_empresa.empty:
            # Informações da Empresa
            st.subheader("🏢 Informações da Empresa")
            df_empresa_editado = UIComponents.data_editor(
                df_empresa,
                key="empresa_editor"
            )
            
            # Sócios da Empresa  
            if not df_socios.empty:
                st.subheader("👥 Sócios da Empresa")
                df_socios_editado = UIComponents.data_editor(
                    df_socios,
                    key="socios_editor"
                )
            else:
                df_socios_editado = pd.DataFrame()
            
            # Novos Sócios
            if not df_novos.empty:
                st.subheader("➕ Novos Sócios")
                df_novos_editado = UIComponents.data_editor(
                    df_novos,
                    key="novos_editor"
                )
            else:
                df_novos_editado = pd.DataFrame()
            
            # Sócios que Saem
            if not df_saindo.empty:
                st.subheader("➖ Sócios que Saem")
                df_saindo_editado = UIComponents.data_editor(
                    df_saindo,
                    key="saindo_editor"
                )
            else:
                df_saindo_editado = pd.DataFrame()
            
            # Botões de ação
            self._render_action_buttons(
                df_empresa_editado,
                df_socios_editado,
                df_novos_editado, 
                df_saindo_editado,
                dados_originais
            )
    
    def _render_action_buttons(self, df_empresa, df_socios, df_novos, df_saindo, dados_originais) -> None:
        """Renderiza botões de ação"""
        buttons_config = [
            {'label': '💾 Salvar Alterações', 'key': 'save'},
            {'label': '📥 Download JSON', 'key': 'download'},
            {'label': '🔄 Resetar', 'key': 'reset'}
        ]
        
        button_states = UIComponents.action_buttons(buttons_config)
        
        if button_states['save']:
            try:
                exporter = SocietaryDataExporter()
                json_modificado = exporter.export_modified_data(
                    df_empresa, df_socios, df_novos, df_saindo, dados_originais
                )
                
                if json_modificado:
                    st.session_state['json_modificado'] = json_modificado
                    self.show_success("Alterações salvas!")
            except Exception as e:
                self.show_error(f"Erro ao salvar: {str(e)}")
        
        if button_states['download'] and 'json_modificado' in st.session_state:
            st.download_button(
                label="📥 Download Executar",
                data=st.session_state['json_modificado'],
                file_name="ato_societario_modificado.json",
                mime="application/json",
                width="stretch"
            )
        
        if button_states['reset']:
            # Limpar session state e recarregar
            for key in list(st.session_state.keys()):
                if key.startswith(('empresa_', 'socios_', 'novos_', 'saindo_', 'json_')):
                    del st.session_state[key]
            st.rerun()
        
        # Prévia do JSON modificado
        if 'json_modificado' in st.session_state:
            with st.expander("👀 Prévia do JSON Modificado"):
                st.code(st.session_state['json_modificado'], language='json')
    
    def _get_sample_data(self) -> Dict:
        """Retorna dados de exemplo"""
        return {
            "company_name": "EXEMPLO SOCIEDADE LTDA",
            "cnpj": "12.345.678/0001-90",
            "nire": "12345678901",
            "address": "Rua Exemplo, 123, Centro, São Paulo/SP",
            "zip_code": "01234-567",
            "partners": [
                {
                    "partner_name": "João Silva",
                    "cpf_cnpj": "123.456.789-10",
                    "represented_by": "",
                    "address": "Rua A, 100, São Paulo/SP",
                    "participation_value": 10000.0,
                    "qualification": "Sócio Administrador"
                },
                {
                    "partner_name": "Maria Santos",
                    "cpf_cnpj": "987.654.321-00", 
                    "represented_by": "",
                    "address": "Rua B, 200, Rio de Janeiro/RJ",
                    "participation_value": 15000.0,
                    "qualification": "Sócia"
                }
            ],
            "new_partners": ["Carlos Oliveira"],
            "leaving_partners": ["Pedro Costa"]
        }

class SocietaryDataProcessor(DataProcessor):
    """Processador específico para dados societários"""
    
    def process_json(self, dados_json: Any) -> Dict[str, Any]:
        """Processa JSON societário e retorna DataFrames"""
        dados = self.safe_json_load(dados_json)
        
        # DataFrame principal da empresa
        info_empresa = {
            'Nome da Empresa': dados.get('company_name', ''),
            'CNPJ': dados.get('cnpj', ''),
            'NIRE': dados.get('nire', ''),
            'Endereço': dados.get('address', ''),
            'CEP': dados.get('zip_code', '')
        }
        df_empresa = self.create_editable_dataframe(info_empresa)
        
        # DataFrame dos sócios
        socios = dados.get('partners', [])
        if socios:
            df_socios = pd.DataFrame(socios)
            # Reorganizar colunas principais
            colunas_principais = ['partner_name', 'cpf_cnpj', 'represented_by', 'address', 'participation_value', 'qualification']
            colunas_existentes = [col for col in colunas_principais if col in df_socios.columns]
            outras_colunas = [col for col in df_socios.columns if col not in colunas_principais]
            df_socios = df_socios[colunas_existentes + outras_colunas]
        else:
            df_socios = pd.DataFrame()
        
        # DataFrame dos novos sócios
        novos_socios = dados.get('new_partners', [])
        df_novos = pd.DataFrame({'Nome': novos_socios}) if novos_socios else pd.DataFrame()
        
        # DataFrame dos sócios que saem
        socios_saindo = dados.get('leaving_partners', [])
        df_saindo = pd.DataFrame({'Nome': socios_saindo}) if socios_saindo else pd.DataFrame()
        
        return {
            'empresa': df_empresa,
            'socios': df_socios,
            'novos': df_novos,
            'saindo': df_saindo,
            'originais': dados
        }

class SocietaryDataExporter:
    """Exportador de dados societários"""
    
    def export_modified_data(self, df_empresa, df_socios, df_novos, df_saindo, dados_originais) -> str:
        """Exporta dados modificados para JSON"""
        dados_modificados = dados_originais.copy()
        
        # Atualizar dados da empresa
        for _, row in df_empresa.iterrows():
            campo = row['Campo']
            valor = row['Valor']
            
            if campo == 'Nome da Empresa':
                dados_modificados['company_name'] = valor
            elif campo == 'CNPJ':
                dados_modificados['cnpj'] = valor
            elif campo == 'NIRE':
                dados_modificados['nire'] = valor
            elif campo == 'Endereço':
                dados_modificados['address'] = valor
            elif campo == 'CEP':
                dados_modificados['zip_code'] = valor
        
        # Atualizar lista de sócios
        if not df_socios.empty:
            dados_modificados['partners'] = df_socios.to_dict('records')
        
        # Atualizar novos sócios
        if not df_novos.empty:
            dados_modificados['new_partners'] = df_novos['Nome'].tolist()
        
        # Atualizar sócios que saem
        if not df_saindo.empty:
            dados_modificados['leaving_partners'] = df_saindo['Nome'].tolist()
        
        return json.dumps(dados_modificados, indent=2, ensure_ascii=False)