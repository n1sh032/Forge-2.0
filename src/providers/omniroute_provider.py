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
