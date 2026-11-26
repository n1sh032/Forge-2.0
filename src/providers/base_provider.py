class BaseProvider:

    def __init__(self, name):
        self.name = name

    def generate(self, prompt):
        raise NotImplementedError("Provider must implement generate()")