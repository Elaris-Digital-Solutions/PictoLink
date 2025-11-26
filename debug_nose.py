import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

def debug_nose():
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    nlp = NLPService.get_instance()
    
    text = "no se que hacer"
    print(f"\nAnalyzing sentence: '{text}'")
    
    tokens = nlp.process_text(text)
    print("\nTokens:", flush=True)
    for t in tokens:
        print(f" - Text: '{t['text']}', Lemma: '{t['lemma']}', POS: '{t['pos']}', Stop: {t['is_stop']}", flush=True)
        
    # Check 'se' in catalog
    print("\nChecking 'se' in catalog:")
    matches = catalog.find_by_term("se")
    if matches:
        print(f"Found 'se': ID {matches[0].id} ({matches[0].labels})")
    else:
        print("'se' NOT found in index.")

    # Check 'hacer' in catalog
    print("\nChecking 'hacer' in catalog:")
    matches = catalog.find_by_term("hacer")
    if matches:
        print(f"Found 'hacer': ID {matches[0].id} ({matches[0].labels})")
    else:
        print("'hacer' NOT found in index.")

if __name__ == "__main__":
    debug_nose()
