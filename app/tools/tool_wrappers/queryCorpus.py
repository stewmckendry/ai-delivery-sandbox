import logging
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from chromadb import HttpClient

logger = logging.getLogger(__name__)
logger.info("✅ queryCorpus Tool loaded")

CHROMA_DIR = os.getenv("CHROMA_DIR", "./local_vector_store")
CHROMA_HOST = os.getenv("CHROMA_SERVER_HOST")
CHROMA_PORT = os.getenv("CHROMA_SERVER_HTTP_PORT", "8000")
USE_REMOTE_CHROMA = CHROMA_HOST is not None
logger.info("USE_REMOTE_CHROMA: %s", USE_REMOTE_CHROMA)
logger.info("CHROMA_HOST: %s", CHROMA_HOST)
logger.info("CHROMA_PORT: %s", CHROMA_PORT)

class Tool:
    def validate(self, input_dict):
        if not input_dict.get("query"):
            raise ValueError("Missing query string")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        query = input_dict["query"]
        logger.info(f"🔍 Querying corpus with: {query}")

        if USE_REMOTE_CHROMA:
            logger.info("Connecting to Chroma host: %s", CHROMA_HOST)
            client = HttpClient(host=CHROMA_HOST, port=int(CHROMA_PORT))
            collection = client.get_or_create_collection("policygpt")
            results = collection.query(query_texts=[query], n_results=5)
            return {"results": results}
        else:
            vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=OpenAIEmbeddings())
            retriever = vectordb.as_retriever()
            qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0), retriever=retriever)
            result = qa.run(query)
            logger.info("✅ Query result ready")
            return {"answer": result}