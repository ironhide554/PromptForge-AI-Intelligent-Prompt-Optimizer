import unittest
from models.classifier import PromptClassifier

class TestPromptClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = PromptClassifier()

    def test_coding_category(self):
        result = self.classifier.classify("Write a python script to reverse a list")
        self.assertEqual(result.category, "Coding")
        self.assertIn("python", result.matched_keywords)

    def test_resume_category(self):
        result = self.classifier.classify("Create an ATS friendly resume")
        self.assertEqual(result.category, "Resume")
        self.assertIn("resume", result.matched_keywords)

    def test_data_analysis_category(self):
        result = self.classifier.classify("Use pandas to perform data analysis")
        self.assertEqual(result.category, "Data Analysis")
        self.assertIn("pandas", result.matched_keywords)

if __name__ == "__main__":
    unittest.main()
