# Model Card

## Intended Use
Study Ground supports study and course-note review. It should help users locate and understand concepts in documents they provide. It is not intended for high-stakes decisions, medical advice, legal advice, or claims beyond the source collection.

## Limitations and Biases
- The lexical ranker can miss synonyms and paraphrases.
- The fallback writer is extractive and may omit nuance.
- Optional model output can introduce errors despite retrieved context.
- Performance depends on document coverage and writing quality.
- The model may reflect biases in supplied documents or configured language model.
- Confidence is a heuristic, not calibrated probability.

## Misuse Prevention
- The system rejects empty and oversized inputs.
- Irrelevant retrieval is blocked by a confidence threshold.
- Answers cite source passages and identify the fallback or model mode.
- No autonomous tools, network actions, or personal-data collection are enabled.
- Users should review sources and remove sensitive documents before sharing logs.

## What Surprised Us
Low lexical similarity can occur even for an obvious concept when the question uses completely different wording. This confirmed the need for an explicit “insufficient evidence” path instead of always forcing an answer.

## AI Collaboration Reflection
I collaborated with an AI coding assistant to decompose the requirements, implement the RAG pipeline, and write tests and documentation.

**Suggestion accepted:** Use a deterministic extractive fallback plus optional model generation. This made the project runnable without credentials and allowed the retrieval and guardrail behavior to be tested reproducibly.

**Suggestion rejected or revised:** The first design proposed a general browser/agent that could search the web and modify files. I rejected that scope because it added security and nondeterminism; I narrowed the system to local documents, read-only retrieval, and a single optional text-generation endpoint.

## Evaluation
The automated harness checks four grounded retrieval questions, empty input, and unrelated or unsupported input. Results are printed by `python -m src.evaluate` and can be saved in interaction logs.
