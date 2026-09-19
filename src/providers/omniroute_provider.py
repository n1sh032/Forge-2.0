import os
import requests
from dotenv import load_dotenv

load_dotenv()


class OmniRouteProvider:
    """
    Minimal wrapper around a local OmniRoute instance.

    OmniRoute exposes an OpenAI-compatible API. This class sends one
    prompt and returns the model's text reply. No retries, no token
    tracking, no fallback yet - those come later.
    """

    def __init__(self, base_url="http://localhost:20128/v1", model="kiro/claude-haiku-4.5"):
        self.base_url = base_url
        self.model = model
        self.api_key = os.getenv("OMNIROUTE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OMNIROUTE_API_KEY is not set. Add it to your .env file."
            )

    def ask(self, prompt):
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]