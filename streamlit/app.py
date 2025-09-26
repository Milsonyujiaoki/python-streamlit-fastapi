#!/usr/bin/env python3
"""
Aplicação Streamlit Modular e Escalável
Sistema corporativo para edição de dados e pesquisa de informações
"""

from core import AppManager, AppConfig
from modules import SocietaryModule, LyricsModule, ExcelModule

def main():
    """Função principal da aplicação"""
    # Configuração da aplicação
    config = AppConfig(
        page_title="Sistema Corporativo Integrado",
        page_icon="🏢",
        layout="wide",
        sidebar_title="📋 Menu Principal"
    )
    
    # Criar gerenciador da aplicação
    app = AppManager(config)
    
    # Registrar módulos disponíveis
    app.register_module(SocietaryModule())
    app.register_module(LyricsModule())
    app.register_module(ExcelModule())
    
    # Executar aplicação
    app.run()

if __name__ == "__main__":
    main()