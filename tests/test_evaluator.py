import unittest
from models.evaluator import PromptEvaluator

class TestPromptEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = PromptEvaluator()

    def test_grade_calculation(self):
        self.assertEqual(self.evaluator._calculate_grade(96), "A+")
        self.assertEqual(self.evaluator._calculate_grade(91), "A")
        self.assertEqual(self.evaluator._calculate_grade(82), "B+")
        self.assertEqual(self.evaluator._calculate_grade(72), "B")
        self.assertEqual(self.evaluator._calculate_grade(62), "C")
        self.assertEqual(self.evaluator._calculate_grade(52), "D")
        self.assertEqual(self.evaluator._calculate_grade(30), "F")

    def test_evaluate_comprehensive(self):
        prompt = (
            "Act as a Senior Cloud Architect. "
            "Design a microservices architecture on AWS. "
            "Requirements: use Terraform, containerized ECS, and RDS PostgreSQL. "
            "Output the response in structured Markdown."
        )
        res = self.evaluator.evaluate(prompt)
        self.assertIsNotNone(res)
        self.assertIn(res.grade, ["A+", "A", "B+", "B", "C"])
        self.assertIsInstance(res.summary, str)
        self.assertGreater(len(res.summary), 10)

if __name__ == "__main__":
    unittest.main()
