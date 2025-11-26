import spacy
from typing import List

class NLPService:
    _instance = None
    
    def __init__(self):
        try:
            print("Loading SpaCy model 'es_core_news_sm'...")
            self.nlp = spacy.load("es_core_news_sm")
            print("SpaCy model loaded.")
        except OSError:
            print("SpaCy model not found. Please run: python -m spacy download es_core_news_sm")
            self.nlp = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def process_text(self, text: str):
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        tokens = []
        for token in doc:
            # Basic filtering: ignore punctuation unless critical
            if not token.is_punct:
                tokens.append({
                    "text": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "is_stop": token.is_stop
                })
        return tokens
