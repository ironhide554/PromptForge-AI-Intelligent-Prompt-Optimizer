from dataclasses import dataclass
import re
from typing import Dict


@dataclass
class PromptStatistics:

    character_count: int
    character_no_spaces: int

    word_count: int
    sentence_count: int
    paragraph_count: int

    average_word_length: float
    average_sentence_length: float

    estimated_tokens: int
    estimated_reading_time: float

    unique_words: int
    lexical_diversity: float

    prompt_density: float

    readability: str
    complexity: str


class PromptStats:

    ACTION_WORDS = [
        "create",
        "build",
        "design",
        "generate",
        "explain",
        "analyze",
        "develop",
        "summarize",
        "compare",
        "translate",
        "optimize",
        "write"
    ]

    def calculate(self, prompt: str) -> PromptStatistics:

        prompt = prompt.strip()

        characters = len(prompt)

        characters_no_spaces = len(prompt.replace(" ", ""))

        words = re.findall(r"\b\w+\b", prompt)

        word_count = len(words)

        paragraphs = len(
            [p for p in prompt.split("\n\n") if p.strip()]
        )

        sentence_count = max(
            1,
            len(re.findall(r"[.!?]", prompt))
        )

        average_word_length = (
            sum(len(w) for w in words) / word_count
            if word_count
            else 0
        )

        average_sentence_length = (
            word_count / sentence_count
            if sentence_count
            else 0
        )

        estimated_tokens = int(word_count * 1.3)

        estimated_reading_time = round(
            word_count / 200,
            2
        )

        unique_words = len(set(w.lower() for w in words))

        lexical_diversity = round(
            unique_words / word_count,
            2
        ) if word_count else 0

        action_count = sum(
            1
            for word in self.ACTION_WORDS
            if word in prompt.lower()
        )

        prompt_density = round(
            action_count / word_count,
            2
        ) if word_count else 0

        # --------------------------
        # Readability
        # --------------------------

        if average_sentence_length < 12:
            readability = "Easy"

        elif average_sentence_length < 20:
            readability = "Medium"

        else:
            readability = "Complex"

        # --------------------------
        # Complexity
        # --------------------------

        if word_count < 20:
            complexity = "Basic"

        elif word_count < 60:
            complexity = "Intermediate"

        else:
            complexity = "Advanced"

        return PromptStatistics(

            character_count=characters,

            character_no_spaces=characters_no_spaces,

            word_count=word_count,

            sentence_count=sentence_count,

            paragraph_count=paragraphs,

            average_word_length=round(
                average_word_length,
                2
            ),

            average_sentence_length=round(
                average_sentence_length,
                2
            ),

            estimated_tokens=estimated_tokens,

            estimated_reading_time=estimated_reading_time,

            unique_words=unique_words,

            lexical_diversity=lexical_diversity,

            prompt_density=prompt_density,

            readability=readability,

            complexity=complexity

        )

    def to_dict(self, prompt: str) -> Dict:

        stats = self.calculate(prompt)

        return stats.__dict__


# ----------------------------------
# Testing
# ----------------------------------

if __name__ == "__main__":

    prompt = """
    Act as an experienced Machine Learning Engineer.

    Build a Streamlit application for predicting house prices.

    Use Random Forest.

    Display the output in Markdown.

    Keep the code modular.

    """

    stats = PromptStats()

    result = stats.calculate(prompt)

    print(result)