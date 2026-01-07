from fastapi import FastAPI
from agent.agent_loop import run_agent
from embeddings.embeded import get_embeddings
from embeddings.vector_store import create_vector_store
from ingestion.loader import load_all_documents
from ingestion.chunker import chunk_documents

app = FastAPI()

docs = load_all_documents()
chunks = chunk_documents(docs)
embeddings = get_embeddings()
vectorstore = create_vector_store(chunks, embeddings)

@app.post("/ask")
def ask(query: str, role: str):
    answer = run_agent(query, role)
    return {"answer": answer}