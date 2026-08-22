from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch


class PromptOptimizer:
    _model = None
    _tokenizer = None

    def __init__(self, model_name: str = "google/flan-t5-base"):
        if PromptOptimizer._model is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            PromptOptimizer._tokenizer = AutoTokenizer.from_pretrained(model_name)
            PromptOptimizer._model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def optimize(
        self,
        prompt: str,
        target_model: str = "ChatGPT",
        style: str = "Professional",
        temperature: float = 0.3,
        max_new_tokens: int = 256,
    ) -> str:
        instruction = f"""Rewrite the following user prompt into a high-quality AI prompt.

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
{prompt}"""

        inputs = PromptOptimizer._tokenizer(
            instruction,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(self.device)

        outputs = PromptOptimizer._model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=max(temperature, 0.1),
            top_p=0.9,
            pad_token_id=PromptOptimizer._tokenizer.pad_token_id,
            eos_token_id=PromptOptimizer._tokenizer.eos_token_id,
        )

        output_text = PromptOptimizer._tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the optimized prompt part (after the instruction)
        if "User Prompt:" in output_text:
            output_text = output_text.split("User Prompt:")[-1].strip()

        return output_text.strip()


if __name__ == "__main__":
    optimizer = PromptOptimizer()
    sample = "Write a resume for a machine learning engineer."
    print(optimizer.optimize(sample))