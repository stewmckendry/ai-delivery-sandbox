import logging
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from chromadb import HttpClient

logger = logging.getLogger(__name__)
logger.info("✅ queryCorpus Tool loaded")

CHROMA_DIR = os.getenv("CHROMA_DIR", "./local_vector_store")
CHROMA_HOST = os.getenv("CHROMA_SERVER_HOST")
CHROMA_PORT = os.getenv("CHROMA_SERVER_HTTP_PORT", "8000")
USE_REMOTE_CHROMA = CHROMA_HOST is not None
logger.debug("USE_REMOTE_CHROMA: %s", USE_REMOTE_CHROMA)
logger.debug("CHROMA_HOST: %s", CHROMA_HOST)
logger.debug("CHROMA_PORT: %s", CHROMA_PORT)

class Tool:
    def validate(self, input_dict):
        if not input_dict.get("query"):
            raise ValueError("Missing query string")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        query = input_dict["query"]
        logger.info(f"🔍 Querying corpus with: {query[:100]}")

        results_list = []
        if USE_REMOTE_CHROMA:
            logger.debug("Connecting to Chroma host: %s", CHROMA_HOST)
            client = HttpClient(host=CHROMA_HOST, port=int(CHROMA_PORT))
            collection = client.get_or_create_collection("policygpt")
            results = collection.query(query_texts=[query], n_results=5)
            docs = results.get("documents", [[]])[0]
            metas = results.get("metadatas", [[]])[0]
            
            for doc, meta in zip(docs, metas):
                title = meta.get("title", "Untitled")
                source = meta.get("source", "Internal Knowledge Base")
                date = meta.get("date", "n.d.")
                url = meta.get("url", "")
                citation = f'"{title}." {source}, {date}, {url}.' if url else f'"{title}." {source}, {date}.'
                results_list.append({
                    "text": doc,
                    "title": title,
                    "source": source,
                    "date": date,
                    "url": url,
                    "citation": citation
                })

            context = "\n\n".join(docs)
            logger.info(f"✅ Retrieved {len(docs)} documents from remote Chroma")
            template = "Based on the following documents:\n\n{context}\n\nAnswer the query: {query}"
            prompt = PromptTemplate.from_template(template)
            llm_chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=prompt)
            answer = llm_chain.run({"context": context, "query": query})
            logger.info(f"✅ Query result ready: {answer[:100]}")
        else:
            vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=OpenAIEmbeddings())
            retriever = vectordb.as_retriever()
            qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0), retriever=retriever)
            answer = qa.run(query)
            logger.info(f"✅ Query result ready: {answer[:100]}")
            # Local Chroma does not expose metadata, so include empty entries
            results_list = []

        return {
            "answer": answer,
            "documents": [r["text"] for r in results_list],
            "citations": [r["citation"] for r in results_list],
            "metadatas": results_list
        }