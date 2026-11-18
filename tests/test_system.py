import unittest

from src.cli import answer


class StudyGroundTests(unittest.TestCase):
    def test_rag_answer_has_source(self):
        result = answer("What is RAG?", "data")
        self.assertEqual(result["mode"], "extractive")
        self.assertGreaterEqual(result["confidence"], 0.18)
        self.assertGreater(len(result["sources"]), 0)

    def test_agent_answer(self):
        result = answer("How does an AI agent work?", "data")
        self.assertIn("agent", " ".join(source["text"] for source in result["sources"]).lower())

    def test_empty_input_guardrail(self):
        result = answer("", "data")
        self.assertEqual(result["mode"], "guardrail")
        self.assertEqual(result["confidence"], 0.10)

    def test_unrelated_question_guardrail(self):
        result = answer("How do quantum magnetics control gardening?", "data")
        self.assertEqual(result["mode"], "guardrail")


if __name__ == "__main__":
    unittest.main()
