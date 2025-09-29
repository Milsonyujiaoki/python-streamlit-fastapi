from cProfile import label
from calendar import c
from email.policy import default
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
st.progress(70)

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

# Sidebar section
st.sidebar.title("Sidebar de Teste")
st.sidebar.write("Conteúdo da sidebar")

# Sidebar para navegação
st.sidebar.header("Navegação")
num_opcoes = 5
opcoes = [f"Opção {i}" for i in range(1, num_opcoes + 1)]
opcao_selecionada = st.sidebar.selectbox("Selecione uma opção:", options=opcoes)

# Funções de renderização
def render_opcao1():
    st.write("Conteúdo da Opção 1")

def render_opcao2():
    st.write("Conteúdo da Opção 2")

def render_opcao3():
    st.write("Conteúdo da Opção 3")

def render_opcao4():
    st.write("Conteúdo da Opção 4")

def render_opcao5():
    st.write("Conteúdo da Opção 5")

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
    
