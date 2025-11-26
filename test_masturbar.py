import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

def test_masturbar_fix():
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    nlp = NLPService.get_instance()
    
    text = "quiero masturbarme"
    print(f"\nTesting: '{text}'")
    
    tokens = nlp.process_text(text)
    
    manual_map = {
        'masturbar': 'masturbación'
    }
    
    for token in tokens:
        print(f"Token: '{token['text']}'", flush=True)
        
        # Simulate translation.py logic
        # 1. Lemma check
        lemma = token['lemma'].lower()
        matches = catalog.find_by_term(lemma)
        
        # 2. Reflexive check (simplified)
        if not matches:
            text = token['text'].lower()
            for suffix in ['me', 'te', 'se', 'nos', 'os']:
                if text.endswith(suffix):
                    stem = text[:-len(suffix)]
                    print(f"   [Reflexive] Stem: '{stem}'")
                    matches = catalog.find_by_term(stem)
                    
                    if not matches and stem in manual_map:
                        mapped = manual_map[stem]
                        print(f"   [Manual Map] Stem '{stem}' -> '{mapped}'")
                        matches = catalog.find_by_term(mapped)
                    
                    if matches: break

        if matches:
            print(f"   -> Found ID {matches[0].id} ({matches[0].labels['es']})")
        else:
            print("   -> NOT FOUND")

if __name__ == "__main__":
    test_masturbar_fix()
