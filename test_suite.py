import sys
import os
import json

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

def run_stress_test():
    # Force UTF-8 for Windows console
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

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
        {"input": "que es eso", "expected": ["qué", "ser", "ese"]}, # 'eso' might map to 'ese' or 'eso'
        {"input": "cuando vamos a casa", "expected": ["cuándo", "ir", "a", "casa"]},
        
        # 4. Commands/Requests
        {"input": "dame la pelota", "expected": ["dar", "la", "pelota"]},
        {"input": "abre la puerta", "expected": ["abrir", "la", "puerta"]},
        {"input": "ven aqui", "expected": ["venir", "aquí"]},
        
        # 5. Complex Grammar (Pronouns, Diminutives, Reflexives)
        {"input": "me lavo las manos", "expected": ["yo", "lavar", "las", "mano"]},
        {"input": "mi perrito come", "expected": ["mío", "perro", "comer"]},
        {"input": "voy a ganar yo solito", "expected": ["ir", "a", "ganar", "yo", "solo"]},
        {"input": "te quiero mucho", "expected": ["tú", "querer", "mucho"]},
        
        # 6. Negation
        {"input": "no quiero comer", "expected": ["no", "querer", "comer"]},
        {"input": "no me gusta", "expected": ["no", "yo", "gustar"]},
        
        # 7. Proactive Strengthening (New Mappings)
        {"input": "quiero masturbarme", "expected": ["querer", "masturbación", "yo"]},
        {"input": "necesito comunicarme", "expected": ["necesitar", "comunicación", "yo"]},
        {"input": "voy a alimentarme", "expected": ["ir", "a", "alimentación", "yo"]},
        {"input": "me gusta viajar", "expected": ["yo", "gustar", "viaje"]},
        {"input": "tengo que estudiar", "expected": ["tener", "que", "estudiar"]}, # estudiar usually exists
        {"input": "quiero comprar algo", "expected": ["querer", "compra", "algo"]},
    ]
    
    print(f"\nRunning {len(test_cases)} stress tests...\n")
    
    passed = 0
    failed = 0
    
    for i, case in enumerate(test_cases):
        text = case["input"]
        expected_keywords = case["expected"]
        
        # Run translation logic (simulating the router)
        # We need to mock the router's logic or import it. 
        # Since we can't easily import the router function without FastAPI context, 
        # we'll use a simplified version of the logic here or try to import the core logic if possible.
        # Actually, let's just use the router function if it's separable.
        # Looking at translation.py, the logic is in `convert_text_to_pictos`.
        # We need to mock the request/response structure or just extract the logic.
        # For now, let's rely on the fact that we imported `convert_text_to_pictos`
        # BUT `convert_text_to_pictos` is an async route handler.
        # We'll just replicate the core logic loop here for testing to avoid async complexity in this script.
        
        # ... Replicating logic for test speed ...
        tokens = nlp.process_text(text)
        
        # Copy-paste of the core logic from translation.py (simplified)
        result_pictos = []
        potential_pictos = []
        
    # Manual Mappings for critical words missing in catalog or needing semantic shift
    manual_map = {
        # Possessives
        'mi': 'mío', 'mis': 'mis',
        'tu': 'tú', 'tus': 'tú',
        'su': 'su', 'sus': 'su',
        'nuestro': 'nuestro', 'nuestra': 'nuestra',
        
        # Articles
        'un': 'uno', 'una': 'uno', 'unos': 'uno', 'unas': 'uno',
        'el': 'el', 'la': 'la', 'los': 'los', 'las': 'las',
        'al': 'al', 'del': 'del',
        
        # Pronouns
        'yo': 'yo', 'me': 'yo', 'mí': 'yo',
        'tú': 'tú', 'te': 'tú', 'ti': 'tú',
        'él': 'él', 'lo': 'él', 'le': 'él',
        'ella': 'ella', 'la': 'ella',
        'nosotros': 'nosotros', 'nos': 'nosotros',
        'vosotros': 'vosotros', 'os': 'vosotros',
        'ellos': 'ellos', 'les': 'ellos',
        
        # Question words
        'qué': 'qué', 'que': 'qué',
        'quién': 'quién', 'quien': 'quién',
        'cómo': 'cómo', 'como': 'cómo',
        'cuándo': 'cuándo', 'cuando': 'cuándo',
        'dónde': 'dónde', 'donde': 'dónde',
        'cuánto': 'cuánto', 'cuanto': 'cuánto',
        'por qué': 'por qué', 'porque': 'por qué',
        
        # Adverbs/Conjunctions
        'sí': 'sí', 'si': 'sí',
        'no': 'no',
        'y': 'y', 'o': 'o',
        'pero': 'pero',
        'muy': 'mucho',
        'más': 'más',
        'a': 'a', 'de': 'de', 'en': 'en', 'con': 'con', 'por': 'por', 'para': 'para',
        
        # Semantic mappings
        'masturbar': 'masturbación',
        'alimentar': 'alimentación',
        'comunicar': 'comunicación',
        'educar': 'educación',
        'respirar': 'respiración',
        'caminar': 'andar',
        'viajar': 'viaje',
        'pintar': 'pintura',
        'limpiar': 'limpieza',
        'comprar': 'compra',
        'vender': 'venta',
        'necesitar': 'necesidad',
        'odiar': 'odio',
        'sentir': 'sentimiento',
        'pensar': 'pensamiento',
        'saber': 'sabiduría',
        'algo': 'cosa',
    }

    for token in tokens:
        text_lower = token['text'].lower()
        matches = []
        
        # Strategy 0: Check Manual Map FIRST
        if text_lower in manual_map:
             mapped_term = manual_map[text_lower]
             matches = catalog.find_by_term(mapped_term)
        
        # Strategy 1: Search by lemma
        if not matches:
            matches = catalog.find_by_term(token['lemma'])
        
        # Strategy 2: Search by original text
        if not matches:
            matches = catalog.find_by_term(token['text'])
        
        if not matches:
            # Reflexive
            for suffix in ['me', 'te', 'se', 'nos', 'os']:
                if text_lower.endswith(suffix) and len(text_lower) > len(suffix) + 3:
                    stem = text_lower[:-len(suffix)]
                    
                    # Check Manual Map for stem FIRST
                    if stem in manual_map:
                        matches = catalog.find_by_term(manual_map[stem])
                        if matches: break
                        
                    matches = catalog.find_by_term(stem)
                    
                    if not matches:
                         matches = catalog.find_fuzzy(stem, threshold=85)
                    if matches: break
            
            if not matches:
                # Diminutive
                diminutive_rules = [
                    ('citos', ''), ('citas', ''), ('cito', ''), ('cita', ''),
                    ('itos', 'os'), ('itas', 'as'), ('ito', 'o'), ('ita', 'a'),
                    ('illos', 'os'), ('illas', 'as'), ('illo', 'o'), ('illa', 'a'),
                    ('icos', 'os'), ('icas', 'as'), ('ico', 'o'), ('ica', 'a')
                ]
                for suffix, replacement in diminutive_rules:
                    if text_lower.endswith(suffix) and len(text_lower) > len(suffix) + 2:
                        stem = text_lower[:-len(suffix)] + replacement
                        matches = catalog.find_by_term(stem)
                        if matches: break
                        if replacement != '':
                            stem_stripped = text_lower[:-len(suffix)]
                            matches = catalog.find_by_term(stem_stripped)
                            if matches: break
            
            if not matches:
                # Manual Map (Fallback)
                if text_lower in manual_map:
                    matches = catalog.find_by_term(manual_map[text_lower])
            
            if not matches and len(token['text']) > 3:
                # Fuzzy
                matches = catalog.find_fuzzy(token['text'])
                
            if matches:
                picto = matches[0]
                result_pictos.append(picto)
            
        # Verify
        result_labels = [p.labels['es'].lower() for p in result_pictos]
        
        # Check if all expected keywords are present (loose check)
        missing = []
        for kw in expected_keywords:
            # We check if the keyword is contained in any of the result labels
            # or if the result label is contained in the keyword (approximate)
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
    run_stress_test()
