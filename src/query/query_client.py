import logging

from abc import abstractmethod
from langchain.chains import RetrievalQAWithSourcesChain
from src.database.vector_embedding.chroma_client import ChromaClient, ImageChromaClient, PdfChromaClient
from src.model.llm_model import LlmModel
from src.utils.singleton import Singleton
from typing import Dict, Sequence

logger = logging.getLogger(__name__)

class QueryClient:
    """QueryClient is the main interface for querying with the vector embedding database."""

    def __init__(self, chrome_client: ChromaClient, llm_model: LlmModel) -> None:
        self.chrome_client = chrome_client
        self.llm_model = llm_model
        self.chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=self.llm_model.model, 
            chain_type="stuff", 
            retriever=self.chrome_client.as_retriever()) 
       
    @abstractmethod
    def query(self, query: str) -> Dict[str, str]:
        """Perform a query."""
        pass

class ImageQueryClient(QueryClient, metaclass=Singleton):
    """ImageQueryClient is the main interface for querying the image embedding data."""

    def __init__(self, chrome_client: ImageChromaClient, llm_model: LlmModel) -> None:
        super().__init__(chrome_client, llm_model)

    def query(self, query: str) -> Dict[str, str]:
        """Perform a query."""
        prompt = 'Which image file contains the following key words {}:'.format(query)
        return self.chain({"question": prompt}, return_only_outputs=True)
        
class PdfQueryClient(QueryClient, metaclass=Singleton):
    """PdfQueryClient is the main interface for querying the PDF embedding data."""

    def __init__(self, chrome_client: PdfChromaClient, llm_model: LlmModel) -> None:
        super().__init__(chrome_client, llm_model)

    def query(self, query: str) -> Dict[str, str]:
        """Perform a query."""
        return self.chain({"question": query}, return_only_outputs=True)
