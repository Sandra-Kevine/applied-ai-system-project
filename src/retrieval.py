import math
import re
from collections import Counter
from pathlib import Path

STOP_WORDS = {"a", "an", "the", "is", "are", "of", "to", "and", "or", "for", "in", "on", "what", "how", "why", "do", "does"}


def tokenize(text: str) -> list[str]:
    return [word for word in re.findall(r"[A-Za-z0-9]+", text.lower()) if word and word not in STOP_WORDS]


class Retriever:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.df = Counter()
        for chunk in chunks:
            self.df.update(set(chunk["tokens"]))

    def search(self, query: str, limit: int = 2) -> list[dict]:
        query_terms = tokenize(query)
        query_counts = Counter(query_terms)
        scores = []
        for chunk in self.chunks:
            score = 0.0
            overlap = []
            for term, count in query_counts.items():
                if term in chunk["tf"]:
                    overlap.append(term)
                    idf = math.log((1 + len(self.chunks)) / (1 + self.df[term])) + 1
                    score += count * chunk["tf"][term] * idf
            if score:
                q_norm = math.sqrt(sum((count * math.sqrt((1 + len(self.chunks)) / (1 + self.df[t])) if t in self.df else 0) ** 2 for t, count in query_counts.items()))
                c_norm = math.sqrt(sum(value ** 2 for value in chunk["tf"].values()))
                score = score / (q_norm * c_norm) if q_norm and c_norm else 0
            scores.append((score, chunk, overlap))
        scores.sort(key=lambda item: item[0], reverse=True)
        return [{**chunk, "score": round(score, 4), "overlap": overlap} for score, chunk, overlap in scores[:limit] if score > 0]


def index_directory(directory: str) -> tuple[Retriever, list[dict]]:
    chunks = []
    for path in sorted(Path(directory).glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for index, block in enumerate([p.strip() for p in text.split("\n\n") if p.strip()], start=1):
            tokens = tokenize(block)
            chunks.append({
                "text": block,
                "path": str(path),
                "block": index,
                "tokens": tokens,
                "tf": Counter(tokens),
            })
    return Retriever(chunks), chunks
