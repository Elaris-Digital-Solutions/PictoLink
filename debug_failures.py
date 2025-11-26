import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

def debug_failures():
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    nlp = NLPService.get_instance()
    
    # Test cases
    cases = [
        "necesito comunicarme",
        "quiero comprar algo",
        "voy a alimentarme"
    ]
    
    # Manual Map (Copy from translation.py to ensure we test the logic we intend)
    MANUAL_MAP = {
        'comunicar': 'comunicación',
        'alimentar': 'alimentación',
        'algo': 'cosa',
        'compra': 'compra', # comprar -> compra
        'comprar': 'compra',
    }
    
    print("\n--- Debugging Failures ---")
    
    for text in cases:
        print(f"\nInput: '{text}'")
        tokens = nlp.process_text(text)
        
        for token in tokens:
            text_lower = token['text'].lower()
            lemma = token['lemma'].lower()
            print(f"  Token: '{text_lower}' (Lemma: '{lemma}')")
            
            # 1. Manual Map Priority
            if text_lower in MANUAL_MAP:
                mapped = MANUAL_MAP[text_lower]
                print(f"    [Priority Map] '{text_lower}' -> '{mapped}'")
                matches = catalog.find_by_term(mapped)
                if matches:
                    print(f"    -> Found ID {matches[0].id} ({matches[0].labels['es']})")
                    continue
            
            # 2. Lemma
            matches = catalog.find_by_term(lemma)
            if matches:
                 print(f"    [Lemma] Found ID {matches[0].id} ({matches[0].labels['es']})")
                 continue
                 
            # 3. Reflexive
            for suffix in ['me', 'te', 'se', 'nos', 'os']:
                if text_lower.endswith(suffix):
                    stem = text_lower[:-len(suffix)]
                    print(f"    [Reflexive] Stem: '{stem}'")
                    
                    # Check Manual Map for stem
                    if stem in MANUAL_MAP:
                        mapped = MANUAL_MAP[stem]
                        print(f"    [Reflexive Map] '{stem}' -> '{mapped}'")
                        matches = catalog.find_by_term(mapped)
                        if matches:
                            print(f"    -> Found ID {matches[0].id} ({matches[0].labels['es']})")
                            break
                    
                    matches = catalog.find_by_term(stem)
                    if matches:
                        print(f"    [Reflexive Stem] Found ID {matches[0].id} ({matches[0].labels['es']})")
                        break

if __name__ == "__main__":
    debug_failures()
