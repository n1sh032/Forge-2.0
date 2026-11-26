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
