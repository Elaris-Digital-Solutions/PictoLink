import sys
import os
import asyncio
import json

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.routers.translation import text_to_pictos, TextRequest
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

async def run_semantic_test():
    print("Initializing services...")
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    
    # Ensure data exists
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    catalog.load_data(data_path)
    
    if not catalog.semantic_engine:
        print("WARNING: Semantic engine not loaded. Tests will likely fail or fallback to fuzzy.")
    
    nlp = NLPService.get_instance()
    
    test_cases = [
        # 1. Semantic Retrieval (Synonyms not in catalog)
        {
            "text": "automóvil",
            "expected_concept": "coche",
            "description": "Synonym: automóvil -> coche"
        },
        {
            "text": "can",
            "expected_concept": "perro",
            "description": "Synonym: can -> perro"
        },
        {
            "text": "laborar",
            "expected_concept": "trabajar",
            "description": "Synonym: laborar -> trabajar"
        },
        
        # 2. Context Re-ranking (Polysemy)
        {
            "text": "me siento en el banco",
            "expected_concept": "banco", # Should be the seat, not the bank
            # We can't easily check the exact ID without knowing it, but we can check the image URL or label
            # Ideally "banco" (seat) vs "banco" (money). 
            # Let's just print the result and manually verify for now, or check if we can distinguish.
            "description": "Polysemy: banco (seat)"
        },
        {
            "text": "voy al banco a sacar dinero",
            "expected_concept": "banco", # Should be the bank
            "description": "Polysemy: banco (money)"
        }
    ]
    
    print(f"\n{'='*80}")
    print(f"RUNNING SEMANTIC SEARCH TESTS")
    print(f"{'='*80}\n")
    
    for case in test_cases:
        print(f"Test: {case['description']}")
        print(f"Input: '{case['text']}'")
        
        request = TextRequest(text=case['text'])
        response = await text_to_pictos(request)
        
        pictos = response["pictograms"]
        if not pictos:
            print("❌ Result: No pictograms found.")
        else:
            # Print all found pictograms
            found = False
            print("Found pictograms:")
            for p in pictos:
                label = p.labels.get('es', 'unknown')
                print(f" - {label} (ID: {p.id})")
                if case['expected_concept'] in label.lower():
                    found = True
            
            if found:
                print(f"✅ Result: Success (Found '{case['expected_concept']}')")
            else:
                print(f"❌ Result: Failed (Expected '{case['expected_concept']}')")
        print("-" * 40)

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(run_semantic_test())
