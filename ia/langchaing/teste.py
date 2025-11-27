#pip install "langchain<0.1.0"
#
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough

system_prompt = (
    "Você é 'Bot de Vendas Consultivas', um assistente amigável e focado no cliente. "
    "Estrutura:"
    "1. Boas-vindas e pergunta do objetivo."
    "2. 1-2 perguntas para entender a dor."
    "3. Oferta de soluções digitais."
    "4. Solicitar contato (email/telefone). "
    "Respostas curtas e direcionadas."
)

llm = Ollama(model="llama3")
memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

chain = (
    RunnablePassthrough.assign(
        history=lambda _: memory.load_memory_variables({})["history"]
    )
    | prompt
    | llm
)

print("Chat iniciado. Digite 'sair' para terminar.\n")
while True:
    msg = input("Cliente: ")
    if msg.lower() in ["sair", "exit"]:
        break
    
    resp = chain.invoke({"input": msg})
    print("Bot:", resp)
    
    memory.save_context({"input": msg}, {"output": resp})
