from cProfile import label
from calendar import c
from email.policy import default
from logging import PlaceHolder
from tkinter import Place
from altair import value
from narwhals import col
import numpy as np
from numpy.random import default_rng as rng
import streamlit as st
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import os
from PIL import Image, ImageDraw
import io
import json
import time

def create_test_image():
    """Cria uma imagem simples programaticamente para teste"""
    try:
        # Criar uma imagem 400x300 com fundo azul
        img = Image.new('RGB', (400, 300), color='#0066CC')
        
        # Adicionar texto à imagem
        draw = ImageDraw.Draw(img)
        
        # Desenhar algumas formas básicas
        draw.rectangle([50, 50, 350, 250], outline='white', width=3)
        draw.ellipse([100, 100, 300, 200], fill='white', outline='#0066CC')
        
        # Adicionar texto (sem fonte específica para evitar dependências)
        draw.text((150, 140), "Imagem de Teste", fill='#0066CC')
        draw.text((180, 160), "Streamlit", fill='#0066CC')
        
        # Converter para bytes para o Streamlit
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        st.image(img_buffer, caption="Imagem criada programaticamente", width=400)
        st.success("✅ Imagem criada com sucesso!")
        
    except Exception as e:
        st.error(f"Erro ao criar imagem programaticamente: {str(e)}")
        # Último recurso: usar placeholder online
        st.info("Usando placeholder online como último recurso")
        st.image("https://via.placeholder.com/400x300/0066CC/FFFFFF?text=Streamlit+Test", 
                caption="Placeholder Online")



# Sidebar section
st.sidebar.title("Sidebar de Teste")
st.sidebar.write("Conteúdo da sidebar")
st.sidebar.markdown("Markdown na sidebar")
sidebar_input = st.sidebar.text_input(label="Input na sidebar", value="Texto padrão")

# Sidebar para navegação
st.sidebar.header("Navegação")
num_opcoes = 5
opcoes = [f"Opção {i}" for i in range(1, num_opcoes + 1)]
opcao_selecionada = st.sidebar.selectbox("Selecione uma opção:", options=opcoes)

