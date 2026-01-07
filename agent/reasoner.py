from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from embeddings.embeded import get_embeddings
from access_control.roles import ROLES
from dotenv import load_dotenv
from qdrant_client.models import Filter, FieldCondition, MatchAny


load_dotenv()

def get_reasoning_response(user_query, role="student"):
    client = OpenAI()

    # 1️⃣ Load embeddings
    embeddings = get_embeddings()

    # 2️⃣ Connect to existing Qdrant collection
    vector_store = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="ai_agent_docs",
        embedding=embeddings,
    )

    # 3️⃣ Role-based filter
    allowed_levels = ROLES.get(role, [])

    qdrant_filter = Filter(
            must=[
                FieldCondition(
                    key="access_level",
                    match=MatchAny(any=allowed_levels)
                )
            ]
    )


    if "*" in allowed_levels:
        search_result = vector_store.similarity_search(
            query=user_query,
            k=5,
        )
    else:
        search_result = vector_store.similarity_search(
            query=user_query,
            k=5,
            filter=qdrant_filter
        )

    # 4️⃣ Safe refusal if nothing retrieved
    if not search_result:
        return {
            "answer": "You are not authorized or no relevant information is available.",
            "citations": [],
            "confidence": 0.0
        }

    # 5️⃣ Build context with page numbers
    context = "\n\n".join(
        [
            f"Page Content: {doc.page_content}\nPage Number: {doc.metadata.get('page', 'N/A')}"
            for doc in search_result
        ]
    )

    # 6️⃣ System prompt (STRICT grounding)
    System_Prompt = f"""
        You are a helpful AI assistant.
        Answer ONLY using the provided context.
        If the answer is not present, say you do not know.

        Provide the answer along with page numbers.

        Context:
        {context}
        """

    # 7️⃣ OpenAI call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": System_Prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return {
        "answer": response.choices[0].message.content,
        "citations": [doc.metadata.get("page") for doc in search_result],
        "confidence": 0.75  
    }
