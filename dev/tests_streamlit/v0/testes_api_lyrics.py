import requests
import streamlit as st
import os

def pesquisar_lyrics(banda, musica, url):
    """
    Pesquisa letras de música usando a API lyrics.ovh
    
    Args:
        banda: Nome da banda
        musica: Nome da música
        url: URL base da API
    
    Returns:
        Dict com a letra ou erro
    """
    if banda and musica:
        try:
            # Limpar espaços e caracteres especiais
            banda_clean = banda.strip()
            musica_clean = musica.strip()
            
            response = requests.get(f"{url}/{banda_clean}/{musica_clean}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {"lyrics": data.get("lyrics", "Letra não encontrada nos dados retornados.")}
            else:
                return {"error": f"Erro na API: {response.status_code} - Letra não encontrada."}
                
        except requests.exceptions.Timeout:
            return {"error": "Timeout na requisição. Tente novamente."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Erro de conexão: {str(e)}"}
        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}
    else:
        return {"error": "Por favor, insira o nome da banda e da música."}

# Configuração da página
st.set_page_config(
    page_title="Pesquisador de Letras",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Pesquisador de Letras de Música")
st.markdown("*Integração FastAPI e Streamlit*")

# Verificar se existe imagem local, senão usar placeholder
image_path = "https://media.licdn.com/dms/image/v2/C4D16AQH1D6d1X2MfXA/profile-displaybackgroundimage-shrink_200_800/profile-displaybackgroundimage-shrink_200_800/0/1649420804230?e=2147483647&v=beta&t=jaNPQxM5MlDk8xfNEyK-QruSwr_gdEIPxYlSDrFdw5A"



# Mostrar imagem se válida, senão mostrar placeholder
if image_path:
    try:
        st.image(image_path, width="stretch", caption="Logo do Projeto")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar imagem: {str(e)}")
        st.info("🎵 Usando interface sem imagem")
else:
    # Mostrar um emoji como placeholder
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 4em; margin: 0;'>🎵</h1>
        <p style='margin: 5px 0; color: #666; font-size: 0.8em;'>
            Adicione uma imagem em: dev/Tests/Prancheta 3@2x-100.jpg
        </p>
    </div>
    """, unsafe_allow_html=True)

# Configuração da API
API_URL = "https://api.lyrics.ovh/v1"

# Interface do usuário
col1, col2 = st.columns(2)

with col1:
    banda = st.text_input("🎤 Digite o nome da banda:", key="banda", placeholder="Ex: Queen")

with col2:
    musica = st.text_input("🎵 Digite o nome da música:", key="musica", placeholder="Ex: Bohemian Rhapsody")

# Botão centralizado
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    pesquisar = st.button("🔍 Pesquisar Letra", use_container_width=True)

# Processamento da pesquisa
if pesquisar:
    if banda.strip() and musica.strip():
        with st.spinner("Buscando letra..."):
            resultado = pesquisar_lyrics(banda, musica, API_URL)
            
            if "lyrics" in resultado:
                st.success("✅ Letra encontrada!")
                
                # Mostrar informações da música
                st.subheader(f"🎵 {musica} - {banda}")
                
                # Mostrar letra em uma caixa de texto expansível
                with st.expander("📜 Visualizar Letra Completa", expanded=True):
                    st.text_area(
                        "Letra:",
                        value=resultado["lyrics"],
                        height=400,
                        disabled=True,
                        key="lyrics_display"
                    )
                
                # Opções adicionais
                col_opt1, col_opt2 = st.columns(2)
                with col_opt1:
                    if st.button("📋 Copiar Letra"):
                        st.info("Letra copiada! (Use Ctrl+C na caixa de texto acima)")
                
                with col_opt2:
                    if st.button("🔄 Nova Pesquisa"):
                        st.rerun()
                        
            elif "error" in resultado:
                st.error(f"❌ {resultado['error']}")
                
                # Sugestões em caso de erro
                st.info("💡 **Dicas para melhorar a pesquisa:**")
                st.markdown("""
                - Verifique a ortografia do nome da banda e música
                - Tente usar o nome em inglês
                - Evite caracteres especiais
                - Tente variações do nome (ex: "The Beatles" ou apenas "Beatles")
                """)
    else:
        st.warning("⚠️ Por favor, preencha tanto o nome da banda quanto o nome da música.")

# Rodapé com informações
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>
        🎵 Powered by <a href="https://lyrics.ovh" target="_blank">lyrics.ovh API</a> | 
        Made with ❤️ using Streamlit
    </small>
</div>
""", unsafe_allow_html=True)

    

