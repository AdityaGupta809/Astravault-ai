from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


def create_vector_store(docs, embeddings):
    client = QdrantClient("http://localhost:6333", prefer_grpc=False   )  
    return QdrantVectorStore.from_documents(
        docs,
        embeddings,
        collection_name="ai_agent_docs",
        url="http://localhost:6333",
    )