from dataclasses import dataclass
from typing import List

from models.analyzer import PromptAnalyzer
from models.classifier import PromptClassifier
from utils.prompt_stats import PromptStats
from utils.scoring import score_prompt


# -------------------------------------------------
# Data Class
# -------------------------------------------------

@dataclass
class PromptEvaluation:

    score: int

    grade: str

    category: str

    confidence: float

    readability: str

    complexity: str

    ai_ready: bool

    estimated_tokens: int

    strengths: List[str]

    weaknesses: List[str]

    suggestions: List[str]

    summary: str


# -------------------------------------------------
# Evaluator
# -------------------------------------------------

class PromptEvaluator:

    def __init__(self):

        self.analyzer = PromptAnalyzer()

        self.classifier = PromptClassifier()

        self.stats = PromptStats()

    def _calculate_grade(self, score):

        if score >= 95:
            return "A+"

        elif score >= 90:
            return "A"

        elif score >= 80:
            return "B+"

        elif score >= 70:
            return "B"

        elif score >= 60:
            return "C"

        elif score >= 50:
            return "D"

        return "F"

    def _generate_summary(
            self,
            score,
            category,
            readability,
            complexity):

        if score >= 90:

            return (
                f"This is an excellent {category.lower()} prompt. "
                f"It is {readability.lower()}, "
                f"well-structured and ready for AI."
            )

        if score >= 75:

            return (
                f"This is a good {category.lower()} prompt. "
                f"Only minor improvements are recommended."
            )

        if score >= 55:

            return (
                f"This prompt has potential but requires "
                f"additional context and better instructions."
            )

        return (
            f"This prompt is too vague. "
            f"Consider rewriting it before using with an LLM."
        )

    # -------------------------------------------------

    def evaluate(self, prompt: str):

        score, score_suggestions = score_prompt(prompt)

        analysis = self.analyzer.analyze(prompt)

        category = self.classifier.classify(prompt)

        statistics = self.stats.calculate(prompt)

        suggestions = list(
            dict.fromkeys(
                analysis.suggestions +
                score_suggestions
            )
        )

        weaknesses = list(
            dict.fromkeys(
                analysis.weaknesses
            )
        )

        strengths = list(
            dict.fromkeys(
                analysis.strengths
            )
        )

        grade = self._calculate_grade(score)

        ai_ready = score >= 75

        summary = self._generate_summary(
            score,
            category.category,
            statistics.readability,
            statistics.complexity
        )

        return PromptEvaluation(

            score=score,

            grade=grade,

            category=category.category,

            confidence=category.confidence,

            readability=statistics.readability,

            complexity=statistics.complexity,

            ai_ready=ai_ready,

            estimated_tokens=statistics.estimated_tokens,

            strengths=strengths,

            weaknesses=weaknesses,

            suggestions=suggestions,

            summary=summary

        )


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    evaluator = PromptEvaluator()

    prompt = """
    Act as an experienced Machine Learning Engineer.

    Build a Streamlit dashboard
    for house price prediction.

    Use Random Forest.

    Display the results in Markdown.

    Keep the code modular.
    """

    result = evaluator.evaluate(prompt)

    print(result)