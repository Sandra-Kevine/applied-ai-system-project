import json
import os
import urllib.request


def synthesize(question: str, passages: list[dict]) -> tuple[str, str]:
    if not passages:
        return "I could not find enough relevant information in the indexed notes to answer reliably. Please rephrase or add supporting documents.", "guardrail"

    context = "\n\n".join(f"[{i+1}] {p['text']}" for i, p in enumerate(passages))
    api_url = os.getenv("AI_API_URL")
    model = os.getenv("AI_MODEL", "local-model")

    if api_url:
        prompt = (
            "Answer the question using only the context below. Cite relevant passages by number. "
            "If the context is insufficient, say so explicitly.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2}).encode()
        request = urllib.request.Request(api_url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                result = json.loads(response.read().decode())
            content = result["choices"][0]["message"]["content"].strip()
            return content, "model"
        except Exception:
            pass

    strongest = passages[0]
    text = strongest["text"]
    return text, "extractive"
