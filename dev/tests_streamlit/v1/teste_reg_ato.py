import requests
import streamlit as st
import os
import json
import pandas as pd
from io import StringIO

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

st.title("📊 Editor de Registro de Ato Societário")
st.markdown("*Sistema para edição e gerenciamento de dados societários*")

# Adicionar função para processar JSON
def processar_json_societario(dados_json):
    """
    Processa dados JSON de ato societário e retorna DataFrames editáveis
    """
    try:
        if isinstance(dados_json, str):
            dados = json.loads(dados_json)
        else:
            dados = dados_json
        
        # DataFrame principal da empresa
        info_empresa = {
            'Campo': ['Nome da Empresa', 'CNPJ', 'NIRE', 'Endereço', 'CEP'],
            'Valor': [
                dados.get('company_name', ''),
                dados.get('cnpj', ''),
                dados.get('nire', ''),
                dados.get('address', ''),
                dados.get('zip_code', '')
            ]
        }
        df_empresa = pd.DataFrame(info_empresa)
        
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
        
        return df_empresa, df_socios, df_novos, df_saindo, dados
        
    except Exception as e:
        st.error(f"Erro ao processar JSON: {str(e)}")
        return None, None, None, None, None

def exportar_dados_modificados(df_empresa, df_socios, df_novos, df_saindo, dados_originais):
    """
    Converte os DataFrames modificados de volta para JSON
    """
    try:
        # Reconstruir dados da empresa
        dados_modificados = dados_originais.copy()
        
        # Atualizar informações da empresa
        if not df_empresa.empty:
            for idx, row in df_empresa.iterrows():
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
        
    except Exception as e:
        st.error(f"Erro ao exportar dados: {str(e)}")
        return None

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

# Sidebar para navegação
st.sidebar.title("📋 Menu")
opcao = st.sidebar.selectbox(
    "Escolha uma funcionalidade:",
    ["🏢 Editor de Atos Societários", "🎵 Pesquisador de Letras"]
)

if opcao == "🏢 Editor de Atos Societários":
    st.header("📊 Editor de Dados Societários")
    
    # Opções de entrada de dados
    tab1, tab2, tab3 = st.tabs(["📁 Upload JSON", "✏️ Colar JSON", "📄 Exemplo"])
    
    with tab1:
        st.subheader("Upload de arquivo JSON")
        arquivo_json = st.file_uploader(
            "Faça upload do arquivo JSON:",
            type=['json'],
            help="Selecione um arquivo JSON com dados societários"
        )
        
        if arquivo_json is not None:
            try:
                dados_json = json.loads(arquivo_json.read().decode('utf-8'))
                st.success("✅ Arquivo carregado com sucesso!")
                
                # Processar dados
                df_empresa, df_socios, df_novos, df_saindo, dados_originais = processar_json_societario(dados_json)
                
                if df_empresa is not None:
                    # Exibir dados editáveis
                    st.subheader("🏢 Informações da Empresa")
                    df_empresa_editado = st.data_editor(
                        df_empresa,
                        width="stretch",
                        num_rows="dynamic",
                        key="empresa_editor"
                    )
                    
                    if not df_socios.empty:
                        st.subheader("👥 Sócios da Empresa")
                        df_socios_editado = st.data_editor(
                            df_socios,
                            width="stretch",
                            num_rows="dynamic",
                            key="socios_editor"
                        )
                    
                    if not df_novos.empty:
                        st.subheader("➕ Novos Sócios")
                        df_novos_editado = st.data_editor(
                            df_novos,
                            width="stretch",
                            num_rows="dynamic",
                            key="novos_editor"
                        )
                    
                    if not df_saindo.empty:
                        st.subheader("➖ Sócios que Saem")
                        df_saindo_editado = st.data_editor(
                            df_saindo,
                            width="stretch",
                            num_rows="dynamic",
                            key="saindo_editor"
                        )
                    
                    # Botões de ação
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("💾 Salvar Alterações", width="stretch"):
                            try:
                                json_modificado = exportar_dados_modificados(
                                    df_empresa_editado,
                                    df_socios_editado if not df_socios.empty else pd.DataFrame(),
                                    df_novos_editado if not df_novos.empty else pd.DataFrame(),
                                    df_saindo_editado if not df_saindo.empty else pd.DataFrame(),
                                    dados_originais
                                )
                                
                                if json_modificado:
                                    st.session_state['json_modificado'] = json_modificado
                                    st.success("✅ Alterações salvas!")
                            except Exception as e:
                                st.error(f"Erro ao salvar: {str(e)}")
                    
                    with col2:
                        if 'json_modificado' in st.session_state:
                            st.download_button(
                                label="📥 Download JSON",
                                data=st.session_state['json_modificado'],
                                file_name="ato_societario_modificado.json",
                                mime="application/json",
                                width="stretch"
                            )
                    
                    with col3:
                        if st.button("🔄 Resetar", width="stretch"):
                            st.rerun()
                    
                    # Prévia do JSON modificado
                    if 'json_modificado' in st.session_state:
                        with st.expander("👀 Prévia do JSON Modificado"):
                            st.code(st.session_state['json_modificado'], language='json')
                            
            except Exception as e:
                st.error(f"❌ Erro ao processar arquivo: {str(e)}")
    
    with tab2:
        st.subheader("Colar dados JSON")
        json_text = st.text_area(
            "Cole os dados JSON aqui:",
            height=200,
            placeholder='{"company_name": "Nome da Empresa", "cnpj": "12.345.678/0001-99", ...}'
        )
        
        if st.button("📊 Processar JSON Colado") and json_text.strip():
            try:
                dados_json = json.loads(json_text)
                df_empresa, df_socios, df_novos, df_saindo, dados_originais = processar_json_societario(dados_json)
                
                if df_empresa is not None:
                    st.success("✅ JSON processado com sucesso!")
                    # Mesmo código de edição que acima...
                    
            except json.JSONDecodeError:
                st.error("❌ JSON inválido. Verifique a sintaxe.")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    
    with tab3:
        st.subheader("📄 Exemplo de JSON")
        exemplo_json = {
            "company_name": "EXEMPLO LTDA",
            "cnpj": "12.345.678/0001-99",
            "nire": "123456789",
            "address": "Rua Exemplo, 123, São Paulo, SP",
            "zip_code": "01234-567",
            "partners": [
                {
                    "partner_name": "JOÃO SILVA",
                    "cpf_cnpj": "123.456.789-00",
                    "participation_value": "R$1.000,00",
                    "qualification": "Sócio-Administrador"
                }
            ],
            "new_partners": ["MARIA SANTOS"],
            "leaving_partners": ["PEDRO OLIVEIRA"]
        }
        
        st.code(json.dumps(exemplo_json, indent=2, ensure_ascii=False), language='json')
        
        if st.button("🧪 Testar com Exemplo"):
            df_empresa, df_socios, df_novos, df_saindo, dados_originais = processar_json_societario(exemplo_json)
            st.success("✅ Exemplo carregado! Veja as abas acima para editar.")

elif opcao == "🎵 Pesquisador de Letras":
    st.header("🎵 Pesquisador de Letras de Música")
    
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
        pesquisar = st.button("🔍 Pesquisar Letra", width="stretch")
        
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



    

