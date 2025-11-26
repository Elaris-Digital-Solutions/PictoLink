import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

def debug_sexual():
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    nlp = NLPService.get_instance()
    
    terms = ["masturbar", "masturbación", "masturbarse", "sexo"]
    
    print("\n--- Checking Terms ---", flush=True)
    for term in terms:
        matches = catalog.find_by_term(term)
        if matches:
            print(f"Found '{term}': ID {matches[0].id} ({matches[0].labels})", flush=True)
        else:
            print(f"'{term}' NOT found in index.", flush=True)
            
    print("\n--- Checking Lemmatization ---", flush=True)
    text = "quiero masturbarme"
    tokens = nlp.process_text(text)
    for t in tokens:
        print(f"Token: {t['text']} -> Lemma: {t['lemma']}", flush=True)

if __name__ == "__main__":
    debug_sexual()
