import pytest

from src.manager.manager import Manager


def test_manager_can_start_without_provider_credentials(monkeypatch):
    monkeypatch.delenv("OMNIROUTE_API_KEY", raising=False)
    manager = Manager()
    manager.start_task("Describe a calculator")
