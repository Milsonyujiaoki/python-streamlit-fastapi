import requests
import streamlit as st
from typing import Dict, Any
from core.base import BaseModule, UIComponents

class LyricsModule(BaseModule):
    """Módulo para pesquisa de letras de música"""
    
    def __init__(self):
        super().__init__(
            name="Pesquisador de Letras",
            icon="🎵",
            description="Pesquisa letras de música usando a API lyrics.ovh"
        )
        self.api_url = "https://api.lyrics.ovh/v1"
    
    def render(self) -> None:
        """Renderiza o módulo de pesquisa de letras"""
        self.show_header()
        
        # Interface de pesquisa
        col1, col2 = st.columns(2)
        
        with col1:
            banda = st.text_input(
                "🎤 Nome da Banda:",
                placeholder="Ex: Beatles"
            )
        
        with col2:
            musica = st.text_input(
                "🎼 Nome da Música:",
                placeholder="Ex: Hey Jude"
            )
        
        # Botão de pesquisa
        if st.button("🔍 Pesquisar Letra", width="stretch"):
            if banda and musica:
                with st.spinner("🔍 Buscando letra..."):
                    resultado = self._search_lyrics(banda, musica)
                    self._display_result(resultado)
            else:
                self.show_warning("Por favor, insira o nome da banda e da música.")
        
        # Seção de ajuda
        with st.expander("ℹ️ Como usar"):
            st.markdown("""
            ### Como pesquisar letras:
            
            1. **Digite o nome da banda** no primeiro campo
            2. **Digite o nome da música** no segundo campo  
            3. **Clique em "🔍 Pesquisar Letra"**
            
            ### Dicas:
            - Use nomes em inglês para melhores resultados
            - Evite caracteres especiais
            - Seja específico com os nomes
            
            ### Exemplos que funcionam:
            - Banda: "Beatles" | Música: "Hey Jude"
            - Banda: "Queen" | Música: "Bohemian Rhapsody"
            - Banda: "Imagine Dragons" | Música: "Believer"
            """)
    
    def _search_lyrics(self, banda: str, musica: str) -> Dict[str, Any]:
        """
        Pesquisa letras de música usando a API lyrics.ovh
        
        Args:
            banda: Nome da banda
            musica: Nome da música
        
        Returns:
            Dict com a letra ou erro
        """
        try:
            # Limpar espaços e caracteres especiais
            banda_clean = banda.strip()
            musica_clean = musica.strip()
            
            response = requests.get(
                f"{self.api_url}/{banda_clean}/{musica_clean}", 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "lyrics": data.get("lyrics", "Letra não encontrada nos dados retornados.")
                }
            else:
                return {
                    "success": False,
                    "error": f"Erro na API: {response.status_code} - Letra não encontrada."
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Timeout na requisição. Tente novamente."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Erro de conexão: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro inesperado: {str(e)}"
            }
    
    def _display_result(self, resultado: Dict[str, Any]) -> None:
        """Exibe o resultado da pesquisa"""
        if resultado.get("success"):
            lyrics = resultado.get("lyrics", "")
            
            if lyrics.strip():
                st.success("🎵 Letra encontrada!")
                
                # Área de texto para a letra
                st.text_area(
                    "📝 Letra da música:",
                    value=lyrics,
                    height=400,
                    help="Você pode copiar a letra daqui"
                )
                
                # Botão para download
                st.download_button(
                    label="📥 Baixar Letra",
                    data=lyrics,
                    file_name="letra_musica.txt",
                    mime="text/plain",
                    width="stretch"
                )
            else:
                self.show_warning("Letra vazia ou não encontrada.")
        else:
            error_msg = resultado.get("error", "Erro desconhecido")
            self.show_error(error_msg)
    
    def _show_image_placeholder(self) -> None:
        """Exibe placeholder para imagem"""
        # Verificar se existe imagem no projeto
        image_path = "dev/Tests/Prancheta 3@2x-100.jpg"
        
        try:
            # Tentar mostrar imagem se existir
            st.image(image_path, width=300, caption="Logo do Projeto")
        except:
            # Mostrar emoji como placeholder
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1 style='font-size: 4em; margin: 0;'>🎵</h1>
                <p style='margin: 5px 0; color: #666; font-size: 0.8em;'>
                    Sistema de Pesquisa de Letras
                </p>
            </div>
            """, unsafe_allow_html=True)