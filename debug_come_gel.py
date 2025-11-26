import sys
import os
import json
from unittest.mock import MagicMock

# Mock semantic_analysis
sys.modules['semantic_analysis'] = MagicMock()

# Add project root to path
sys.path.append(os.getcwd())

from nlp_backend.map_pictograms import load_pictogram_catalog, META_PATH

def reproduce_issue():
    print(f"CWD: {os.getcwd()}")
    print(f"META_PATH: {META_PATH}")
    abs_path = os.path.abspath(META_PATH)
    print(f"Absolute META_PATH: {abs_path}")
    print(f"File exists: {os.path.exists(abs_path)}")
    
    try:
        catalog = load_pictogram_catalog()
        print(f"Catalog loaded. Size: {len(catalog)}")
        
        with open("debug_output.txt", "w", encoding="utf-8") as f:
            f.write(f"Catalog loaded. Size: {len(catalog)}\n")
            
            term = "come"
            f.write(f"\nTesting term: '{term}'\n")
            
            # 1. Exact match
            if term in catalog:
                f.write(f"Exact match: {catalog[term]['id']}\n")
            else:
                f.write("Exact match: None\n")
                
            # 2. Fuzzy match
            from thefuzz import process, fuzz
            keys = list(catalog.keys())
            fuzzy = process.extract(term, keys, limit=10)
            f.write(f"Fuzzy match: {fuzzy}\n")
            
            # Check score for 'gel'
            score = fuzz.ratio(term, "gel")
            partial_score = fuzz.partial_ratio(term, "gel")
            token_sort = fuzz.token_sort_ratio(term, "gel")
            f.write(f"\n'come' vs 'gel' scores:\n")
            f.write(f"Ratio: {score}\n")
            f.write(f"Partial Ratio: {partial_score}\n")
            f.write(f"Token Sort Ratio: {token_sort}\n")
            
            # Check if 'gel' is in the top matches
            gel_in_fuzzy = any(m[0] == 'gel' for m in fuzzy)
            f.write(f"'gel' in top fuzzy matches: {gel_in_fuzzy}\n")
            
            if 'gel' in catalog:
                f.write(f"\n'gel' ID: {catalog['gel']['id']}\n")
            
    except Exception as e:
        print(f"Error loading catalog: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce_issue()
