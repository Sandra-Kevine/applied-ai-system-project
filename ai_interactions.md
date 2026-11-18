# AI Interaction Log

## 2026-11-18: RAG question
- **Input:** What is RAG?
- **Plan:** Validate input -> index local `.txt` files -> rank chunks -> reject low confidence -> synthesize/extract answer -> cite sources.
- **Retrieved:** `data/ai_systems.txt`, passage 1.
- **Decision:** Use deterministic extractive mode because no model endpoint was configured.
- **Result:** `6/6` reliability checks pass in the default fixture run.

## 2026-11-18: Guardrail question
- **Input:** How do quantum magnetics control gardening?
- **Plan:** Validate input -> retrieve -> detect low relevance -> block unsupported answer.
- **Retrieved:** No passages met the confidence threshold.
- **Decision:** Return a refusal/rephrase response.
- **Result:** Passes the low-confidence guardrail test.
