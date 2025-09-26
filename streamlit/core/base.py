# Base Imports
import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class AppConfig:
    """Configuração centralizada da aplicação"""
    page_title: str = "Sistema Corporativo"
    page_icon: str = "🏢" 
    layout: str = "wide"
    sidebar_title: str = "📋 Menu Principal"

class BaseModule(ABC):
    """Classe base para módulos da aplicação"""
    
    def __init__(self, name: str, icon: str, description: str = ""):
        self.name = name
        self.icon = icon
        self.description = description
        self.full_name = f"{icon} {name}"
    
    @abstractmethod
    def render(self) -> None:
        """Método principal para renderizar o módulo"""
        pass
    
    def show_header(self) -> None:
        """Exibe cabeçalho padrão do módulo"""
        st.header(f"{self.icon} {self.name}")
        if self.description:
            st.markdown(f"*{self.description}*")
    
    def show_error(self, message: str) -> None:
        """Exibe erro padronizado"""
        st.error(f"❌ {message}")
    
    def show_success(self, message: str) -> None:
        """Exibe sucesso padronizado"""  
        st.success(f"✅ {message}")
        
    def show_warning(self, message: str) -> None:
        """Exibe aviso padronizado"""
        st.warning(f"⚠️ {message}")

class DataProcessor:
    """Processador de dados genérico"""
    
    @staticmethod
    def safe_json_load(data: Any) -> Dict:
        """Carregamento seguro de JSON"""
        try:
            if isinstance(data, str):
                return json.loads(data)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido: {str(e)}")
    
    @staticmethod  
    def create_editable_dataframe(data: Dict[str, Any], key_name: str = "Campo", value_name: str = "Valor") -> pd.DataFrame:
        """Cria DataFrame editável a partir de dicionário"""
        if not data:
            return pd.DataFrame({key_name: [], value_name: []})
            
        return pd.DataFrame({
            key_name: list(data.keys()),
            value_name: list(data.values())
        })

class UIComponents:
    """Componentes de interface reutilizáveis"""
    
    @staticmethod
    def file_uploader(label: str, file_types: List[str], help_text: str = "") -> Optional[Any]:
        """File uploader padronizado"""
        return st.file_uploader(
            label,
            type=file_types,
            help=help_text or f"Selecione um arquivo {', '.join(file_types)}"
        )
    
    @staticmethod
    def data_editor(df: pd.DataFrame, key: str, **kwargs) -> pd.DataFrame:
        """Data editor padronizado"""
        default_config = {
            'width': "stretch",
            'num_rows': "dynamic",
            'key': key
        }
        default_config.update(kwargs)
        return st.data_editor(df, **default_config)
    
    @staticmethod
    def action_buttons(buttons_config: List[Dict[str, Any]], columns: int = 3) -> Dict[str, bool]:
        """Cria botões de ação em colunas"""
        cols = st.columns(columns)
        button_states = {}
        
        for i, config in enumerate(buttons_config):
            col = cols[i % columns]
            with col:
                button_states[config['key']] = st.button(
                    config['label'],
                    width="stretch" if config.get('full_width', True) else "content",
                    type=config.get('type', 'secondary')
                )
        
        return button_states
    
    @staticmethod
    def tabs(tab_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cria abas padronizadas"""
        tab_names = [config['name'] for config in tab_configs]
        tabs = st.tabs(tab_names)
        
        tab_objects = {}
        for i, (tab, config) in enumerate(zip(tabs, tab_configs)):
            tab_objects[config['key']] = {
                'tab': tab,
                'config': config
            }
        
        return tab_objects

class AppManager:
    """Gerenciador principal da aplicação"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.modules: Dict[str, BaseModule] = {}
        self._setup_page()
    
    def _setup_page(self) -> None:
        """Configuração inicial da página"""
        st.set_page_config(
            page_title=self.config.page_title,
            page_icon=self.config.page_icon,
            layout=self.config.layout
        )
    
    def register_module(self, module: BaseModule) -> None:
        """Registra um novo módulo"""
        self.modules[module.name] = module
    
    def render_sidebar(self) -> str:
        """Renderiza sidebar com seleção de módulos"""
        st.sidebar.title(self.config.sidebar_title)
        
        module_names = [module.full_name for module in self.modules.values()]
        
        if not module_names:
            st.sidebar.warning("Nenhum módulo disponível")
            return ""
        
        selected = st.sidebar.selectbox(
            "Escolha uma funcionalidade:",
            module_names
        )
        
        # Encontrar o módulo selecionado
        for module in self.modules.values():
            if module.full_name == selected:
                return module.name
        
        return ""
    
    def run(self) -> None:
        """Executa a aplicação"""
        # Título principal
        st.title(f"{self.config.page_icon} {self.config.page_title}")
        
        # Renderizar sidebar e obter módulo selecionado
        selected_module_name = self.render_sidebar()
        
        # Renderizar módulo selecionado
        if selected_module_name and selected_module_name in self.modules:
            try:
                self.modules[selected_module_name].render()
            except Exception as e:
                st.error(f"Erro ao carregar módulo '{selected_module_name}': {str(e)}")
                st.exception(e)
        elif self.modules:
            # Renderizar primeiro módulo se nenhum estiver selecionado
            first_module = next(iter(self.modules.values()))
            first_module.render()
        else:
            st.info("📋 Nenhum módulo configurado. Adicione módulos para começar.")