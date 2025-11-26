import json
import os
from typing import List, Dict, Optional
from pydantic import BaseModel

class Pictogram(BaseModel):
    id: int
    labels: Dict[str, str]
    image_urls: Dict[str, str]

class CatalogService:
    _instance = None
    
    def __init__(self):
        self.index: Dict[str, List[Pictogram]] = {}
        self.pictograms: Dict[int, Pictogram] = {}
        self.loaded = False
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def load_data(self, file_path: str):
        if self.loaded:
            return
            
        print(f"Loading catalog from {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        picto = Pictogram(
                            id=data['id'],
                            labels=data.get('labels', {}),
                            image_urls=data.get('image_urls', {})
                        )
                        
                        self.pictograms[picto.id] = picto
                        
                        # Index by Spanish label
                        if 'es' in picto.labels:
                            label = picto.labels['es'].lower()
                            if label not in self.index:
                                self.index[label] = []
                            self.index[label].append(picto)
                            
                            # Also index normalized version (remove accents/tildes)
                            # e.g. "bañar" -> "banar", "avión" -> "avion"
                            import unicodedata
                            normalized = ''.join(c for c in unicodedata.normalize('NFD', label) if unicodedata.category(c) != 'Mn')
                            if normalized != label:
                                if normalized not in self.index:
                                    self.index[normalized] = []
                                self.index[normalized].append(picto)
                            
                        # Index by synonyms (if available in the raw data, usually in 'keywords' or similar)
                        # Note: The raw Arasaac format varies. We'll stick to labels for now to match frontend logic.
                        # If synonyms are needed, we'd check data.get('keywords', []) or similar.
                        
                    except Exception as e:
                        continue
            self.loaded = True
            print(f"Loaded {len(self.pictograms)} pictograms.")
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")

    def find_by_term(self, term: str) -> List[Pictogram]:
        term = term.lower().strip()
        return self.index.get(term, [])

    def find_fuzzy(self, term: str, threshold: int = 80) -> List[Pictogram]:
        """
        Find pictograms using fuzzy matching on the index keys.
        """
        from thefuzz import process, fuzz
        
        term = term.lower().strip()
        if not term:
            return []
            
        # Get top 3 matches using Ratio (stricter than partial)
        matches = process.extract(term, self.index.keys(), limit=3, scorer=fuzz.ratio)
        
        results = []
        for match_term, score in matches:
            if score >= threshold:
                print(f"Fuzzy match: '{term}' -> '{match_term}' (score: {score})")
                results.extend(self.index.get(match_term, []))
                
        return results

    def search_autocomplete(self, query: str, limit: int = 10) -> List[str]:
        """
        Returns a list of suggested terms starting with query.
        """
        query = query.lower().strip()
        if not query:
            return []
            
        suggestions = []
        # Inefficient linear scan of keys (for MVP it's okay given ~10k keys)
        # For production, use a Trie or prefix index.
        count = 0
        for key in self.index.keys():
            if key.startswith(query):
                suggestions.append(key)
                count += 1
                if count >= limit:
                    break
        return suggestions
        
    def get_by_id(self, picto_id: int) -> Optional[Pictogram]:
        return self.pictograms.get(picto_id)
