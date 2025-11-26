import sys
import os

# Add the current directory to sys.path so we can import nlp_backend
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService

def debug_fuzzy():
    catalog = CatalogService.get_instance()
    # Assuming the data file is at nlp_backend/data/arasaac_catalog.jsonl
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    catalog.load_data(data_path)
    
    term = "banar"
    print(f"\nTesting fuzzy search for '{term}'...", flush=True)
    results = catalog.find_fuzzy(term, threshold=60) # Lower threshold to see what comes up
    
    # We need to hack find_fuzzy to see scores or just use process.extract here
    from thefuzz import process, fuzz
    print(f"\nDirect fuzzy scores for '{term}' with fuzz.ratio:", flush=True)
    matches = process.extract(term, catalog.index.keys(), limit=5, scorer=fuzz.ratio)
    for m, score in matches:
        print(f" - '{m}': {score}", flush=True)

if __name__ == "__main__":
    debug_fuzzy()
