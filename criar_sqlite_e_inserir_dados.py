import sqlite3
import pandas as pd

# Função para carregar dados do Excel
def carregar_dados_excel(arquivo):
    try:
        df = pd.read_excel(arquivo)
        if "Pergunta" not in df.columns or "Resposta" not in df.columns:
            raise ValueError("O arquivo deve conter as colunas 'Pergunta' e 'Resposta'.")
        
        # Função para processar as variações de perguntas
        def processar_variacoes(row):
            pergunta = row["Pergunta"]
            resposta = row["Resposta"]
            variacao = row["Variações de Pergunta"]
            
            if isinstance(variacao, str) and variacao.strip():  # Verifica se é uma string não vazia
                variacao = variacao.split(';')  # Separar as variações
            else:
                variacao = []  # Se não houver variações, deixar uma lista vazia
            
            perguntas_respostas = [(pergunta, resposta, ", ".join(variacao))]
            return perguntas_respostas
        
        # Aplica a função para processar as perguntas, respostas e variações
        perguntas_respostas = df.apply(processar_variacoes, axis=1)
        
        # Flatten a lista de tuplas para uma lista simples
        perguntas, respostas, variacoes = zip(*[item for sublist in perguntas_respostas for item in sublist])
        
        return list(perguntas), list(respostas), list(variacoes)
    
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return [], [], []

# Função para inserir dados no banco de dados SQLite
def inserir_dados_banco(perguntas, respostas, variacoes):
    try:
        # Conectar ao banco de dados SQLite (ele será criado se não existir)
        conn = sqlite3.connect("database/chatbot.db")
        cursor = conn.cursor()
        
        # Criar a tabela se não existir
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS perguntas_respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL,
            variacoes TEXT
        )
        ''')
        
        # Inserir dados no banco de dados
        for pergunta, resposta, variacao in zip(perguntas, respostas, variacoes):
            cursor.execute('''
            INSERT INTO perguntas_respostas (pergunta, resposta, variacoes)
            VALUES (?, ?, ?)
            ''', (pergunta, resposta, variacao))
        
        # Confirmar e fechar a conexão
        conn.commit()
        conn.close()
        print("Dados inseridos no banco de dados com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")

# Carregar dados do arquivo Excel
arquivo_excel = "chatbot_dados.xlsx"
perguntas, respostas, variacoes = carregar_dados_excel(arquivo_excel)

# Verificar se as listas de perguntas, respostas e variações não estão vazias
if perguntas and respostas and variacoes:
    # Inserir os dados no banco de dados
    inserir_dados_banco(perguntas, respostas, variacoes)
else:
    print("Erro: Não foi possível carregar as perguntas, respostas ou variações.")