# Funções de renderização
def render_opcao1():
    st.write("Conteúdo da Opção 1")
    st.title("Teste Streamlit")
    st.header("Header de Teste")
    st.subheader("Subheader de Teste")
    st.markdown("Este é um teste de arquivo Streamlit.")
    st.caption("Descrição do teste.")

    st.divider()

    st.write("Teste de escrita")
    st.write("Teste de escrita", "Teste de escrita")
    st.write("Teste de escrita", "Teste de escrita", "Teste de escrita")

    st.divider()

    st.code("print('Hello, World!')", language="python")
    st.text("Texto simples")

    st.divider()

    st.latex(r"e^{i\pi} - 1 = 0")

    st.error("Teste de erro")
    st.warning("Teste de aviso")
    st.info("Teste de informação")
    st.success("Teste de sucesso")
    st.exception(Exception("Teste de exceção"))

    st.divider()

    # Verificar e carregar imagem local
    image_path = os.path.join(os.path.dirname(__file__), "Prancheta.jpg")

    # Verificar se o arquivo existe e é válido
    if os.path.exists(image_path):
        try:
            st.image(image_path, caption="Imagem Local - Prancheta.jpg")
        except Exception as e:
            st.error(f"Erro ao carregar imagem local: {str(e)}")
            st.info(f"Caminho do arquivo: {image_path}")
            if os.path.exists(image_path):
                st.info(f"Tamanho do arquivo: {os.path.getsize(image_path)} bytes")
            
            # Criar uma imagem simples programaticamente como fallback
            st.info("Criando imagem de teste programaticamente como alternativa")
            create_test_image()
    else:
        st.error(f"Arquivo de imagem não encontrado: {image_path}")
        st.info("Criando imagem de teste programaticamente como alternativa")
        create_test_image()
        
    st.divider()

    st.image(os.path.join(os.path.dirname(__file__), '[CSG] Capa LI Colaboradores.png'), caption="Imagem com caminho dinâmico")

    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", caption="Logo Streamlit")

    st.divider()

    st.video("https://www.youtube.com/watch?v=JwSS70SZdyM")

    st.divider()

    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

    st.divider()

    #st.balloons()
    #st.snow()

    st.divider()

    st.tabs(["Tab 1", "Tab 2", "Tab 3"])

    st.divider()

    st.button("Botão de Teste")
    st.checkbox("Checkbox de Teste")
    st.radio("Radio de Teste", ["Opção 1", "Opção 2", "Opção 3"])

    st.selectbox("Selectbox de Teste", ["Opção A", "Opção B", "Opção C"])
    st.multiselect("Multiselect de Teste", ["Item 1", "Item 2", "Item 3", "Item 4"])
    st.slider("Slider de Teste", 0, 100, 50)
    st.select_slider("Select Slider de Teste", ["Opção 1", "Opção 2", "Opção 3"])
    st.text_input("Text Input de Teste", "Texto padrão")
    st.text_area("Text Area de Teste", "Texto padrão\nMultilinha")
    st.number_input("Number Input de Teste", 0, 100, 50)
    st.date_input("Date Input de Teste")
    st.time_input("Time Input de Teste")
    st.file_uploader("File Uploader de Teste")
    st.color_picker("Color Picker de Teste", "#00f900")
    st.metric("Metric de Teste", 42, -3)
    
    # Progress Bar interativo com slider
    st.write("Progress Bar interativo:")
    progress_value = st.slider("Ajuste o progresso:", 0, 100, 70, key="progress_slider")
    st.progress(progress_value / 100.0)
    st.caption(f"Progresso atual: {progress_value}%")

    st.divider()



    """ st.spinner("Spinner de Teste")
    st.stop() """


    st.form("Formulário de Teste")
    with st.form("form_de_teste"):
        nome = st.text_input("Nome:")
        idade = st.number_input("Idade:", min_value=0, max_value=120, value=25)
        if st.form_submit_button("Enviar"):
            st.success(f"Formulário enviado! Nome: {nome}, Idade: {idade}")


    st.divider()

    st.header("Data Elements")
    st.subheader("DataFrame de Teste")

    # Data frame section
    df = pd.DataFrame({
        'Nome': ["Alex", "Bob", "Charlie", "David", "Eve"],
        'Idade': [25, 30, 35, 40, 45],
        'Cidade': ["New York", "London", "Paris", "Tokyo", "Sydney"],
        'Data de Cadastro': pd.date_range(start='2023-01-01', periods=5, freq='YE'),
        'Matricula': [1122003300, 1122003301, 1122003302, 1122003303, 1122003304],
        'Emprego': ["Estágio", "Pleno", "Sênior", "Estágio", "Pleno"],
        'Ativo': [True, False, True, False, True]
    })

    st.dataframe(df.sort_values('Idade'), width='stretch', height=400)

    # Data frame editor
    st.subheader("Data Editor de Teste")
    edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor_teste")

    # Static table section
    st.subheader("Tabela Estática de Teste")
    st.table(df)

    # Metric section
    st.subheader("Métricas de Teste")
    st.metric(label="Total de Usuários", value=len(df), help="Quantidade de usuários cadastrados", delta="+5%")
    st.metric(label="Usuários Ativos", value=df['Ativo'].sum(), help="Quantidade de usuários ativos", delta="-2%")
    st.metric(label="Idade Média", value=f"{df['Idade'].mean():.1f}", help="Média de idade dos usuários", delta="+0.5")

    # JSON and Dict section
    st.subheader("JSON e Dicionário de Teste")
    sample_dict = {
        "nome": "Alice",
        "idade": 28,
        "cidade": "São Paulo",
        "habilidades": ["Python", "Data Science", "Machine Learning"],
        "emprego": {
            "empresa": "Tech Corp",
            "cargo": "Data Scientist",
            "anos_experiencia": 5
        }
    }
    st.json(sample_dict)
    st.write("Dicionário de Teste", sample_dict)
    st.write("Dicionário como tabela", pd.DataFrame([sample_dict]))

    complex_dict = {
        "usuarios": {"Nome": ["Alice", "Bob", "Charlie"], 
                    "idade": [25, 30, 35],
                    "cidade": ["São Paulo", "New York", "London"],
                    "emprego": ["Estágio", "Pleno", "Sênior"],
                    "ativo": [True, False, True],
                    "matricula": [1122003300, 1122003301, 1122003302],
                    "data_cadastro": ["2023-01-01", "2023-02-01", "2023-03-01"]},
        "detalhes": {
            "idade": [25, 30, 35],
            "cidade": ["São Paulo", "New York", "London"],
            "emprego": ["Estágio", "Pleno", "Sênior"],
            "ativo": [True, False, True],
            "matricula": [1122003300, 1122003301, 1122003302],
            "data_cadastro": ["2023-01-01", "2023-02-01", "2023-03-01"]
        }
    }
    st.write("Dicionário complexo de teste", complex_dict)
    st.write("Dicionário complexo como tabela", pd.DataFrame(complex_dict["usuarios"]))
    st.write("Dicionário detalhes como tabela", pd.DataFrame(complex_dict["detalhes"]))

    st.json(complex_dict)

    st.divider()

    st.header("Charts de Teste")

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )

    chart_data.index = pd.date_range(start='2023-01-01', periods=20, freq='D')
    chart_data = chart_data.cumsum()

    chart_data_2 = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )

    # Line chart Section
    st.subheader("Line Chart de Teste")
    st.line_chart(chart_data_2, x_label="char_data_2", y_label="valores", width=700, height=300)
    st.line_chart(chart_data, width='stretch', height=300)

    # Area chart Section
    st.subheader("Area Chart de Teste")
    st.area_chart(chart_data_2, x_label="char_data_2", y_label="valores", width=700, height=300)
    st.area_chart(chart_data, width='stretch', height=300)

    # Bar chart Section
    st.subheader("Bar Chart de Teste")
    st.bar_chart(chart_data_2, x_label="char_data_2", y_label="valores", width=700, height=300)
    st.bar_chart(chart_data, width='stretch')

    # Scatter plot Section
    st.subheader("Scatter Plot de Teste")
    st.scatter_chart(chart_data_2, x_label="char_data_2", y_label="valores", width=700, height=300)
    st.scatter_chart(chart_data, width='stretch')

    # Map Section (displayying random points on a map)
    st.subheader("Mapa de Teste")
    st.map(pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon']), zoom=10, width=700)

    # Pyplot Section
    st.subheader("Pyplot de Teste")
    fig, ax = plt.subplots()
    ax.plot(chart_data.index, chart_data_2['a'], label='A')
    ax.plot(chart_data.index, chart_data_2['b'], label='B')
    ax.plot(chart_data.index, chart_data_2['c'], label='C')
    ax.set_xlabel("Data")
    ax.set_ylabel("Valores")
    ax.set_title("Gráfico de Linhas")
    ax.legend()
    st.pyplot(fig, width='stretch', clear_figure=True)


    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig2, ax2 = plt.subplots()
    ax2.plot(x, y)
    st.pyplot(fig2, width='stretch', clear_figure=True)

    """ # using the variable axs for multiple Axes
    fig2, axs2 = plt.subplots(2, 2)

    # using tuple unpacking for multiple Axes
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2) 

    # Create just a figure and only one subplot
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Simple plot')

    # Create two subplots and unpack the output array immediately
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.plot(x, y)
    ax1.set_title('Sharing Y axis')
    ax2.scatter(x, y)

    # Create four polar Axes and access them through the returned array
    fig, axs = plt.subplots(2, 2, subplot_kw=dict(projection="polar"))
    axs[0, 0].plot(x,axs[1, 1].scatter(x, y))

    # Share a X axis with each column of subplots
    plt.subplots(2, 2, sharex='col')

    # Share a Y axis with each row of subplots
    plt.subplots(2, 2, sharey='row')

    # Share both X and Y axes with all subplots
    plt.subplots(2, 2, sharex='all', sharey='all')

    # Note that this is the same as
    plt.subplots(2, 2, sharex=True, sharey=True)

    # Create figure number 10 with a single subplot
    # and clears it if it already exists.
    fig, ax = plt.subplots(num=10, clear=True)"""

    st.divider()

    # Form to hold the interactive elements
    st.title("Formulário Interativo de Teste")

    with st.form(key="form_interativo"):
        
        # Text inputs
        st.subheader("Text Inputs")
        nome = st.text_input("Nome:")
        feedback = st.text_area("Feedback:")
        
        # Numeric inputs
        st.subheader("Numeric Inputs")
        idade = st.number_input("Idade:", min_value=0, max_value=120, value=25)
        salario = st.number_input("Salário:", min_value=0.0, value=50000.0, step=1000.0, format="%.2f")
        
        # Date and time inputs
        st.subheader("Date and Time Inputs")
        data_evento = st.date_input("Data do Evento:")
        horario_evento = st.time_input("Hora do Evento:")
        
        # Selection inputs
        cidade = st.selectbox("Cidade:", ["São Paulo", "New York", "London", "Tokyo", "Sydney"])
        habilidades = st.multiselect("Habilidades:", ["Python", "Data Science", "Machine Learning", "Web Development", "DevOps"])
        emprego = st.radio("Nível de Emprego:", ["Estágio", "Pleno", "Sênior"])
        
        intervalo = st.slider("Intervalo de Teste:", 0, 100, (25, 75))
        
        # Toggle switch and checkbox
        st.subheader("Toggle Switch")
        ativo = st.toggle("Ativo")
        ativo = st.checkbox("Ativo")
        
        # Submit button
        if st.form_submit_button("Enviar"):
            st.success(f"Formulário enviado! Nome: {nome}, Idade: {idade}, Cidade: {cidade}, Habilidades: {', '.join(habilidades)}, Emprego: {emprego}, Ativo: {ativo}, Intervalo: {intervalo}")
            
            
    #Simple form example

    st.title("Exemplo Simples de Formulário")

    form_values = {
        "nome": None,
        "idade": None,
        "sexo": None,
        "cidade": None,
        "data_nascimento": None
    }

    min_date = datetime.date(1900, 1, 1)
    max_date = datetime.date.today()

    with st.form(key="form_simples"):
        form_values["nome"] = st.text_input("Nome:")
        form_values["idade"] = st.slider("Idade:", min_value=0, max_value=120, value=25)
        form_values["sexo"] = st.selectbox("Sexo:", ["Masculino", "Feminino", "Outro"])
        form_values["cidade"] = st.text_input("Cidade:")
        form_values["data_nascimento"] = st.date_input("Data de Nascimento:", min_value=min_date, max_value=max_date)

        submit_button = st.form_submit_button(label="Enviar", width='stretch')
        if submit_button:
            try:
                if not all(form_values.values()):
                    st.error("Por favor, preencha todos os campos.")
                else:
                    st.success(f"Formulário enviado! Valores: {form_values}")
                    st.balloons()
                    for key, value in form_values.items():
                        st.write(f"**{key.capitalize()}**: {value}")
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
                
                
    # Advance form example
    st.title("Exemplo Avançado de Formulário")


    with st.form(key="form_avancado", clear_on_submit=True):
        st.subheader("Informações Pessoais")
        nome = st.text_input("Nome Completo:")
        email = st.text_input("Email:")
        telefone = st.text_input("Telefone:")
        data_aniversario = st.date_input("Data de Aniversário:", min_value=min_date, max_value=max_date)
        if data_aniversario:
            idade = max_date.year - data_aniversario.year 
            if data_aniversario.month > max_date.month or (data_aniversario.month == max_date.month and data_aniversario.day > max_date.day):
                idade -= 1
            st.write(f"Idade calculada: {idade} anos")
        
        st.subheader("Endereço")
        rua = st.text_input("Rua:")
        cidade = st.text_input("Cidade:")
        estado = st.text_input("Estado:")
        cep = st.text_input("CEP:")
        
        st.subheader("Preferências")
        contato_preferido = st.selectbox("Método de Contato Preferido:", ["Email", "Telefone", "WhatsApp"])
        interesses = st.multiselect("Interesses:", ["Tecnologia", "Esportes", "Música", "Viagens", "Leitura"])
        
        receber_newsletter = st.checkbox("Deseja receber nossa newsletter?")
        
        if st.form_submit_button(label="Enviar", width='stretch'):
            try:
                if not all([nome, email, telefone, data_aniversario, rua, cidade, estado, cep, contato_preferido, interesses, receber_newsletter]):
                    st.error("Por favor, preencha todos os campos obrigatórios.")
                else:
                    st.success(f"Formulário avançado enviado! Nome: {nome}, Email: {email}, Telefone: {telefone}, Rua: {rua}, Cidade: {cidade}, Estado: {estado}, CEP: {cep}, Contato Preferido: {contato_preferido}, Interesses: {', '.join(interesses)}, Newsletter: {'Sim' if receber_newsletter else 'Não'}")
                    st.balloons()
                    st.write("### Resumo do Formulário")
                    st.write(f"- **Nome:** {nome}")
                    st.write(f"- **Email:** {email}")
                    st.write(f"- **Telefone:** {telefone}")
                    st.write(f"- **Data de Aniversário:** {data_aniversario} (Idade: {idade} anos)")
                    st.write(f"- **Endereço:** {rua}, {cidade}, {estado}, {cep}")
                    st.write(f"- **Contato Preferido:** {contato_preferido}")
                    st.write(f"- **Interesses:** {', '.join(interesses) if interesses else 'Nenhum'}")
                    st.write(f"- **Receber Newsletter:** {'Sim' if receber_newsletter else 'Não'}")
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
                
                
    st.divider()

    # Session State example
    st.title("Exemplo de Session State")

    counter = 0
    counter_persistente = 0

    st.write(f"Contador padrão: {counter}")
    if st.button(key="Incrementar Contador",label="Incrementar Contador"):
        counter += 1
        st.write(f"Contador padrão: {counter}")
    else:
        st.write("Contador não incrementado.")
        
    # Using session state to persist counter value
    if 'counter_persistente' not in st.session_state:
        st.session_state.counter_persistente = 0

    st.write(f"Contador Persistente: {st.session_state.counter_persistente}")
    if st.button(key="Incrementar Contador persistente",label="Incrementar Contador persistente"):
        st.session_state.counter_persistente += 1
        st.write(f"Contador Persistente: {st.session_state.counter_persistente}")
    else:
        st.write(f"Contador Persistente: {st.session_state.counter_persistente}.")
        
    if st.button("Resetar Contador persistente"):
        st.session_state.counter_persistente = 0
        st.write(f"Contador Persistente resetado: {st.session_state.counter_persistente}")
        
    # Using session state to persist counter value
    if 'counter_persistente' not in st.session_state:
        st.session_state.counter_persistente = 0

    # Using session state with text input
    if 'nome' not in st.session_state:
        st.session_state.nome = ""

    st.write(f"Nome: {st.session_state.nome}")
    st.text_input("Digite seu nome:", key="nome")
    st.write(f"Nome atualizado: {st.session_state.nome}")
    st.write("O nome persiste mesmo após interações, graças ao session state.")


    st.divider()

    # CallBacks section
    st.title("Exemplo de Callbacks")

    if "step" not in st.session_state:
        st.session_state.step = 1
        
    if "informacoes" not in st.session_state:
        st.session_state.informacoes = {}

    def etapa_1():
        try:
            st.session_state.step = 1
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

    def etapa_2(nome, idade):
        if nome and idade:
            st.session_state.informacoes["nome"] = nome
            st.session_state.informacoes["idade"] = idade
            st.session_state.step = 2
        else:
            st.error("Por favor, preencha todos os campos.")
    def etapa_3(email, telefone):
        if email and telefone:
            st.session_state.informacoes["email"] = email
            st.session_state.informacoes["telefone"] = telefone
            st.session_state.step = 3
        else:
            st.error("Por favor, preencha todos os campos.")

    if st.session_state.step == 1:
        st.header("Passo 1: Informações Básicas")
        nome = st.text_input(label="Nome:", value=st.session_state.informacoes.get("nome", ""))
        idade = st.number_input(label="Idade:", min_value=0, max_value=120, value=st.session_state.informacoes.get("idade", 25))

        st.button(label="Etapa 2",on_click=etapa_2, args=(nome, idade), width='stretch')
            
    if st.session_state.step == 2:
        st.header("Passo 2: Contato")
        email = st.text_input(label="Email:", value=st.session_state.informacoes.get("email", ""))
        telefone = st.number_input(label="Telefone:", value=st.session_state.informacoes.get("telefone", 0), step=1)

        st.button(label="Etapa 1", on_click=etapa_1, width='stretch')
        st.button(label="Etapa 3", on_click=etapa_3, args=(email, telefone), width='stretch')

    if st.session_state.step == 3:
        st.header("Passo 3: Confirmação")
        st.write("Por favor, confirme suas informações:")
        for key, value in st.session_state.informacoes.items():
            st.write(f"- **{key.capitalize()}**: {value}")

        st.button(label="Anterior", on_click=lambda: setattr(st.session_state, "step", 2))

        st.button(label="Enviar", on_click=lambda: [st.success("Formulário enviado com sucesso!"), st.balloons(), setattr(st.session_state, "step", 1), setattr(st.session_state, "informacoes", {})])
        
        
    st.divider()

    # Layout section
    st.title("Exemplo de Layout")


    st.title("Tab de Teste")
    st.write("Podemos adicionar vários elementos na sidebar, assim como na área principal.")

    num_tabs = 5
    tab_labels = [f"Tab {i}" for i in range(1, num_tabs + 1)]
    tabs = st.tabs(tab_labels)
    for i, tab in enumerate(tabs):
        with tab:
            st.header(f"Header da {tab_labels[i]}")
            st.subheader(f"Subheader da {tab_labels[i]}")
            st.title(f"Conteúdo da {tab_labels[i]}")
            st.write(f"Conteúdo da {tab_labels[i]}")


    # Colunas layout
    num_cols = 3
    col_labels = [f"Coluna {i}" for i in range(1, num_cols + 1)]
    cols = st.columns(num_cols)
    for i, col in enumerate(cols):
        with col:
            st.header(col_labels[i])
            st.write(f"Conteúdo da {col_labels[i]}")
            st.button(f"Botão na {col_labels[i]}")

    # Expander layout
    num_expanders = 3
    expander_labels = [f"Expander {i}" for i in range(1, num_expanders + 1)]
    for i in range(1, num_expanders + 1):
        with st.expander(f"Expander {i}"):
            st.header(f"Header do {expander_labels[i-1]}")
            st.write(f"Conteúdo do {expander_labels[i-1]}")
            st.button(f"Botão no {expander_labels[i-1]}")
            
    st.divider()

def render_opcao2():
    st.header("Conteúdo da Opção 2")
    
    # Exemplo de atualização dinâmica de conteúdo
    st.write("Clique no botão abaixo para atualizar o conteúdo dinamicamente.")
    
    placeholder = st.empty()
    if placeholder.button(label="Clique para atualizar o conteúdo"):
        placeholder.write("Conteúdo atualizado!")
        
    st.divider()
    
    # Expander exemplo
    st.write("Exemplo de Expander:")
    with st.expander(label="Expander"):
        st.write("Conteúdo dentro do expander.")
        
        #PopOver exemplo
        st.write("Exemplo de Popover:")
        st.button("Passe o mouse para ver o popover", help="Este é um popover de exemplo.")
    
    # Exemplo de tabela dinâmica
    st.write("Exemplo de tabela dinâmica:")
    data = {"Coluna 1": [1, 2, 3], "Coluna 2": ["A", "B", "C"]}
    df = pd.DataFrame(data)
    st.data_editor(df)
        
    st.divider()
    
    # Exemplo de barra de progresso controlada
    st.write("Exemplo de barra de progresso:")
    
    # Botão para iniciar o progress bar
    if st.button("🚀 Iniciar Progress Bar", key="start_progress_1"):
        progress_container = st.empty()
        status_text = st.empty()
        
        # Criar progress bar
        progress_bar = progress_container.progress(0)
        
        for i in range(101):
            # Atualizar o progress bar
            progress_bar.progress(i)
            # Atualizar texto de status
            status_text.text(f"Processando... {i}%")
            time.sleep(0.05)  # Reduzir tempo para ser mais rápido
            
        # Finalizar
        status_text.success("✅ Progress Bar concluído com sucesso!")
        time.sleep(1)
        progress_container.empty()  # Limpar o progress bar após conclusão
        
    st.divider()
    
    # Exemplo de slider interativo
    st.write("Exemplo de slider interativo:")
    slider_value = st.slider("Selecione um valor:", 0, 100, 50)
    st.write(f"Valor selecionado: {slider_value}")
    
    st.divider()
    
    # Seção avançada de Progress Bars
    st.write("### 🎯 Progress Bars Avançados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Progress Bar com Simulação de Download**")
        if st.button("📥 Simular Download", key="simulate_download"):
            files = ["arquivo1.pdf", "arquivo2.xlsx", "arquivo3.png", "arquivo4.docx", "arquivo5.zip"]
            download_container = st.empty()
            
            for idx, file in enumerate(files):
                with download_container.container():
                    st.write(f"Baixando: {file}")
                    progress = st.progress(0)
                    
                    # Simular download do arquivo
                    for percent in range(101):
                        progress.progress(percent / 100)
                        time.sleep(0.02)
                    
                    st.success(f"✅ {file} baixado!")
                    time.sleep(0.5)
            
            download_container.success("🎉 Todos os arquivos baixados com sucesso!")
    
    with col2:
        st.write("**Progress Bar Multi-etapa**")
        if st.button("🔄 Processo Multi-etapa", key="multi_step"):
            steps = [
                ("🔍 Verificando dados", 20),
                ("📊 Processando informações", 40), 
                ("💾 Salvando resultados", 30),
                ("✅ Finalizando processo", 10)
            ]
            
            multi_container = st.empty()
            total_progress = st.progress(0)
            current_progress = 0
            
            for step_name, step_duration in steps:
                with multi_container.container():
                    st.info(step_name)
                    step_progress = st.progress(0)
                    
                    for i in range(step_duration):
                        step_progress.progress((i + 1) / step_duration)
                        current_progress += 1
                        total_progress.progress(current_progress / 100)
                        time.sleep(0.05)
                    
                    st.success(f"{step_name} - Concluído!")
                    time.sleep(0.3)
            
            multi_container.success("🚀 Processo completo finalizado!")
    
    # Exemplo de gráfico interativo
    st.write("Exemplo de gráfico interativo:")
    chart_data = pd.DataFrame(np.random.randn(50, 3), columns=["A", "B", "C"])
    st.line_chart(chart_data)
    st.bar_chart(chart_data)
    
    # Handling user inputs in sidebar
    if sidebar_input:
        st.write(f"Você digitou: {sidebar_input}")

def render_opcao3():
    

    
    st.title("Conteúdo da Opção 3")
    st.header("Advance Widgets Test")
    st.write("Exemplo de widget avançado:")

    st.button(label="Clique aqui",key="botao_avancado")
    
    st.divider()
    
    # Toggle switch
    st.write("Exemplo de toggle switch:")
    
    
    if "checkbox_avancado" not in st.session_state:
        st.session_state.checkbox_avancado = False
        

    st.checkbox(label="Marque esta caixa", key="checkbox_avancado", help="Este é um checkbox de exemplo.")

    if st.session_state.checkbox_avancado:
        st.success("Checkbox está marcado!")
        user_input = st.text_input(label="Digite algo:", key="input_avancado", placeholder="Digite aqui...",value=st.session_state.get("input_avancado", ""))
        st.write(f"Você digitou: {user_input}")
    else:
        # Não renderiza o campo, mas mantém o valor no session_state
        user_input = st.session_state.get("input_avancado", "")
        st.write(f"Você digitou: {user_input}")

   # Slider do valor mínimo

    min_value = st.slider(label="Selecione o valor mínimo:", min_value=0, max_value=50, value=25, key="min_value_avancado")

    # Slider principal, sempre respeitando o mínimo
    valor = st.slider(
        label="Selecione um valor:",
        min_value=0,
        max_value=100,
        value=max(min_value, st.session_state.get("min_value_avancado", min_value)),
        key="slider_avancado"
    )
    if st.session_state.slider_avancado < min_value:
        st.session_state.slider_avancado = min_value

    st.write(f"Valor selecionado: {valor}")
    
    st.divider()

    st.selectbox(label="Selecione uma opção:", options=["Opção 1", "Opção 2", "Opção 3"], key="selectbox_avancado")
    
    st.radio(label="Escolha uma opção:", options=["Opção A", "Opção B", "Opção C"], key="radio_avancado")
    st.multiselect(label="Selecione múltiplas opções:", options=["Item 1", "Item 2", "Item 3", "Item 4"], key="multiselect_avancado")
    st.text_input(label="Digite algo:", value="Texto padrão", key="text_input_avancado")
    st.date_input(label="Selecione uma data:", key="date_input_avancado")
    st.time_input(label="Selecione uma hora:", key="time_input_avancado")
    
    
    st.divider()
    
    # CACHING section
    st.title("Exemplo de Caching")
    @st.cache_data(ttl=60) #Cache por 60 segundos
    def fetch_data():
        time.sleep(2)  # Simula uma operação demorada
        return {"data": "Dados carregados com cache!",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    st.write("Clique no botão abaixo para carregar os dados com cache.")
    if st.button(label="Carregar Dados com Cache", key="botao_cache"):
        data = fetch_data()
        print(type(data))
        
        
        json_string = json.dumps(data)
        st.write(json_string)
        print(type(json_string))
        
        json_data = json.loads(json_string)
        print(type(json_data))
        st.write(json_data)
        st.write(f"json_data: {json_data}") # print(json_data)

        st.write(f"data: {data}") # print(data)
        st.write(f"fetch_data()['data']: {fetch_data()['data']}") # print(fetch_data()['data'])
        st.write(f"fetch_data()['timestamp']: {fetch_data()['timestamp']}") # print(fetch_data()['timestamp'])

    st.divider()
    
    
    # Caching Resource
    file_path = "test.txt"
    
    st.title("Exemplo de Caching Resource")
    @st.cache_resource
    def get_file_handler():
        file = open(os.path.join(os.path.dirname(__file__), "[CSG] Capa LI Colaboradores.png"), "rb")
        return file
    
    file_handler = get_file_handler()
    st.download_button(label="Baixar Capa", data=file_handler, file_name="[CSG] Capa LI Colaboradores.png", mime="image/png")
    
    # Escrever no arquivo
    if st.button(label="Escrever no arquivo", key="botao_escrever_arquivo"):
        with open(file_path, "a", encoding="utf-8") as file:
            file.write("Texto para escrever no arquivo.\n")
            file.write(f"Escrito em: {datetime.datetime.now()}\n")
        st.success("Texto escrito no arquivo com sucesso!")

    # Ler o arquivo
    if st.button(label="Ler o arquivo", key="botao_ler_arquivo"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            st.write(f"Conteudo do arquivo:\n{content}")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

    st.divider()

    st.title("Counter exemplo com Imediate run")
    if "counter_imediate" not in st.session_state:
        st.session_state.counter_imediate = 0
    def increment_and_rerun():
        st.session_state.counter_imediate += 1
        st.rerun()
    st.write(f"Contador Imediate: {st.session_state.counter_imediate}")
    st.button("Incrementar Contador Imediate", on_click=increment_and_rerun)
        

def render_opcao4():
    st.title("Conteúdo da Opção 4")
    st.header("Este é um exemplo de fragmento.")
    st.subheader("Fragmentos ajudam a organizar o código.")
    st.write("Eles podem ser reutilizados em diferentes partes do aplicativo.")
    
    @st.fragment()
    def fragment_example():
        
        cols = st.columns(2)
        cols[0].toggle(label="Toggle", key="toggle_fragment_col1", label_visibility="visible")
        cols[0].toggle(label="Toggle 2", key="toggle_fragment_col1_2", label_visibility="visible")
        cols[0].toggle(label="Toggle 3", key="toggle_fragment_col1_3", label_visibility="visible")
        cols[1].text_area(label="Text Area", placeholder="Texto padrão", key="text_area_fragment_col2", label_visibility="visible")
        st.file_uploader(label="File Uploader", key="file_uploader_fragment", label_visibility="visible")
        
    @st.fragment()
    def another_fragment():
        num_colunas = 2
        colunas = st.columns(num_colunas)
        for i, coluna in enumerate(colunas):
            with coluna:
                st.subheader(f"Conteúdo da Coluna {i+1} dentro do fragmento.")
                st.button(label=f"Botão na Coluna {i+1}")

    @st.fragment()
    def progress_bar_fragment():
        st.write("### Progress Bar com Fragment")
        
        # Botão para iniciar o progress bar fragmentado
        if st.button("🎯 Iniciar Progress Fragment", key="start_progress_fragment"):
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            # Criar progress bar dentro do fragment
            with progress_placeholder.container():
                progress_bar = st.progress(0)
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    status_placeholder.info(f"Fragment Progress: {i + 1}/100")
                    time.sleep(0.03)  # Mais rápido para melhor UX
                    
            status_placeholder.success("🎉 Fragment Progress concluído!")
            time.sleep(1)
            progress_placeholder.empty()  # Limpar após conclusão
    
    st.divider()
    
    progress_bar_fragment()
    fragment_example()
    cols = st.columns(2)
    st.selectbox(label="Select", options=["Opção 1", "Opção 2", "Opção 3"], key="selectbox_out_fragment_col1", label_visibility="visible")
    st.button(label="Update", key="button_out_fragment_col2", width='stretch')
    st.divider()  
    another_fragment()
    
    
def render_opcao5():
    st.title("Conteúdo da Opção 5")
    st.header("Este é um exemplo multi-página.")
    
    # Exemplo de multipáginas usando session state (método simples)
    st.subheader("🔧 Método 1: Multipáginas com Session State")
    
    # Inicializar estado da página
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    # Menu de navegação
    st.write("**Menu de Navegação:**")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Home", key="nav_home"):
            st.session_state.current_page = 'Home'
    with col2:
        if st.button("👤 Perfil", key="nav_profile"):
            st.session_state.current_page = 'Perfil'
    with col3:
        if st.button("📊 Dashboard", key="nav_dashboard"):
            st.session_state.current_page = 'Dashboard'
    with col4:
        if st.button("⚙️ Configurações", key="nav_settings"):
            st.session_state.current_page = 'Configurações'
    with col5:
        if st.button("ℹ️ Sobre", key="nav_about"):
            st.session_state.current_page = 'Sobre'
    
    st.divider()
    
    # Renderizar página atual
    render_current_page()
    
    st.divider()
    
    # Exemplo de navegação com selectbox
    st.subheader("🎯 Método 2: Navegação com Selectbox")
    
    page_options = ["Home", "Perfil", "Dashboard", "Configurações", "Sobre"]
    selected_page = st.selectbox(
        "Selecione uma página:",
        page_options,
        index=page_options.index(st.session_state.current_page),
        key="page_selector"
    )
    
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()
    
    st.divider()
    
    # Informações sobre st.navigation para arquivos separados
    st.subheader("📁 Método 3: st.navigation (Arquivos Separados)")
    st.info("""
    Para usar `st.navigation()` com arquivos separados, você precisa:
    1. Criar arquivos Python separados (ex: page1.py, page2.py)
    2. Cada arquivo deve conter o conteúdo da página
    3. Usar st.navigation() para navegar entre eles
    
    Exemplo de estrutura:
    ```
    projeto/
    ├── main.py (arquivo principal)
    ├── pages/
    │   ├── page1.py
    │   ├── page2.py
    │   └── page3.py
    ```
    """)
    
    if st.button("🚀 Criar Exemplo de Multipáginas Separadas", key="create_multipage"):
        create_multipage_example()

def render_current_page():
    """Renderiza a página atual baseada no session state"""
    
    current_page = st.session_state.current_page
    
    if current_page == 'Home':
        render_home_page()
    elif current_page == 'Perfil':
        render_profile_page()
    elif current_page == 'Dashboard':
        render_dashboard_page()
    elif current_page == 'Configurações':
        render_settings_page()
    elif current_page == 'Sobre':
        render_about_page()

def render_home_page():
    """Página Home"""
    st.markdown("## 🏠 Página Home")
    st.write("Bem-vindo à página inicial!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Usuários Ativos", "1,234", "+12%")
        st.metric("Vendas Hoje", "R$ 56.789", "+5%")
    with col2:
        st.metric("Novos Clientes", "89", "+23%")
        st.metric("Taxa de Conversão", "3.4%", "-0.2%")
    
    # Gráfico simples
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Vendas', 'Marketing', 'Suporte']
    )
    st.line_chart(chart_data)

def render_profile_page():
    """Página Perfil"""
    st.markdown("## 👤 Página Perfil")
    st.write("Gerencie suas informações pessoais")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo", value="João Silva")
            email = st.text_input("Email", value="joao@exemplo.com")
            telefone = st.text_input("Telefone", value="(11) 99999-9999")
        
        with col2:
            departamento = st.selectbox("Departamento", ["TI", "Vendas", "Marketing", "RH"])
            cargo = st.text_input("Cargo", value="Desenvolvedor")
            data_admissao = st.date_input("Data de Admissão")
        
        if st.form_submit_button("💾 Salvar Alterações"):
            st.success("Perfil atualizado com sucesso!")
            st.balloons()

def render_dashboard_page():
    """Página Dashboard"""
    st.markdown("## 📊 Dashboard")
    st.write("Visualize métricas e relatórios importantes")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Receita Total", "R$ 1.2M", "+15%")
    with col2:
        st.metric("Clientes", "2.5K", "+8%")
    with col3:
        st.metric("Produtos Vendidos", "15.3K", "+12%")
    with col4:
        st.metric("Taxa de Retenção", "94%", "+2%")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vendas por Mês")
        sales_data = pd.DataFrame({
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'Vendas': [100, 120, 140, 110, 160, 180]
        })
        st.bar_chart(sales_data.set_index('Mês'))
    
    with col2:
        st.subheader("Distribuição por Categoria")
        category_data = pd.DataFrame({
            'Categoria': ['Eletrônicos', 'Roupas', 'Casa', 'Esportes'],
            'Vendas': [30, 25, 20, 25]
        })
        st.bar_chart(category_data.set_index('Categoria'))

def render_settings_page():
    """Página Configurações"""
    st.markdown("## ⚙️ Configurações")
    st.write("Configure suas preferências do sistema")
    
    # Configurações gerais
    st.subheader("Configurações Gerais")
    
    col1, col2 = st.columns(2)
    with col1:
        theme = st.selectbox("Tema", ["Claro", "Escuro", "Auto"])
        language = st.selectbox("Idioma", ["Português", "English", "Español"])
        notifications = st.checkbox("Receber notificações", value=True)
    
    with col2:
        auto_save = st.checkbox("Salvamento automático", value=True)
        show_tooltips = st.checkbox("Mostrar dicas", value=True)
        compact_mode = st.checkbox("Modo compacto", value=False)
    
    # Configurações de segurança
    st.subheader("Segurança")
    
    with st.expander("Alterar Senha"):
        current_password = st.text_input("Senha Atual", type="password")
        new_password = st.text_input("Nova Senha", type="password")
        confirm_password = st.text_input("Confirmar Nova Senha", type="password")
        
        if st.button("Alterar Senha"):
            if new_password == confirm_password:
                st.success("Senha alterada com sucesso!")
            else:
                st.error("As senhas não coincidem!")
    
    # Botão salvar
    if st.button("💾 Salvar Configurações", key="save_settings"):
        st.success("Configurações salvas com sucesso!")

def render_about_page():
    """Página Sobre"""
    st.markdown("## ℹ️ Sobre")
    st.write("Informações sobre o sistema")
    
    st.markdown("""
    ### 🚀 Sistema de Gestão v2.0
    
    Este é um sistema completo de gestão desenvolvido com Streamlit.
    
    **Recursos principais:**
    - Dashboard interativo
    - Gerenciamento de perfil
    - Configurações personalizáveis
    - Múltiplas páginas
    - Interface responsiva
    
    **Tecnologias utilizadas:**
    - Python 3.9+
    - Streamlit
    - Pandas
    - NumPy
    - Matplotlib
    
    **Versão:** 2.0.1
    **Desenvolvido por:** Equipe de Desenvolvimento
    **Última atualização:** Setembro 2025
    """)
    
    st.divider()
    
    # Informações do sistema
    st.subheader("Informações do Sistema")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Status:** ✅ Online")
        st.info("**Uptime:** 99.9%")
        st.info("**Usuários Ativos:** 1,234")
    
    with col2:
        st.info("**Última Manutenção:** 20/09/2025")
        st.info("**Próxima Atualização:** 30/09/2025")
        st.info("**Suporte:** suporte@empresa.com")

def create_multipage_example():
    """Cria arquivos de exemplo para multipáginas separadas"""
    try:
        # Criar diretório pages se não existir
        pages_dir = os.path.join(os.path.dirname(__file__), "pages")
        os.makedirs(pages_dir, exist_ok=True)
        
        # Conteúdo dos arquivos de exemplo
        page_contents = {
            "home.py": '''
import streamlit as st
import pandas as pd
import numpy as np

st.title("🏠 Home")
st.write("Esta é a página inicial do sistema multipáginas!")

# Métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Usuários", "1,234", "+12%")
with col2:
    st.metric("Vendas", "R$ 56.789", "+5%")
with col3:
    st.metric("Conversão", "3.4%", "-0.2%")

# Gráfico
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)
''',
            "analytics.py": '''
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
''',
            "settings.py": '''
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
'''
        }
        
        # Criar arquivos
        for filename, content in page_contents.items():
            file_path = os.path.join(pages_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content.strip())
        
        # Criar arquivo principal de navegação
        main_content = '''
import streamlit as st

# Configurar página
st.set_page_config(
    page_title="Sistema Multipáginas",
    page_icon="🚀",
    layout="wide"
)

# Criar páginas
home_page = st.Page("pages/home.py", title="Home", icon="🏠")
analytics_page = st.Page("pages/analytics.py", title="Analytics", icon="📊")
settings_page = st.Page("pages/settings.py", title="Configurações", icon="⚙️")

# Navegação
pg = st.navigation([home_page, analytics_page, settings_page])

# Executar página selecionada
pg.run()
'''
        
        main_file_path = os.path.join(os.path.dirname(__file__), "multipage_main.py")
        with open(main_file_path, 'w', encoding='utf-8') as f:
            f.write(main_content.strip())
        
        st.success("✅ Arquivos de exemplo criados com sucesso!")
        st.info(f"""
        Arquivos criados:
        - `multipage_main.py` (arquivo principal)
        - `pages/home.py`
        - `pages/analytics.py`
        - `pages/settings.py`
        
        Para executar o exemplo:
        ```bash
        streamlit run multipage_main.py
        ```
        """)
        
    except Exception as e:
        st.error(f"Erro ao criar arquivos: {str(e)}")

# Mapeamento dinâmico
render_map = {
    "Opção 1": render_opcao1,
    "Opção 2": render_opcao2,
    "Opção 3": render_opcao3,
    "Opção 4": render_opcao4,
    "Opção 5": render_opcao5,
}

# Renderização
render_map.get(opcao_selecionada, lambda: st.write("Opção não implementada"))()
    
