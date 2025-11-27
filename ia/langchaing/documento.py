from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# 1 — Carrega o PDF
loader = PyPDFLoader("documentox.pdf")
docs = loader.load()

# 2 — Fragmenta em partes menores
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs_chunked = splitter.split_documents(docs)

# 3 — Cria embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4 — Banco vetorial local
db = Chroma.from_documents(docs_chunked, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})

# 5 — Modelo local do Ollama
llm = Ollama(model="llama3")

# 6 — Chain de Perguntas com RAG
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

print("PDF carregado! Pergunte algo.\n")

while True:
    pergunta = input("> Você: ")
    if pergunta.lower() in ("sair", "exit", "quit"):
        break
    resposta = qa.run(pergunta)
    print("\n🤖 Bot:", resposta, "\n")
