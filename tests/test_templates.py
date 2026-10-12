import unittest
from utils.templates import PromptTemplates

class TestPromptTemplates(unittest.TestCase):
    def setUp(self):
        self.manager = PromptTemplates()

    def test_get_categories(self):
        categories = self.manager.get_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)

    def test_get_all_templates(self):
        templates = self.manager.get_all_templates()
        self.assertGreater(len(templates), 0)
        self.assertTrue(any(t.name == "Coding" for t in templates))

    def test_add_custom_template(self):
        self.manager.add_custom_template(
            name="Test Architecture",
            category="Custom",
            description="Unit test template",
            template="Act as an architect. {task}"
        )
        templates = self.manager.get_all_templates()
        self.assertTrue(any(t.name == "Test Architecture" for t in templates))

if __name__ == "__main__":
    unittest.main()
