# 5–7 Minute Presentation Script: Study Ground

## Slide 1 — Problem (30 seconds)
I extended a Study Notes Summarizer into a source-grounded applied AI system. It helps a learner ask questions about local course notes instead of receiving an answer without evidence.

## Slide 2 — Live demo (2 minutes)
1. Run `python -m src.cli index --data data`.
2. Run the RAG question: `python -m src.cli ask "What is RAG?"`.
3. Run the agent question: `python -m src.cli ask "How does an AI agent work?"`.
4. Run the unsupported question and show the guardrail response.

## Slide 3 — Architecture (90 seconds)
The diagram separates input validation, indexing, retrieval, synthesis, confidence/citation checking, logging, human review, and automated testing. Retrieved passages are used with an optional chat endpoint or the deterministic extractive fallback.

## Slide 4 — Reliability (90 seconds)
The automated harness covers four grounded questions, empty input, and unsupported context. A 6/6 result demonstrates that the default fixture passes. Testing also showed that lexical retrieval can miss paraphrases, so uncertainty is surfaced rather than hidden.

## Slide 5 — Responsible AI (60 seconds)
Limitations include lexical ranking, extractive simplification, document bias, and the heuristic confidence score. The system prevents unsupported answers with a low-confidence threshold and provides source citations. My collaboration accepted the reproducible fallback and rejected an over-broad autonomous web-agent design.

## Slide 6 — Next steps (30 seconds)
Next, I would add semantic retrieval, human-labeled relevance tests, and a larger set of course documents. The system would remain local-first and auditable.
