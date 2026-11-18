import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from src.guardrails import validate_query
from src.retrieval import index_directory
from src.synthesis import synthesize


def confidence(passages: list[dict]) -> float:
    if not passages:
        return 0.10
    top = passages[0]["score"]
    return round(min(0.95, max(0.10, top)), 2)


def answer(question: str, data_dir: str = "data") -> dict:
    valid, error = validate_query(question)
    if not valid:
        return {"answer": error, "sources": [], "confidence": 0.10, "mode": "guardrail", "query": question}

    retriever, _ = index_directory(data_dir)
    passages = retriever.search(question, limit=2)
    if not passages or confidence(passages) < 0.18:
        passages = []
    text, mode = synthesize(question, passages)
    return {
        "answer": text,
        "sources": passages,
        "confidence": confidence(passages),
        "mode": mode,
        "query": question,
    }


def log_interaction(result: dict) -> None:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), **result}
    with (log_dir / "interactions.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Study Ground: source-grounded local RAG assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)
    index = subparsers.add_parser("index", help="Verify and index a document directory")
    index.add_argument("--data", default="data", help="Directory containing .txt documents")
    ask = subparsers.add_parser("ask", help="Ask a question")
    ask.add_argument("question")
    ask.add_argument("--data", default="data", help="Directory containing .txt documents")
    args = parser.parse_args()

    if args.command == "index":
        retriever, chunks = index_directory(args.data)
        print(f"Indexed {len(chunks)} passages from {args.data}")
    else:
        result = answer(args.question, args.data)
        log_interaction(result)
        print("Answer:", result["answer"])
        print("\nSources:")
        if result["sources"]:
            for i, source in enumerate(result["sources"], start=1):
                print(f"[{i}] {source['path']} (passage {source['block']})")
        else:
            print("none")
        print(f"\nConfidence: {result['confidence']:.2f}")
        print("Mode:", result["mode"])


if __name__ == "__main__":
    main()
