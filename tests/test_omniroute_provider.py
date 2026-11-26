import pytest
import requests

from src.providers.omniroute_provider import OmniRouteProvider


def omniroute_is_running():
    try:
        requests.get("http://localhost:20128/v1/models", timeout=2)
        return True
    except requests.exceptions.RequestException:
        return False
