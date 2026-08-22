from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ClassificationResult:
    category: str
    confidence: float
    matched_keywords: List[str]


class PromptClassifier:

    def __init__(self):

        self.categories: Dict[str, List[str]] = {

            "Coding": [
                "python","java","c++","javascript","react","node",
                "django","flask","fastapi","api","algorithm",
                "bug","debug","leetcode","sql","database",
                "program","function","code","streamlit"
            ],

            "Resume": [
                "resume","cv","ats","linkedin","cover letter",
                "job","internship","career"
            ],

            "Email": [
                "email","mail","reply","subject",
                "professional email","compose"
            ],

            "Research": [
                "research","paper","journal",
                "citation","literature",
                "methodology","abstract"
            ],

            "Marketing": [
                "marketing","seo","advertisement",
                "facebook","instagram","campaign",
                "brand","promotion"
            ],

            "Blog": [
                "blog","article","medium",
                "post","newsletter"
            ],

            "Translation": [
                "translate","translation",
                "english","hindi","french",
                "german","spanish"
            ],

            "Summarization": [
                "summarize","summary",
                "shorten","brief"
            ],

            "Image Generation": [
                "image","draw","logo",
                "poster","illustration",
                "design","generate image"
            ],

            "SQL": [
                "sql","mysql","postgresql",
                "query","join","table",
                "database"
            ],

            "Machine Learning": [
                "machine learning",
                "deep learning",
                "transformer",
                "tensorflow",
                "keras",
                "pytorch",
                "llm",
                "rag",
                "embedding",
                "classification",
                "prediction",
                "training",
                "model"
            ],
            
            "Data Analysis": [
                "data analysis",
                "pandas",
                "matplotlib",
                "seaborn",
                "visualization",
                "chart",
                "graph",
                "statistics"
            ]
        }

    def classify(self, prompt: str) -> ClassificationResult:
        """
        Classifies a given prompt into a category based on keyword matching.
        
        Args:
            prompt (str): The user prompt to classify.
            
        Returns:
            ClassificationResult: Result containing category name, confidence score, and matched keywords.
        """
        prompt_lower = prompt.lower()

        scores = {}

        matches = {}

        for category, keywords in self.categories.items():

            matched = []

            score = 0

            for keyword in keywords:

                if keyword in prompt_lower:
                    matched.append(keyword)
                    score += 1

            scores[category] = score
            matches[category] = matched

        best_category = max(scores, key=scores.get)

        best_score = scores[best_category]

        if best_score == 0:

            return ClassificationResult(
                category="General",
                confidence=0.50,
                matched_keywords=[]
            )

        total = sum(scores.values())

        confidence = round(best_score / total, 2)

        return ClassificationResult(
            category=best_category,
            confidence=confidence,
            matched_keywords=matches[best_category]
        )


if __name__ == "__main__":

    classifier = PromptClassifier()

    examples = [

        "Write a FastAPI REST API",

        "Create an ATS friendly resume",

        "Summarize this research paper",

        "Translate this paragraph to Hindi",

        "Generate an image of a futuristic city"

    ]

    for prompt in examples:

        result = classifier.classify(prompt)

        print("=" * 50)
        print(prompt)
        print(result)