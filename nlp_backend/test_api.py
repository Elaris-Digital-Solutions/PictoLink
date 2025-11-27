
import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_backend.routers.translation import text_to_pictos, TextRequest
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

async def test_api_logic():
    # Initialize services
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming data is in ../data relative to nlp_backend/test_api.py
    data_path = os.path.join(base_dir, '..', 'data', 'embeddings', 'meta.jsonl')
    
    print(f"Loading catalog from {data_path}...")
    catalog = CatalogService.get_instance()
    catalog.load_data(data_path)
    
    nlp = NLPService.get_instance()
    
    # Test case
    text = "bajar las escaleras"
    print(f"\nTesting phrase: '{text}'")
    
    try:
        request = TextRequest(text=text)
        response = await text_to_pictos(request)
        
        print(f"Result pictograms: {len(response['pictograms'])}")
        for p in response['pictograms']:
            print(f"ID: {p.id}, Label: {p.labels.get('es')}")
            
        if len(response['pictograms']) == 1 and response['pictograms'][0].id == 2654:
            print("SUCCESS: Correctly identified single pictogram.")
        else:
            print("FAILURE: Did not identify single pictogram.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api_logic())
