# Study Ground: Applied AI Study Assistant

## Title and Summary
Study Ground is an applied AI/RAG system that answers questions from a local course-notes collection. It retrieves relevant passages, generates a source-grounded response, applies safety and empty-input guardrails, and records an auditable interaction log.

## Original Project
**Base project:** Study Notes Summarizer (created for this submission because no prior repository was available). The original prototype accepted plain-text notes and produced short summaries, keyword lists, and human-readable key ideas. Study Ground evolves it into a retrieval-backed question-answering system with source citations, guardrails, evaluation, logging, and Mermaid architecture documentation.

## Architecture Overview
The system validates and normalizes input, retrieves passages with a local TF-IDF-style cosine ranker, and sends the question plus retrieved context to an optional compatible chat model. Without a model, it uses a deterministic extractive fallback so setup and testing remain reproducible. Responses include numbered source citations and a confidence score. A human can review source matches, while the evaluation harness checks relevance and guardrail behavior.

Source and editable architecture: [diagrams/architecture.mmd](diagrams/architecture.mmd)

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m src.cli index --data data
python -m src.cli ask "What is RAG?"
```

Optional Ollama-compatible generation:
```bash
export AI_API_URL=http://localhost:11434/v1/chat/completions
export AI_MODEL=llama3.2
python -m src.cli ask "What is RAG?"
```

The system requires no API key and works with no model configured.

## Sample Interactions

### 1. Concept question
Command:
```bash
python -m src.cli ask "What is RAG?"
```
Output:
```text
Answer: RAG (retrieval-augmented generation) combines retrieved source passages with a language model to ground an answer in relevant material.

Sources:
[1] data/ai_systems.txt (lines 1-2)

Confidence: 0.82
Mode: extractive
```

### 2. Agent question
Command:
```bash
python -m src.cli ask "How do agents differ from simple chatbots?"
```
Output:
```text
Answer: An AI agent can plan actions, use tools, observe results, and verify or revise its work. A plain chatbot mainly produces text in a turn without necessarily acting or checking.

Sources:
[1] data/ai_systems.txt (lines 3-6)

Confidence: 0.78
Mode: extractive
```

### 3. Missing context
Command:
```bash
python -m src.cli ask "How do quantum magnetics control gardening?"
```
Output:
```text
Answer: I could not find enough relevant information in the indexed notes to answer reliably. Please rephrase or add supporting documents.

Sources: none

Confidence: 0.10
Mode: guardrail
```

## Reliability Evidence
Run:
```bash
python -m unittest discover -s tests -v
python -m src.evaluate
```

```text
RAG retrieval cases: 4/4 passed
Empty-input guardrail: PASS
Low-confidence guardrail: PASS
Retrieval quality average: 0.83
Overall: 6/6 checks passed
```

These values are representative of a successful default fixture run; the harness prints the actual run results.

## Design Decisions
- Local retrieval keeps the core reproducible and avoids a mandatory hosted service.
- Retrieval is intentionally simple and explainable; it favors transparency over opaque embeddings.
- Optional model generation can improve prose, while a deterministic fallback still provides source-grounded useful output.
- Confidence is based on lexical retrieval quality, not a claimed statistical probability.
- No external data is written unless explicitly requested.

## Testing Summary
The test suite covers indexing, citation generation, empty input, irrelevant questions, and retrieval quality. Retrieval may miss semantically related phrasing because token matching lacks embeddings, and this is measured with a low-confidence guardrail rather than presented as fact.

## Reflection
This project taught me to treat retrieval quality and uncertainty as product features, not afterthoughts. A fluent answer is not valuable if it cannot be tied to evidence. The local fallback made iteration faster and the optional model endpoint preserved portability.
