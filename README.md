
![Licença MIT](https://opensource.org/files/OSI_Approved_Icons/MIT_Logo.svg)

# Chatbot com Aprendizado de Máquina

Este é um chatbot baseado em aprendizado de máquina que utiliza o modelo Naive Bayes para responder perguntas baseadas em um conjunto de dados fornecido via arquivo Excel ou banco de dados SQLite.

## Tecnologias Utilizadas
- Python
- NLTK
- Pandas
- Scikit-learn
- SQLite
- Numpy

## Estrutura do Projeto
```
/
|-- app.py  # Arquivo principal do chatbot
|-- criar_sqlite_e_inserir_dados.py  # Script para criar e inserir dados no banco SQLite
|-- chatbot_dados.xlsx  # (Opcional) Arquivo Excel com perguntas e respostas
|-- database/
    |-- chatbot.db  # Banco de dados SQLite
|-- requirements.txt  # Dependências do projeto
```

## Como Configurar e Executar

### 1. Clonar o repositório
```sh
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scriptsctivate  # Windows
```

### 3. Instalar dependências
```sh
pip install -r requirements.txt
```

### 4. Executar o chatbot
```sh
python app.py
```

O chatbot perguntará se deseja carregar os dados do Excel ou do banco de dados SQLite.

## Como Usar
1. Execute o script `app.py`.
2. Digite uma pergunta e receba uma resposta baseada no aprendizado de máquina.
3. Para sair, digite "sair".

## Criando o Banco de Dados SQLite
Se desejar utilizar um banco de dados SQLite para armazenar as perguntas e respostas, execute:
```sh
python criar_sqlite_e_inserir_dados.py
```
Isso criará o banco `database/chatbot.db` e preencherá a tabela `perguntas_respostas`.

## Formato do Arquivo Excel
O chatbot pode carregar dados a partir de um arquivo Excel. O arquivo deve conter as seguintes colunas:
- **Pergunta**: A pergunta original.
- **Resposta**: A resposta correspondente.
- **Variações de Pergunta**: Perguntas alternativas separadas por `;` (opcional).

Exemplo:
| Pergunta | Resposta | Variações de Pergunta |
|----------|---------|--------------------|
| Olá, tudo bem? | Estou bem, e você? | Oi, como você está?;E aí, tudo certo? |

## Dependências (requirements.txt)
```
nltk
pandas
scikit-learn
numpy
sqlite3
openpyxl
```

## Licença
Este projeto está sob a licença MIT.
