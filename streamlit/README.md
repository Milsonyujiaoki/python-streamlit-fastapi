# 🏢 Sistema Corporativo Integrado

Sistema Streamlit modular e escalável para edição de dados corporativos com funcionalidades avançadas de manipulação de Excel, análise de dados e automação empresarial.

## 📁 Estrutura do Projeto

```
📦 python-streamlit-spacy-fastapi/
├── 📄 app.py                    # Aplicação principal
├── 📁 core/                     # Componentes base
│   ├── __init__.py
│   └── base.py                  # Classes base e utilitários
├── 📁 modules/                  # Módulos da aplicação
│   ├── __init__.py
│   ├── societary.py            # Editor de atos societários  
│   ├── lyrics.py               # Pesquisador de letras
│   ├── excel_editor.py         # Editor completo de Excel
│   └── example.py              # Exemplo de novo módulo
└── 📄 README.md                # Este arquivo
```

## 🚀 Características

### ✅ **Modular**
- Cada funcionalidade é um módulo independente
- Fácil adição/remoção de funcionalidades
- Código organizado e separado por responsabilidades

### ✅ **Escalável**
- Componentes reutilizáveis (UIComponents, DataProcessor)
- Sistema de configuração centralizado
- Gerenciador de aplicação robusto

### ✅ **Reutilizável**
- Classes base para novos módulos
- Componentes de UI padronizados
- Templates para desenvolvimento rápido

## 🛠️ Instalação e Uso

### Pré-requisitos
- Python 3.12+
- pipenv ou pip

### Instalação
```bash
# Clonar o repositório
git clone <repository-url>
cd python-streamlit-fastapi

# Instalar dependências com pipenv (recomendado)
pipenv install

# Ou com pip
pip install -r requirements.txt
```

### Executar a Aplicação
```bash
# Com pipenv
pipenv run streamlit run app.py

# Ou diretamente
streamlit run app.py
```

### Acesso
Abra seu navegador em: `http://localhost:8501`

## 🎯 Casos de Uso Práticos

### Para Empresas
- **📋 Gestão de Dados Corporativos**: Edição de planilhas empresariais com validação
- **🔄 Integração de Sistemas**: Combinação de dados de diferentes fontes
- **📊 Análise Rápida**: Insights instantâneos sem necessidade de ferramentas complexas
- **📑 Relatórios Automatizados**: Geração de relatórios a partir de múltiplas fontes

### Para Analistas
- **🔍 Exploração de Dados**: Interface intuitiva para análise exploratória
- **🧮 Cálculos Avançados**: Operações matemáticas entre colunas e tabelas
- **📈 Estatísticas Descritivas**: Análise automática com métricas relevantes
- **💱 Conversão de Dados**: Tabelas DE/PARA para padronização

### Para Desenvolvedores
- **🚀 Prototipagem Rápida**: Desenvolvimento ágil de módulos
- **🔧 Reutilização**: Componentes prontos para uso
- **🏗️ Arquitetura Escalável**: Base sólida para expansão
- **📦 Modularidade**: Fácil manutenção e extensão

## 📊 Funcionalidades do Editor de Excel

### 🔧 **Upload e Gerenciamento**
- **Upload Múltiplo**: Carregue vários arquivos Excel/CSV simultaneamente
- **Múltiplas Planilhas**: Navegue entre diferentes abas do mesmo arquivo
- **Visualização**: Preview dos dados com informações detalhadas
- **Renomeação**: Defina nomes personalizados para suas tabelas

### ✏️ **Edição Avançada**
- **Editor Interativo**: Modifique dados diretamente na interface
- **Operações de Coluna**: Adicione, remova e renomeie colunas
- **Restauração**: Volte aos dados originais a qualquer momento
- **Validação**: Verificação automática de tipos e formato

### 🔗 **Operações de Dados**
- **JOIN/MERGE**: Combine tabelas com diferentes tipos de junção
- **PROCV/Lookup**: Busque valores entre tabelas (equivalente ao VLOOKUP)
- **DE/PARA**: Substitua valores usando tabelas de conversão
- **Matemática**: Soma, subtração, multiplicação, divisão entre colunas
- **Estatísticas**: Análise descritiva completa dos dados

### 📈 **Análise e Visualização**
- **Estatísticas Gerais**: Contagem de linhas, colunas, valores nulos
- **Análise por Colunas**: Insights específicos por tipo de dado
- **Valores Únicos**: Identificação de padrões nos dados
- **Distribuição**: Visualização da estrutura dos dados

### 💾 **Export e Download**
- **Excel**: Download no formato .xlsx preservando formatação
- **CSV**: Export para análise em outras ferramentas
- **Múltiplas Tabelas**: Download individual ou em lote

### Módulos Disponíveis

1. **🏢 Editor de Atos Societários** - Edição e gerenciamento de dados corporativos
2. **🎵 Pesquisador de Letras** - Busca letras de música via API
3. **� Editor de Excel** - Editor completo com funcionalidades avançadas:
   - Upload múltiplo de arquivos (Excel/CSV)
   - Seleção de planilhas individuais
   - Editor de dados com interface intuitiva
   - Operações avançadas (JOIN, MERGE, PROCV)
   - Tabelas DE/PARA e operações matemáticas
   - Análise estatística e visualização
   - Download em múltiplos formatos
4. **�🚀 Módulo de Exemplo** - Template para desenvolvimento de novos módulos

## 🔧 Arquitetura

### Core Components

#### `AppManager`
Gerenciador principal da aplicação que:
- Configura a página Streamlit
- Gerencia registro de módulos
- Controla navegação via sidebar
- Trata erros de execução

