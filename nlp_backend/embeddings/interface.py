from abc import ABC, abstractmethod
from typing import List
from nlp_backend.services.catalog import Pictogram

class SemanticSearchEngine(ABC):
    @abstractmethod
    def index_catalog(self, pictograms: List[Pictogram]):
        """
        Builds the vector index from the catalog.
        """
        pass
        
    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[Pictogram]:
        """
        Returns semantically similar pictograms.
        """
        pass
