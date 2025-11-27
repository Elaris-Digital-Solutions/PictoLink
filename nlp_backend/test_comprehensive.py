
import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_backend.routers.translation import text_to_pictos, TextRequest
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

async def run_tests():
    # Initialize services
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', 'embeddings', 'meta.jsonl')
    
    print(f"Loading catalog...")
    catalog = CatalogService.get_instance()
    catalog.load_data(data_path)
    nlp = NLPService.get_instance()
    
    test_cases = [
        {
            "input": "bajar las escaleras",
            "expected_count": 1,
            "description": "Exact phrase match"
        },
        {
            "input": "quiero comer",
            "expected_count": 2, # querer + comer
            "description": "Verb conjugation (quiero -> querer)"
        },
        {
            "input": "el perro",
            "expected_count": 1, # perro (el should be skipped/mapped or handled)
            "check_content": ["perro"],
            "description": "Stopword filtering (el perro)"
        },
        {
            "input": "cepillar los dientes",
            "expected_count": 1,
            "description": "Reflexive phrase"
        },
        {
            "input": "me lavo los dientes",
            "expected_count": 1,
            "description": "Conjugated reflexive phrase"
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting: '{case['input']}' ({case['description']})")
        request = TextRequest(text=case['input'])
        response = await text_to_pictos(request)
        pictos = response['pictograms']
        
        print(f"Result count: {len(pictos)}")
        labels = [p.labels.get('es') for p in pictos]
        print(f"Labels: {labels}")
        
        if 'expected_count' in case:
            if len(pictos) == case['expected_count']:
                print("PASS: Count matches")
            else:
                print(f"WARN: Count mismatch (Expected {case['expected_count']}, got {len(pictos)})")
                
        if 'check_content' in case:
            for item in case['check_content']:
                if item in labels:
                    print(f"PASS: Found '{item}'")
                else:
                    print(f"FAIL: Missing '{item}'")

if __name__ == "__main__":
    asyncio.run(run_tests())
