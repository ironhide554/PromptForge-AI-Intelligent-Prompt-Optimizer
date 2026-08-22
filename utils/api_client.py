import openai
import anthropic
import google.generativeai as genai
from typing import Optional

def generate_response(provider: str, api_key: str, prompt: str, model_name: str) -> str:
    """
    Sends the prompt to the specified provider using the given API key.
    Returns the text response.
    """
    if not api_key:
        return "Error: API Key is missing."

    try:
        if provider == "OpenAI":
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content

        elif provider == "Anthropic":
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model=model_name,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        elif provider == "Google Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
            
        else:
            return "Error: Unsupported provider."

    except Exception as e:
        return f"Error connecting to API: {str(e)}"
