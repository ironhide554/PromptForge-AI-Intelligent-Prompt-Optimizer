
from transformers import pipeline
import torch


class PromptOptimizer:
    _generator = None

    def __init__(self, model_name: str = "google/flan-t5-base"):
        if PromptOptimizer._generator is None:
            device = 0 if torch.cuda.is_available() else -1
            PromptOptimizer._generator = pipeline(
                "text2text-generation",
                model=model_name,
                tokenizer=model_name,
                device=device,
            )

    def optimize(
        self,
        prompt: str,
        target_model: str = "ChatGPT",
        style: str = "Professional",
        temperature: float = 0.3,
        max_new_tokens: int = 256,
    ) -> str:
        instruction = f"""
Rewrite the following user prompt into a high-quality AI prompt.

Requirements:
- Target AI: {target_model}
- Style: {style}
- Add an expert role/persona.
- Clarify the objective.
- Add constraints when appropriate.
- Specify a structured output format.
- Keep the original intent.
- Return only the optimized prompt.

User Prompt:
{prompt}
"""

        output = PromptOptimizer._generator(
            instruction,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=max(temperature, 0.1),
        )[0]["generated_text"]

        return output.strip()


if __name__ == "__main__":
    optimizer = PromptOptimizer()
    sample = "Write a resume for a machine learning engineer."
    print(optimizer.optimize(sample))
