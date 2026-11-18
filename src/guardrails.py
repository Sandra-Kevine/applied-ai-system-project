def validate_query(question: str) -> tuple[bool, str]:
    if not isinstance(question, str) or not question.strip():
        return False, "Please enter a question."
    question = question.strip()
    if len(question) > 1000:
        return False, "Question is too long; please keep it under 1000 characters."
    if len(question.split()) < 2:
        return False, "Please provide a complete question."
    return True, ""
