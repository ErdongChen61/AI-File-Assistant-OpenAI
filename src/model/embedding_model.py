from langchain.embeddings import OpenAIEmbeddings
from src.utils.singleton import Singleton

class EmbeddingModel(metaclass=Singleton):
    """A singleton class that loads the embedding model for embedding text."""

    def __init__(self) -> None:
        self.model = OpenAIEmbeddings()
