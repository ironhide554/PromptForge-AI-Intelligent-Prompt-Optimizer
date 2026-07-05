
from dataclasses import dataclass, field
from typing import List
import re


@dataclass
class PromptAnalysis:

    overall_score: int

    clarity_score: int
    context_score: int
    specificity_score: int
    constraints_score: int
    format_score: int
    persona_score: int

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    word_count: int = 0
    sentence_count: int = 0

    readability: str = "Unknown"

    complexity: str = "Unknown"


# ----------------------------
# Analyzer
# ----------------------------

class PromptAnalyzer:

    PERSONA_WORDS = [
        "act as",
        "you are",
        "behave as",
        "assume the role",
        "expert",
        "specialist",
        "teacher",
        "engineer",
        "developer",
        "consultant"
    ]

    FORMAT_WORDS = [
        "markdown",
        "json",
        "table",
        "bullet",
        "csv",
        "xml",
        "format",
        "response format",
        "output"
    ]

    CONSTRAINT_WORDS = [
        "must",
        "only",
        "do not",
        "don't",
        "without",
        "maximum",
        "minimum",
        "at least",
        "under",
        "exactly"
    ]

    EXAMPLE_WORDS = [
        "example",
        "for example",
        "sample"
    ]

    ACTION_VERBS = [
        "create",
        "write",
        "generate",
        "design",
        "build",
        "analyze",
        "summarize",
        "explain",
        "develop",
        "compare",
        "translate",
        "optimize"
    ]

    def _contains_any(self, text, keywords):

        text = text.lower()

        return any(word in text for word in keywords)

    def analyze(self, prompt: str) -> PromptAnalysis:

        prompt = prompt.strip()

        words = prompt.split()

        word_count = len(words)

        sentence_count = max(
            1,
            len(re.findall(r"[.!?]", prompt))
        )

        strengths = []

        weaknesses = []

        suggestions = []

        clarity = 0
        context = 0
        specificity = 0
        constraints = 0
        formatting = 0
        persona = 0

        # ------------------------
        # Clarity
        # ------------------------

        if self._contains_any(prompt, self.ACTION_VERBS):
            clarity = 20
            strengths.append("Clear objective detected.")
        else:
            weaknesses.append("Task objective is unclear.")
            suggestions.append(
                "Start with a clear action such as Create, Explain, Analyze or Build."
            )

        # ------------------------
        # Context
        # ------------------------

        if word_count >= 25:
            context = 20
            strengths.append("Sufficient context provided.")
        elif word_count >= 15:
            context = 15
            suggestions.append("Adding more context can improve results.")
        else:
            weaknesses.append("Very little context provided.")
            suggestions.append(
                "Describe the background or intended purpose."
            )

        # ------------------------
        # Persona
        # ------------------------

        if self._contains_any(prompt, self.PERSONA_WORDS):
            persona = 15
            strengths.append("Expert persona detected.")
        else:
            weaknesses.append("No AI role/persona specified.")
            suggestions.append(
                "Example: Act as an experienced Data Scientist."
            )

        # ------------------------
        # Output Format
        # ------------------------

        if self._contains_any(prompt, self.FORMAT_WORDS):
            formatting = 15
            strengths.append("Desired output format specified.")
        else:
            weaknesses.append("Output format not specified.")
            suggestions.append(
                "Specify Markdown, JSON, Bullet Points, Table etc."
            )

        # ------------------------
        # Constraints
        # ------------------------

        if self._contains_any(prompt, self.CONSTRAINT_WORDS):
            constraints = 15
            strengths.append("Prompt contains useful constraints.")
        else:
            weaknesses.append("No constraints detected.")
            suggestions.append(
                "Mention length, tone, restrictions or formatting rules."
            )

        # ------------------------
        # Specificity
        # ------------------------

        specificity = 15

        if word_count < 12:
            specificity = 5

        if word_count < 6:
            specificity = 0

        if specificity >= 15:
            strengths.append("Prompt is reasonably specific.")
        else:
            weaknesses.append("Prompt is too generic.")
            suggestions.append(
                "Provide additional details about your expectations."
            )

        # ------------------------
        # Bonus
        # ------------------------

        bonus = 0

        if self._contains_any(prompt, self.EXAMPLE_WORDS):
            bonus += 5
            strengths.append("Example detected.")

        if any(char.isdigit() for char in prompt):
            bonus += 5

        overall = (
            clarity +
            context +
            specificity +
            constraints +
            formatting +
            persona +
            bonus
        )

        overall = min(overall, 100)

        # ------------------------
        # Readability
        # ------------------------

        if word_count < 20:
            readability = "Easy"

        elif word_count < 50:
            readability = "Medium"

        else:
            readability = "Advanced"

        # ------------------------
        # Complexity
        # ------------------------

        if overall >= 85:
            complexity = "Professional"

        elif overall >= 60:
            complexity = "Intermediate"

        else:
            complexity = "Basic"

        return PromptAnalysis(

            overall_score=overall,

            clarity_score=clarity,

            context_score=context,

            specificity_score=specificity,

            constraints_score=constraints,

            format_score=formatting,

            persona_score=persona,

            strengths=strengths,

            weaknesses=weaknesses,

            suggestions=suggestions,

            word_count=word_count,

            sentence_count=sentence_count,

            readability=readability,

            complexity=complexity

        )


# ----------------------------------------
# Testing
# ----------------------------------------

if __name__ == "__main__":

    analyzer = PromptAnalyzer()

    prompt = """
    Act as an experienced Machine Learning Engineer.

    Build a Streamlit dashboard for house price prediction.

    Use Random Forest.

    Output in Markdown.

    Keep the code modular.

    """

    result = analyzer.analyze(prompt)

    print(result)