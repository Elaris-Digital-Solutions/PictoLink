from abc import ABC, abstractmethod
from typing import List, Tuple
from nlp_backend.services.catalog import Pictogram

class SemanticSearchEngine(ABC):
    @abstractmethod
    def index_catalog(self, pictograms: List[Pictogram]):
        """
        Builds the vector index from the catalog.
        """
        pass
        
    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[Tuple[Pictogram, float]]:
        """
        Returns semantically similar pictograms with their scores.
        """
        pass
    
    @abstractmethod
    def save(self, path: str):
        """
        Saves the index to disk.
        """
        pass
    
    @abstractmethod
    def load(self, path: str) -> bool:
        """
        Loads the index from disk. Returns True if successful.
        """
        pass
