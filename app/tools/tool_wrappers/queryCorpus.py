import logging
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

logger = logging.getLogger(__name__)
logger.info("✅ queryCorpus Tool loaded")

class Tool:
    def validate(self, input_dict):
        if not input_dict.get("query"):
            raise ValueError("Missing query string")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        query = input_dict["query"]
        logger.info(f"🔍 Querying corpus with: {query}")

        vectordb = Chroma(persist_directory="./local_vector_store", embedding_function=OpenAIEmbeddings())
        retriever = vectordb.as_retriever()
        qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0), retriever=retriever)

        result = qa.run(query)
        logger.info("✅ Query result ready")
        return {"answer": result}