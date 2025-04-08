# pip install langchain faiss-cpu pypdf ollama 
# pip install langchain-community
# pip install langchain-ollama

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# 1. Carregue e divida o PDF
loader = PyPDFLoader("Apostila 2 Legislação Básica.pdf")  # <- coloque o caminho do seu PDF aqui
pages = loader.load()
print("📘 Loas PDF.\n")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(pages)
print("📘 Split PDF.\n")

# 2. Gere embeddings com Ollama
embeddings = OllamaEmbeddings(model="deepseek-v2:16b")  # usa o modelo para embed também
print("📘 Load Deepseek.\n")

# 3. Crie a base vetorial FAISS
db = FAISS.from_documents(docs, embeddings)
print("📘 Crie a base vetorial FAISS\n")

# 4. Configure o LLM com Ollama
llm = Ollama(model="deepseek-v2:16b")
print("📘 Configure o LLM com Ollama\n")

# 5. Crie a cadeia de perguntas com recuperação de contexto
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    return_source_documents=False
)

# 6. Interface no terminal
print("📘 Pronto! Faça perguntas sobre o PDF. Digite 'sair' para encerrar.\n")
while True:
    query = input("Você: ")
    if query.lower() in ["sair", "exit", "quit"]:
        break
    resposta = qa.run(query)
    print(f"🤖 DeepSeek: {resposta}\n")
