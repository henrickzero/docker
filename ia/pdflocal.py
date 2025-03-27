from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings
from llama_index.llms.ollama import Ollama
import chromadb

# Configura embedding local
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Configura LLM local via Ollama (ex: mistral)
Settings.llm = Ollama(model="mistral", request_timeout=60)

# Inicializa Chroma local
chroma_client = chromadb.PersistentClient(path="./chroma_storage_local")
collection = chroma_client.get_or_create_collection("meus_pdfs2")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Lê os documentos da pasta (coloque seus PDFs aqui)
documents = SimpleDirectoryReader("meus_pdfs2").load_data()

# Cria o índice vetorial com embeddings locais
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Cria mecanismo de consulta
query_engine = index.as_query_engine()

# Consulta (com instrução em português)
resposta = query_engine.query("O que ocorre no abandono de cargo? Devolva a resposta em português do Brasil")
print(resposta)