#### `BaseModule` (Classe Abstrata)
Classe base para todos os módulos com:
- Estrutura padrão (nome, ícone, descrição)
- Métodos de interface comuns
- Sistema de mensagens padronizado

#### `UIComponents`
Componentes de interface reutilizáveis:
- `file_uploader()` - Upload de arquivos padronizado
- `data_editor()` - Editor de dados configurável  
- `action_buttons()` - Botões em colunas
- `tabs()` - Sistema de abas

#### `DataProcessor`
Processamento de dados genérico:
- `safe_json_load()` - Carregamento seguro de JSON
- `create_editable_dataframe()` - Criação de DataFrames editáveis

## 📝 Como Adicionar Novos Módulos

### 1. Criar o Módulo

```python
# modules/meu_modulo.py
import streamlit as st
from core.base import BaseModule, UIComponents

class MeuModulo(BaseModule):
    def __init__(self):
        super().__init__(
            name="Meu Módulo",
            icon="🎯",
            description="Descrição do módulo"
        )
    
    def render(self) -> None:
        self.show_header()
        
        # Sua implementação aqui
        st.write("Conteúdo do módulo")
        
        if st.button("Ação", width="stretch"):
            self.show_success("Funcionou!")
```

### 2. Registrar no Pacote

```python
# modules/__init__.py
from .societary import SocietaryModule
from .lyrics import LyricsModule
from .meu_modulo import MeuModulo  # ← Adicionar

__all__ = ['SocietaryModule', 'LyricsModule', 'MeuModulo']  # ← Adicionar
```

### 3. Adicionar à Aplicação

```python
# app.py
from modules import SocietaryModule, LyricsModule, MeuModulo  # ← Adicionar

def main():
    # ... configuração ...
    
    app.register_module(SocietaryModule())
    app.register_module(LyricsModule())
    app.register_module(MeuModulo())  # ← Adicionar
```

### 4. Pronto! 🎉
O novo módulo aparecerá automaticamente na sidebar.

## 🎨 Componentes Disponíveis

### Botões de Ação
```python
buttons_config = [
    {'label': '💾 Salvar', 'key': 'save'},
    {'label': '📥 Download', 'key': 'download'},
]

button_states = UIComponents.action_buttons(buttons_config)

if button_states['save']:
    # Ação do botão salvar
    pass
```

### Abas Organizadas
```python
tab_configs = [
    {'name': '📁 Upload', 'key': 'upload'},
    {'name': '✏️ Editar', 'key': 'edit'},
]

tabs = UIComponents.tabs(tab_configs)

with tabs['upload']['tab']:
    # Conteúdo da aba upload
    pass
```

### Editor de Dados
```python
df_editado = UIComponents.data_editor(
    df_original,
    key="meu_editor"
)
```

### Upload de Arquivos
```python
arquivo = UIComponents.file_uploader(
    "Selecione um arquivo:",
    ['json', 'csv'],
    "Ajuda sobre o arquivo"
)
```

## 🎯 Vantagens da Arquitetura

### Para Desenvolvedores
- **Desenvolvimento Rápido**: Templates e componentes prontos
- **Código Limpo**: Separação clara de responsabilidades
- **Reutilização**: Componentes aproveitáveis entre módulos
- **Manutenção Fácil**: Módulos independentes

### Para Usuários
- **Interface Consistente**: Mesmo padrão visual
- **Navegação Intuitiva**: Sidebar organizada
- **Funcionalidades Integradas**: Tudo em um lugar
- **Experiência Fluída**: Componentes padronizados

## � Dependências

### Principais
- **streamlit** - Framework web interativo
- **pandas** - Manipulação e análise de dados
- **openpyxl** - Leitura/escrita de arquivos Excel
- **xlsxwriter** - Geração otimizada de arquivos Excel
- **requests** - Requisições HTTP para APIs
- **fastapi** - API REST (opcional)

### Desenvolvimento
- **pytest** - Framework de testes
- **black** - Formatador de código
- **flake8** - Linter de código
- **mypy** - Verificador de tipos

## �🔮 Próximas Melhorias

### Em Desenvolvimento
- [x] **Editor completo de Excel** - Funcionalidades avançadas
- [x] **Operações de dados** - JOIN, MERGE, PROCV
- [x] **Múltiplas planilhas** - Navegação entre abas
- [x] **Análise estatística** - Insights automáticos

### Planejado
- [ ] **Dashboard visual** - Gráficos interativos
- [ ] **Módulo de relatórios** - Templates personalizáveis  
- [ ] **Sistema de plugins** - Carregamento dinâmico
- [ ] **Configurações por usuário** - Preferências salvas
- [ ] **Tema customizável** - Interface personalizável
- [ ] **Cache inteligente** - Performance otimizada
- [ ] **Logs centralizados** - Monitoramento completo
- [ ] **Autenticação/autorização** - Controle de acesso
- [ ] **API REST integrada** - Automação externa
- [ ] **Testes automatizados** - Qualidade garantida

## 🤝 Contribuindo

1. Crie seu módulo seguindo o template
2. Documente as funcionalidades
3. Teste a integração
4. Atualize este README se necessário

---

## 💻 Tecnologias Utilizadas

- **Python 3.12+** - Linguagem principal
- **Streamlit** - Framework web interativo
- **Pandas** - Manipulação de dados
- **OpenPyXL/XlsxWriter** - Processamento Excel
- **FastAPI** - API REST (opcional)
- **Pipenv** - Gerenciamento de dependências

---

*Desenvolvido com ❤️ para facilitar o trabalho com dados corporativos*