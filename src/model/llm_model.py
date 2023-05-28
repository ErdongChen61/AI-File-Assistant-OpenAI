from langchain.llms import OpenAI
from src.utils.singleton import Singleton

class LlmModel(metaclass=Singleton):
    """A singleton class that loads the large language model."""

    def __init__(self) -> None:
        self.model = OpenAI(temperature=0)
