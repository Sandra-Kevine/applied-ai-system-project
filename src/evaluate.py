from src.cli import answer

CASES = [
    ("What is RAG?", "retrieval", "rag"),
    ("How does an AI agent work?", "retrieval", "agent"),
    ("What is a guardrail?", "retrieval", "guardrail"),
    ("How should outputs be checked?", "retrieval", "verification"),
]


def evaluate() -> dict:
    passed = 0
    for question, category, term in CASES:
        result = answer(question)
        ok = result["mode"] != "guardrail" and result["confidence"] >= 0.18 and term in " ".join(s["text"].lower() for s in result["sources"])
        passed += bool(ok)

    empty = answer("")
    empty_ok = empty["mode"] == "guardrail" and empty["confidence"] == 0.10

    unrelated = answer("How do quantum magnetics control gardening?")
    unrelated_ok = unrelated["mode"] == "guardrail"

    total = len(CASES) + 2
    score = passed + bool(empty_ok) + bool(unrelated_ok)
    retrieval_results = []
    for question, category, term in CASES:
        result = answer(question)
        retrieval_results.append({
            "input": question,
            "result": "PASS" if term in " ".join(s["text"].lower() for s in result["sources"]) else "FAIL",
            "confidence": result["confidence"],
        })

    return {
        "passed": score,
        "total": total,
        "retrieval_passed": passed,
        "retrieval_total": len(CASES),
        "retrieval_results": retrieval_results,
    }


def main() -> None:
    result = evaluate()
    print(f"RAG retrieval cases: {result['retrieval_passed']}/{result['retrieval_total']} passed")
    print("Empty-input guardrail:", "PASS" if answer("")["mode"] == "guardrail" else "FAIL")
    print("Low-confidence guardrail:", "PASS" if answer("How do quantum magnetics control gardening?")["mode"] == "guardrail" else "FAIL")
    print(f"Overall: {result['passed']}/{result['total']} checks passed")


if __name__ == "__main__":
    main()
