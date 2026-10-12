from dataclasses import dataclass
from typing import Dict, List



# Data Class


@dataclass
class PromptTemplate:

    name: str
    category: str
    description: str
    template: str



# Template Manager


class PromptTemplates:

    def __init__(self):

        self.templates: Dict[str, PromptTemplate] = {

            "Coding": PromptTemplate(
                name="Coding",
                category="Programming",
                description="General coding prompt",
                template="""Act as a Senior Software Engineer.

Task:
{task}

Requirements:
- Write clean and modular code.
- Explain the logic.
- Handle edge cases.
- Include comments.
- Output using Markdown.
"""
            ),

            "Machine Learning": PromptTemplate(
                name="Machine Learning",
                category="AI",
                description="Machine Learning projects",
                template="""Act as an experienced Machine Learning Engineer.

Task:
{task}

Requirements:
- Explain the algorithm.
- Mention preprocessing.
- Include model training.
- Evaluate performance.
- Suggest improvements.
"""
            ),

            "Resume": PromptTemplate(
                name="Resume",
                category="Career",
                description="ATS Resume Builder",
                template="""Act as an experienced HR Recruiter.

Task:
{task}

Requirements:
- ATS Friendly
- Professional formatting
- Highlight measurable achievements
- Keep under two pages.
"""
            ),

            "Research": PromptTemplate(
                name="Research",
                category="Academic",
                description="Research Paper",
                template="""Act as a Research Scientist.

Task:
{task}

Requirements:
- Explain methodology.
- Cite assumptions.
- Mention limitations.
- Write professionally.
"""
            ),

            "SQL": PromptTemplate(
                name="SQL",
                category="Database",
                description="SQL Query Generator",
                template="""Act as a Database Administrator.

Task:
{task}

Requirements:
- Write optimized SQL.
- Explain every query.
- Handle edge cases.
"""
            ),

            "Blog": PromptTemplate(
                name="Blog",
                category="Writing",
                description="Blog Generator",
                template="""Act as a Professional Content Writer.

Task:
{task}

Requirements:
- SEO Optimized
- Clear headings
- Bullet points
- Conclusion
"""
            ),

            "Marketing": PromptTemplate(
                name="Marketing",
                category="Business",
                description="Marketing Prompt",
                template="""Act as a Digital Marketing Expert.

Task:
{task}

Requirements:
- Define target audience.
- Mention KPIs.
- Suggest strategies.
- Professional tone.
"""
            ),

            "Email": PromptTemplate(
                name="Email",
                category="Communication",
                description="Professional Email",
                template="""Act as a Corporate Communication Expert.

Task:
{task}

Requirements:
- Professional tone.
- Subject line.
- Greeting.
- Body.
- Closing.
"""
            ),

            "Translation": PromptTemplate(
                name="Translation",
                category="Language",
                description="Translation Prompt",
                template="""Act as a Professional Translator.

Task:
{task}

Requirements:
- Preserve meaning.
- Maintain grammar.
- Natural wording.
"""
            ),

            "Image Generation": PromptTemplate(
                name="Image Generation",
                category="Creative",
                description="Image Prompt",
                template="""Act as an AI Image Prompt Engineer.

Task:
{task}

Requirements:
- Mention subject.
- Describe lighting.
- Camera angle.
- Background.
- Style.
- Color palette.
"""
            )

        }

    # --------------------------------------------------

    def get_categories(self) -> List[str]:

        return list(self.templates.keys())

    # --------------------------------------------------

    def get_template(self, name: str):

        return self.templates.get(name)

    # --------------------------------------------------

    def build_prompt(
        self,
        template_name: str,
        task: str
    ) -> str:

        template = self.get_template(template_name)

        if template is None:
            raise ValueError(
                f"Unknown template: {template_name}"
            )

        return template.template.format(task=task)

    # --------------------------------------------------

    def search_templates(
        self,
        keyword: str
    ) -> List[PromptTemplate]:

        keyword = keyword.lower()

        results = []

        for template in self.templates.values():

            if (
                keyword in template.name.lower()
                or
                keyword in template.category.lower()
                or
                keyword in template.description.lower()
            ):

                results.append(template)

        return results

    def load_custom_templates(self):
        """Loads user-saved custom templates from data/custom_templates.json."""
        from pathlib import Path
        import json
        custom_file = Path("data/custom_templates.json")
        if custom_file.exists():
            try:
                with open(custom_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        t = PromptTemplate(
                            name=item["name"],
                            category=item.get("category", "Custom"),
                            description=item.get("description", ""),
                            template=item.get("template", "")
                        )
                        self.templates[t.name] = t
            except Exception:
                pass

    def add_custom_template(self, name: str, category: str, description: str, template: str):
        """Saves a new custom template to data/custom_templates.json."""
        from pathlib import Path
        import json
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        custom_file = data_dir / "custom_templates.json"
        current = []
        if custom_file.exists():
            try:
                with open(custom_file, "r", encoding="utf-8") as f:
                    current = json.load(f)
            except Exception:
                current = []
        # Update existing or append new
        current = [t for t in current if t.get("name") != name]
        current.append({
            "name": name,
            "category": category,
            "description": description,
            "template": template
        })
        with open(custom_file, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4)
        self.templates[name] = PromptTemplate(
            name=name,
            category=category,
            description=description,
            template=template
        )

    # --------------------------------------------------

    def get_all_templates(self):
        self.load_custom_templates()
        return list(self.templates.values())



# Testing


if __name__ == "__main__":

    manager = PromptTemplates()

    print(manager.get_categories())

    print()

    prompt = manager.build_prompt(

        "Coding",

        "Build a FastAPI authentication system."

    )

    print(prompt)