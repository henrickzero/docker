#pip install langchain langchain-community
#ollama pull llama3
#pip install langchain langchain-core langchain-community --upgrade
#
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate # Importação Corrigida

# 1. Instancie o modelo Ollama
llm_local = Ollama(model="llama3")

# 2. Crie um prompt template
prompt = ChatPromptTemplate.from_template(
    "Você é um assistente de escrita criativa. Escreva uma breve história sobre {personagem} que encontra um objeto mágico."
)

# 3. Crie a Chain usando o padrão LCEL (mais simples e eficiente)
# O '|' é o operador de encadeamento
chain = prompt | llm_local

# 4. Execute a Chain
personagem = "um programador sênior"

print(f"Gerando história para: {personagem}...\n")
# Em LCEL, use 'invoke' com um dicionário de entrada
resposta = chain.invoke({"personagem": personagem}) 

print("--- Resultado do Llama 3 ---")
print(resposta)