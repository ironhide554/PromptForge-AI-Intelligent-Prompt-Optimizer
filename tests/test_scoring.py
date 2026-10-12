import unittest
from utils.scoring import score_prompt

class TestPromptScoring(unittest.TestCase):
    def test_empty_prompt(self):
        score, suggestions = score_prompt("")
        self.assertEqual(score, 0)
        self.assertGreater(len(suggestions), 0)

    def test_short_vague_prompt(self):
        score, suggestions = score_prompt("write a poem")
        self.assertLess(score, 50)
        self.assertIn("Assign a role/persona (e.g. 'Act as a senior data scientist').", suggestions)

    def test_high_quality_structured_prompt(self):
        prompt = (
            "Act as a Principal Python Architect. "
            "Write a production-ready FastAPI endpoint for user registration. "
            "Requirements and constraints: "
            "You must ensure inputs are validated with Pydantic v2 schemas. "
            "Do not include conversational filler or external dependencies. "
            "For example, provide sample JSON payload like this: {'username': 'test'}. "
            "Output the response format in clean Markdown with comments explaining the logic."
        )
        score, suggestions = score_prompt(prompt)
        self.assertGreaterEqual(score, 80)
        self.assertIsInstance(score, int)

if __name__ == "__main__":
    unittest.main()
