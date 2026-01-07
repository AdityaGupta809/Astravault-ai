from agent.reasoner import get_reasoning_response
from agent.verifier import verify_answer


def run_agent(query: str, role: str = "student"):

    # 1️⃣ Call reasoning + retrieval (already implemented by you)
    result = get_reasoning_response(
        user_query=query,
        role=role
    )


    # 2️⃣ Handle access denial or empty result
    if not result or result["confidence"] == 0.0:
        return {
            "answer": "Access denied or no relevant information.",
            "citations": [],
            "confidence": 0.0
        }

    # 3️⃣ Verification layer (trust-aware)
    if not verify_answer(result["confidence"]):
        return {
            "answer": "I am not confident enough to answer based on the available information.",
            "citations": result["citations"],
            "confidence": result["confidence"]
        }

    # 4️⃣ Final agent response
    return {
        "answer": result["answer"],
        "citations": result["citations"],
        "confidence": result["confidence"]
    }
