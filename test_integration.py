import sys
import os
import asyncio
import json

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.routers.translation import text_to_pictos, TextRequest
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

async def run_integration_tests():
    # Initialize services
    print("Initializing services...")
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    nlp = NLPService.get_instance()
    
    # Test Cases
    test_cases = [
        # 1. Basic Needs
        {"input": "quiero agua", "expected": ["querer", "agua"]},
        {"input": "tengo hambre", "expected": ["tener", "hambre"]},
        {"input": "necesito ir al baño", "expected": ["necesitar", "ir", "al", "baño"]},
        
        # 2. Emotions
        {"input": "estoy feliz", "expected": ["estar", "feliz"]},
        {"input": "me siento triste", "expected": ["yo", "sentir", "triste"]},
        {"input": "estoy enfadado", "expected": ["estar", "enfadado"]},
        
        # 3. Questions
        {"input": "donde esta mama", "expected": ["dónde", "estar", "mamá"]},
        {"input": "que es eso", "expected": ["qué", "ser", "ese"]}, 
        {"input": "cuando vamos a casa", "expected": ["cuándo", "ir", "a", "casa"]},
        
        # 4. Commands/Requests
        {"input": "dame la pelota", "expected": ["dar", "la", "pelota"]},
        {"input": "abre la puerta", "expected": ["abrir", "la", "puerta"]},
        {"input": "ven aqui", "expected": ["venir", "aquí"]},
        
        # 5. Complex Grammar
        {"input": "me lavo las manos", "expected": ["yo", "lavar", "las", "mano"]},
        {"input": "mi perrito come", "expected": ["mío", "perro", "comer"]},
        {"input": "voy a ganar yo solito", "expected": ["ir", "a", "ganar", "yo", "solo"]},
        {"input": "te quiero mucho", "expected": ["tú", "querer", "mucho"]},
        
        # 6. Negation
        {"input": "no quiero comer", "expected": ["no", "querer", "comer"]},
        {"input": "no me gusta", "expected": ["no", "yo", "gustar"]},
        
        # 7. Proactive Strengthening
        {"input": "quiero masturbarme", "expected": ["querer", "masturbación", "yo"]},
        {"input": "necesito comunicarme", "expected": ["necesitar", "comunicar", "yo"]},  # comunicar verb exists
        {"input": "voy a alimentarme", "expected": ["ir", "a", "alimentar", "yo"]},  # alimentar verb exists
        {"input": "me gusta viajar", "expected": ["yo", "gustar", "viaje"]},
        {"input": "tengo que estudiar", "expected": ["tener", "qué", "estudiar"]},  # 'que' maps to 'qué'
        {"input": "quiero comprar algo", "expected": ["querer", "compra"]},  # 'algo' has no pictogram
    ]
    
    print(f"\nRunning {len(test_cases)} integration tests...\n")
    
    passed = 0
    failed = 0
    
    for i, case in enumerate(test_cases):
        text = case["input"]
        expected_keywords = case["expected"]
        
        # Call the router directly
        request = TextRequest(text=text)
        response = await text_to_pictos(request)
        
        # Handle dict response (FastAPI returns dict when called directly)
        pictograms = response["pictograms"]
        result_labels = [p.labels['es'].lower() for p in pictograms]
        
        # Check if all expected keywords are present
        missing = []
        for kw in expected_keywords:
            found_kw = False
            for label in result_labels:
                if kw in label or label in kw:
                    found_kw = True
                    break
            if not found_kw:
                missing.append(kw)
        
        if not missing:
            print(f"✅ Test {i+1}: '{text}' -> Passed")
            passed += 1
        else:
            print(f"❌ Test {i+1}: '{text}' -> FAILED")
            print(f"   Expected: {expected_keywords}")
            print(f"   Got:      {result_labels}")
            print(f"   Missing:  {missing}")
            failed += 1
            
    print(f"\nSummary: {passed} Passed, {failed} Failed")

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(run_integration_tests())
