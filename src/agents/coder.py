import os
import json

from .base_agent import BaseAgent
from src.providers.omniroute_provider import OmniRouteProvider


class Coder(BaseAgent):

    def __init__(self, provider=None, project_root="."):
        super().__init__("Coder")
        self.provider = provider or OmniRouteProvider()
