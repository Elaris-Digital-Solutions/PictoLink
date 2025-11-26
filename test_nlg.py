import sys
import os
import asyncio
import json

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.nlg import NLGService
from nlp_backend.routers.translation import pictos_to_text, PictosRequest, PictoItem

async def run_nlg_test():
    print("Initializing NLG Service...")
    try:
        nlg = NLGService.get_instance()
        if not nlg.model:
            print("WARNING: Model not loaded correctly. Tests might fail or use fallback.")
    except Exception as e:
        print(f"Error initializing NLG: {e}")
        return

    test_cases = [
        {
            "lemmas": ["yo", "querer", "comer", "manzana"],
            "description": "Simple sentence: Yo quiero comer manzana"
        },
        {
            "lemmas": ["el", "perro", "estar", "dormir"],
            "description": "Conjugation: El perro está durmiendo"
        },
        {
            "lemmas": ["ir", "a", "casa"],
            "description": "Prepositions: Voy a casa"
        }
    ]
    
    print(f"\n{'='*80}")
    print(f"RUNNING NLG TESTS")
    print(f"{'='*80}\n")
    
    for case in test_cases:
        print(f"Test: {case['description']}")
        print(f"Input: {case['lemmas']}")
        
        # Test direct service call
        generated = nlg.generate_sentence(case['lemmas'])
        print(f"Generated (Service): '{generated}'")
        
        # Test endpoint simulation
        # Construct mock pictograms
        pictos = []
        for i, lemma in enumerate(case['lemmas']):
            pictos.append(PictoItem(
                id=i,
                labels={'es': lemma},
                image_urls={}
            ))
            
        request = PictosRequest(pictograms=pictos)
        response = await pictos_to_text(request)
        print(f"Generated (Endpoint): '{response['text']}'")
        
        print("-" * 40)

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(run_nlg_test())
