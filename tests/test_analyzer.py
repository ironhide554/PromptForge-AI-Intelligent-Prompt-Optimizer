import unittest
from models.analyzer import PromptAnalyzer

class TestPromptAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PromptAnalyzer()

    def test_syntax_extraction_and_complexity(self):
        prompt = "Act as an expert developer. Create a python script. You must output in json format."
        analysis = self.analyzer.analyze(prompt)
        self.assertIsNotNone(analysis)
        self.assertGreater(analysis.persona_score, 0)
        self.assertGreater(analysis.constraints_score, 0)
        self.assertGreater(analysis.format_score, 0)
        self.assertIn(analysis.complexity, ["Basic", "Intermediate", "Professional"])

    def test_strengths_and_weaknesses(self):
        prompt = "write code"
        analysis = self.analyzer.analyze(prompt)
        self.assertGreater(len(analysis.weaknesses), 0)
        self.assertGreater(len(analysis.suggestions), 0)

if __name__ == "__main__":
    unittest.main()
