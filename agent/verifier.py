

def verify_answer(similarity_score, threshold=0.6):
    if similarity_score < threshold:
        return False
    return True
