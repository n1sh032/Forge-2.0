import os
import json

from .base_agent import BaseAgent
from src.providers.omniroute_provider import OmniRouteProvider


class Coder(BaseAgent):

    def __init__(self, provider=None, project_root="."):
        super().__init__("Coder")
        self.provider = provider or OmniRouteProvider()
        self.project_root = project_root

    def run(self, step):
        file_list = self._list_project_files()
        relevant_files = self._pick_relevant_files(step, file_list)
        file_contents = self._read_files(relevant_files)
