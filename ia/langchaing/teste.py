from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import json
import time

# --- Configuração ---
# 1. Instancie o modelo Ollama
# Certifique-se de que o Ollama está rodando e o modelo 'llama3' está baixado.
llm_local = Ollama(model="llama3")

# 2. Defina a persona de Vendas (System Prompt)
# Esta persona instrui o LLM sobre seu papel e o fluxo de vendas.
system_prompt = (
    "Você é 'Bot de Vendas Consultivas', um assistente amigável e focado no cliente. "
    "Seu objetivo é guiar o cliente através de um funil de vendas simples, seguindo estes passos:"
    "1. **Boas-vindas:** Se apresente e pergunte o objetivo do cliente."
    "2. **Sondagem (Necessidade):** Faça 1 ou 2 perguntas para entender a dor e o contexto do cliente."
    "3. **Oferta/Solução:** Sugira um produto/serviço relevante (mencione 'Soluções Digitais')."
    "4. **Próximo Passo:** Peça o e-mail ou telefone para agendar uma demonstração."
    "**Mantenha cada resposta curta e focada em avançar o diálogo.**"
)

# O prompt principal que será usado no fluxo. Ele aceita o histórico do chat.
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}"),
])

# 3. Crie a Chain (Prompt | LLM)
chain = prompt | llm_local

# ----------------- Simulação do Fluxo de Vendas no Chat -----------------

print("===============================================")
print("🤖 INÍCIO DO CHAT DE VENDAS (Modelo: Llama 3)")
print("===============================================")

# Passo 1: Início (Pergunta do Cliente)
user_input = "Olá, estou pensando em modernizar os sistemas da minha empresa."

print(f"\n[CLIENTE]: {user_input}")
time.sleep(1) # Simula o tempo de espera
bot_response = chain.invoke({"input": user_input})
print(f"\n[BOT DE VENDAS]: {bot_response.strip()}")

# Passo 2: Sondagem (Continuação)
# O bot deve responder fazendo perguntas sobre a dor (Graças ao System Prompt)
user_input_2 = "Ah, sim. Atualmente nossa maior dor é a lentidão do nosso sistema de CRM."

print(f"\n[CLIENTE]: {user_input_2}")
time.sleep(1)
# Aqui, o LLM usa o histórico implícito (mantido pelo usuário) + o System Prompt para saber como continuar
# Nota: Para um chat persistente real, você usaria um objeto 'ConversationalChain' que armazena o histórico!
bot_response_2 = chain.invoke({"input": f"{user_input_2}. O que você me sugere agora?"})
print(f"\n[BOT DE VENDAS]: {bot_response_2.strip()}")

# Passo 3: Fechamento/Próximo Passo (Continuação)
user_input_3 = "Parece interessante. Como podemos avançar?"

print(f"\n[CLIENTE]: {user_input_3}")
time.sleep(1)
bot_response_3 = chain.invoke({"input": f"{user_input_3}. O que você me sugere agora?"})
print(f"\n[BOT DE VENDAS]: {bot_response_3.strip()}")

print("\n===============================================")
print("✅ FIM DA SIMULAÇÃO")