import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import sqlite3

# Baixar tokenizer do NLTK (caso ainda não tenha sido feito)
nltk.download('punkt')

# Função para carregar dados do Excel e validar colunas
def carregar_dados_excel(arquivo):
    try:
        df = pd.read_excel(arquivo)
        if "Pergunta" not in df.columns or "Resposta" not in df.columns:
            raise ValueError("O arquivo deve conter as colunas 'Pergunta' e 'Resposta'.")
        
        perguntas = []
        respostas = []
        
        # Loop para expandir as variações de pergunta
        for index, row in df.iterrows():
            pergunta = row["Pergunta"]
            resposta = row["Resposta"]
            variacoes = row["Variações de Pergunta"]
            
            # Verificar se 'Variações de Pergunta' não é NaN e é uma string
            if isinstance(variacoes, str):  # Verifica se é uma string
                variacoes = variacoes.split(';')  # Separar as variações
            else:
                variacoes = []  # Se não for string, não há variações
            
            perguntas.extend([pergunta] + variacoes)  # Adicionar pergunta original e suas variações
            respostas.extend([resposta] * (len([pergunta] + variacoes)))  # A resposta será a mesma para todas as variações
        
        return perguntas, respostas
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return [], []

# Função para carregar dados do banco de dados SQLite
def carregar_dados_banco():
    try:
        conn = sqlite3.connect("database/chatbot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT pergunta, resposta, variacoes FROM perguntas_respostas")
        dados = cursor.fetchall()
        
        perguntas = []
        respostas = []
        
        # Loop para expandir as variações de pergunta
        for pergunta, resposta, variacoes in dados:
            if isinstance(variacoes, str):  # Verifica se é uma string
                variacoes = variacoes.split(';')  # Separar as variações
            else:
                variacoes = []  # Se não for string, não há variações
            
            perguntas.extend([pergunta] + variacoes)  # Adicionar pergunta original e suas variações
            respostas.extend([resposta] * (len([pergunta] + variacoes)))  # A resposta será a mesma para todas as variações
        
        conn.close()
        return perguntas, respostas
    except Exception as e:
        print(f"Erro ao carregar dados do banco de dados: {e}")
        return [], []

# Função para carregar dados com base na escolha do usuário
def carregar_dados():
    escolha = input("Escolha a origem dos dados (1 para Excel, 2 para Banco de Dados SQLite): ").strip()
    
    if escolha == "1":
        arquivo_excel = "chatbot_dados.xlsx"
        return carregar_dados_excel(arquivo_excel)
    elif escolha == "2":
        return carregar_dados_banco()
    else:
        print("Opção inválida. Usando Excel por padrão.")
        return carregar_dados_excel("chatbot_dados.xlsx")

# Carregar perguntas e respostas com base na escolha
perguntas, respostas = carregar_dados()

# Verificar se as listas de perguntas e respostas não estão vazias
if not perguntas or not respostas:
    print("Erro: As perguntas ou respostas não foram carregadas corretamente.")
else:
    # Vetorização do texto
    vectorizer = CountVectorizer(stop_words="english")  # Remover palavras comuns (stopwords)
    x_train = vectorizer.fit_transform(perguntas)
    y_train = np.arange(len(perguntas))

    # Treinando o modelo Naive Bayes
    modelo = MultinomialNB()
    modelo.fit(x_train, y_train)

    # Função para responder ao chatbot
    def chatbot_responder(mensagem):
        mensagem = mensagem.lower()
        mensagem_vectorizada = vectorizer.transform([mensagem])
        indice = modelo.predict(mensagem_vectorizada)[0]
        # Garantir que o índice esteja dentro do intervalo válido
        return respostas[indice] if indice < len(respostas) else "Desculpe, não entendi. Pode reformular?"

    # Loop de interação com o usuário
    if __name__ == "__main__":
        print("Chatbot: Olá! Digite uma mensagem (ou 'sair' para encerrar).")
        while True:
            usuario_input = input("Você: ")
            if usuario_input.lower() == "sair":
                print("Chatbot: Até mais!")
                break
            if not usuario_input.strip():  # Verifica se a entrada não está vazia
                print("Chatbot: Por favor, digite uma mensagem válida.")
                continue
            resposta = chatbot_responder(usuario_input)
            print(f"Chatbot: {resposta}")
