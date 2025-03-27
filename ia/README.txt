pip install llama-index chromadb PyMuPDF
pip uninstall llama-index -y
pip install llama-index llama-index-vector-stores-chroma chromadb
pip install sentence-transformers
pip install llama-index-embeddings-huggingface
pip install llama-index-llms-ollama
pip install openai




from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, load_index_from_storage

# Lê os PDFs de uma pasta
documents = SimpleDirectoryReader("meus_pdfs").load_data()

# Cria o índice vetorial local com ChromaDB
vector_store = ChromaVectorStore(persist_dir="./chroma_storage")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
index.storage_context.persist()

# Cria o chatbot com o índice
query_engine = index.as_query_engine()

# Faz uma pergunta
resposta = query_engine.query("Quais são os principais temas do documento?")
print(resposta)



# https://ollama.com
# ollama run mistral
http://localhost:11434/