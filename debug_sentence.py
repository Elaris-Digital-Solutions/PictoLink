import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

def debug_sentence():
    # Initialize services
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    nlp = NLPService.get_instance()
    
    text = "mi perrito pequeñito come su panecillo con su abuelita"
    print(f"\nAnalyzing sentence: '{text}'")
    
    # 1. NLP Processing
    tokens = nlp.process_text(text)
    print("\nTokens:")
    for t in tokens:
        print(f" - Text: '{t['text']}', Lemma: '{t['lemma']}', Stop: {t['is_stop']}")
        
    print("\nMatching:")
    for token in tokens:
        print(f"\nProcessing token: '{token['text']}' (Lemma: '{token['lemma']}')")
        
        # Strategy 1: Lemma
        matches = catalog.find_by_term(token['lemma'])
        if matches:
            print(f"   [Lemma Match] '{token['lemma']}' -> ID {matches[0].id} ({matches[0].labels['es']})")
        else:
            print(f"   [Lemma Fail] '{token['lemma']}'")
            
            # Strategy 2: Text
            matches = catalog.find_by_term(token['text'])
            if matches:
                print(f"   [Text Match] '{token['text']}' -> ID {matches[0].id} ({matches[0].labels['es']})")
            else:
                print(f"   [Text Fail] '{token['text']}'")
                
                # Strategy 3: Fuzzy
                if len(token['text']) > 3:
                    print("   [Fuzzy Search] Trying...")
                    results = catalog.find_fuzzy(token['text'])
                    if results:
                        # find_fuzzy returns list of pictos, but doesn't tell us WHICH term matched.
                        # We need to hack find_fuzzy or just re-run process.extract here to see.
                        from thefuzz import process
                        matches = process.extract(token['text'], catalog.index.keys(), limit=1)
                        matched_term = matches[0][0]
                        score = matches[0][1]
                        print(f"   [Fuzzy Match] '{token['text']}' matched '{matched_term}' (Score: {score})")
                        print(f"   -> Mapped to ID {results[0].id}")
                    else:
                        print("   [Fuzzy Fail]")
                else:
                    print("   [Fuzzy Skip] Too short")

if __name__ == "__main__":
    debug_sentence()
