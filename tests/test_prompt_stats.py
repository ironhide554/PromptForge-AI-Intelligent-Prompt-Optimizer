import unittest
from utils.prompt_stats import PromptStats

class TestPromptStats(unittest.TestCase):
    def setUp(self):
        self.stats_engine = PromptStats()

    def test_word_and_char_count(self):
        text = "Hello world this is a test prompt."
        stats = self.stats_engine.calculate(text)
        self.assertEqual(stats.word_count, 7)
        self.assertEqual(stats.character_count, len(text))
        self.assertGreater(stats.estimated_tokens, 0)
        self.assertEqual(stats.sentence_count, 1)

    def test_empty_string_handling(self):
        stats = self.stats_engine.calculate("")
        self.assertEqual(stats.word_count, 0)
        self.assertEqual(stats.character_count, 0)
        self.assertEqual(stats.estimated_tokens, 0)

    def test_reading_time_and_readability(self):
        long_text = "Word " * 250
        stats = self.stats_engine.calculate(long_text)
        self.assertGreaterEqual(stats.estimated_reading_time, 1)
        self.assertIn(stats.readability, ["Easy", "Medium", "Complex"])

if __name__ == "__main__":
    unittest.main()
