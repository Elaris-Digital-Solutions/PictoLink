import os
import json
import numpy as np
import faiss
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
from nlp_backend.embeddings.interface import SemanticSearchEngine
from nlp_backend.services.catalog import Pictogram

class FaissBackend(SemanticSearchEngine):
    def __init__(self, model_name: str = "distiluse-base-multilingual-cased-v2"):
        print(f"Loading SentenceTransformer model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.pictograms: List[Pictogram] = []
        self.id_map: Dict[int, int] = {} # FAISS index ID -> Pictogram ID
        print("Model loaded.")

    def _get_text_representation(self, picto: Pictogram) -> str:
        """
        Constructs a rich text representation for the pictogram.
        """
        texts = []
        # Main label
        if 'es' in picto.labels:
            texts.append(picto.labels['es'])
        
        # Synonyms (we don't have them in the Pictogram model yet, but if we did...)
        # For now, we rely on what's available. 
        # If the raw data had keywords, we'd use them.
        
        return " ".join(texts)

    def index_catalog(self, pictograms: List[Pictogram]):
        print(f"Indexing {len(pictograms)} pictograms...")
        self.pictograms = pictograms
        self.id_map = {p.id: i for i, p in enumerate(pictograms)}
        
        texts = [self._get_text_representation(p) for p in pictograms]
        
        # Encode texts
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension) # Inner Product + Normalized = Cosine Similarity
        self.index.add(embeddings)
        
        print(f"Index built with {self.index.ntotal} vectors.")

    def search(self, query: str, limit: int = 10) -> List[Tuple[Pictogram, float]]:
        if not self.index:
            return []
            
        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, limit)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.pictograms):
                score = float(distances[0][i])
                picto = self.pictograms[idx]
                results.append((picto, score))
                
        return results

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Helper to get embedding for a single text (used for re-ranking).
        """
        embedding = self.model.encode([text], convert_to_numpy=True)
        faiss.normalize_L2(embedding)
        return embedding[0]
        
    def get_vector_by_id(self, picto_id: int) -> Optional[np.ndarray]:
        """
        Retrieve the pre-computed embedding for a pictogram by its ID.
        """
        if not self.index or picto_id not in self.id_map:
            return None
            
        idx = self.id_map[picto_id]
        try:
            # Reconstruct vector from FAISS index
            vector = self.index.reconstruct(idx)
            # Ensure it's a numpy array (FAISS might return float array)
            return np.array(vector)
        except Exception as e:
            print(f"Error retrieving vector for ID {picto_id}: {e}")
            return None

    def save(self, path_prefix: str):
        if not self.index:
            return
            
        # Save FAISS index
        index_path = f"{path_prefix}.index"
        faiss.write_index(self.index, index_path)
        
        # Save metadata (mapping from index ID to Pictogram ID)
        meta_path = f"{path_prefix}.meta.json"
        meta = {
            "picto_ids": [p.id for p in self.pictograms if p is not None]
        }
        with open(meta_path, 'w') as f:
            json.dump(meta, f)
            
        print(f"Index saved to {index_path}")

    def load(self, path_prefix: str) -> bool:
        index_path = f"{path_prefix}.index"
        meta_path = f"{path_prefix}.meta.json"
        
        if not os.path.exists(index_path) or not os.path.exists(meta_path):
            return False
            
        try:
            self.index = faiss.read_index(index_path)
            with open(meta_path, 'r') as f:
                meta = json.load(f)
                self.loaded_picto_ids = meta["picto_ids"] # Store for later linking
            print(f"Index loaded from {index_path}")
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False

    def link_pictograms(self, all_pictograms: Dict[int, Pictogram]):
        """
        After loading index, we need to reconstruct self.pictograms list 
        using the loaded IDs and the full catalog.
        """
        if not hasattr(self, 'loaded_picto_ids'):
            return
            
        self.pictograms = []
        self.id_map = {}
        
        for i, pid in enumerate(self.loaded_picto_ids):
            if pid in all_pictograms:
                picto = all_pictograms[pid]
                self.pictograms.append(picto)
                self.id_map[pid] = i
            else:
                # Should not happen if catalog is consistent
                print(f"Warning: Pictogram ID {pid} in index but not in catalog.")
                self.pictograms.append(None) 
 
