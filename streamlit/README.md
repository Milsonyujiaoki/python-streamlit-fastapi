# 🏢 Sistema Corporativo Modular

Sistema Streamlit modular e escalável para edição de dados corporativos e outras funcionalidades empresariais.

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

## 🛠️ Como Usar

### Executar a Aplicação
```bash
streamlit run app.py
```

### Módulos Disponíveis
1. **🏢 Editor de Atos Societários** - Edição de dados corporativos
2. **🎵 Pesquisador de Letras** - Busca letras de música
3. **🚀 Módulo de Exemplo** - Template para novos módulos

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

## 🔮 Próximas Melhorias

- [ ] Sistema de plugins dinâmicos
- [ ] Configurações por usuário
- [ ] Tema customizável
- [ ] Cache inteligente
- [ ] Logs centralizados
- [ ] Autenticação/autorização
- [ ] API REST opcional
- [ ] Testes automatizados

## 🤝 Contribuindo

1. Crie seu módulo seguindo o template
2. Documente as funcionalidades
3. Teste a integração
4. Atualize este README se necessário

---

**Desenvolvido com ❤️ usando Streamlit e Python**