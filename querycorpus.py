from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Use env vars or hardcode host/port
db = Chroma(
    embedding_function=OpenAIEmbeddings(),
    collection_name="policygpt",
    client_settings={
        "chroma_api_impl": "rest",
        "chroma_server_host": "https://just-harmony-production.up.railway.app",
        "chroma_server_http_port": "8000"
    }
)

print("Docs stored:", db._collection.count())
