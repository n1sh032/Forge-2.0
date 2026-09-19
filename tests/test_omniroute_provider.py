import pytest
import requests

from src.providers.omniroute_provider import OmniRouteProvider


def omniroute_is_running():
    try:
        requests.get("http://localhost:20128/v1/models", timeout=2)
        return True
    except requests.exceptions.RequestException:
        return False


@pytest.mark.skipif(
    not omniroute_is_running(),
    reason="OmniRoute is not running on localhost:20128"
)
def test_ask_returns_text():

    provider = OmniRouteProvider()

    reply = provider.ask("Reply with exactly one word: hello")

    assert isinstance(reply, str)
    assert len(reply) > 0