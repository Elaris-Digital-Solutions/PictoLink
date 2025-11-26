import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService

def debug_mi():
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    term = "mi"
    print(f"\nChecking for '{term}'...")
    matches = catalog.find_by_term(term)
    if matches:
        print(f"Found '{term}': ID {matches[0].id} ({matches[0].labels})")
    else:
        print(f"'{term}' NOT found in index.")
        
    # Check fuzzy just in case
    print(f"Fuzzy check for '{term}':")
    fuzzy = catalog.find_fuzzy(term)
    for p in fuzzy:
        print(f" - {p.labels['es']} (ID: {p.id})")

if __name__ == "__main__":
    debug_mi()
