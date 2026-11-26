import os
import requests
from dotenv import load_dotenv

load_dotenv()


class OmniRouteProvider:
    """
    Minimal wrapper around a local OmniRoute instance.

    OmniRoute exposes an OpenAI-compatible API. This class sends one
    prompt and returns the model's text reply. Also keeps a simple
    in-memory log of token usage per call. No retries, no persistence,
    no fallback yet - those come later.
    """

    def __init__(self, base_url="http://localhost:20128/v1", model="kiro/claude-haiku-4.5"):
        self.base_url = base_url
        self.model = model
        self.api_key = os.getenv("OMNIROUTE_API_KEY")
        self.usage_log = []

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
        self._log_usage(data)

        return data["choices"][0]["message"]["content"]

    def _log_usage(self, data):
        usage = data.get("usage", {})

        self.usage_log.append({
            "model": self.model,
            "input_tokens": usage.get("prompt_tokens"),
            "output_tokens": usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "raw_usage": usage
        })