import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService

def check_conflicts():
    # Force UTF-8 for Windows console
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    # 1. Reflexive Verbs to check (stem existence)
    reflexives = [
        "duchar", "lavar", "peinar", "vestir", "sentar", "levantar", "acostar", "despertar", 
        "llamar", "ir", "quedar", "poner", "quitar", "bañar", "cepillar", "afeitar", 
        "maquillar", "relajar", "divertir", "aburrir", "casar", "divorciar", "enamorar", 
        "enfadar", "asustar", "preocupar", "reír", "sonreír", "dormir", "comer", "beber"
    ]
    
    # 2. Potential Semantic Gaps (Verb -> Noun mapping candidates)
    # Words that are often used as verbs but might only exist as nouns in the catalog
    semantic_checks = [
        ("alimentar", "alimentación"),
        ("comunicar", "comunicación"),
        ("educar", "educación"),
        ("respirar", "respiración"),
        ("caminar", "camino"), # or andar
        ("viajar", "viaje"),
        ("trabajar", "trabajo"),
        ("jugar", "juego"),
        ("pintar", "pintura"),
        ("cocinar", "cocina"),
        ("limpiar", "limpieza"),
        ("comprar", "compra"),
        ("vender", "venta"),
        ("ayudar", "ayuda"),
        ("necesitar", "necesidad"),
        ("querer", "deseo"), # or amor?
        ("amar", "amor"),
        ("odiar", "odio"),
        ("sentir", "sentimiento"),
        ("pensar", "pensamiento"),
        ("saber", "sabiduría"), # or conocimiento
    ]
    
    print("\n--- Checking Reflexive Stems ---")
    missing_stems = []
    for stem in reflexives:
        matches = catalog.find_by_term(stem)
        if not matches:
            print(f"MISSING STEM: {stem}")
            missing_stems.append(stem)
        else:
            # Optional: print(f"Found: {stem} -> ID {matches[0].id}")
            pass
            
    print(f"Total missing stems: {len(missing_stems)}")
    
    print("\n--- Checking Semantic Gaps ---")
    gaps = []
    for verb, noun in semantic_checks:
        # Check if verb exists
        verb_matches = catalog.find_by_term(verb)
        if not verb_matches:
            print(f"Verb '{verb}' NOT found.")
            # Check if noun exists
            noun_matches = catalog.find_by_term(noun)
            if noun_matches:
                print(f"  -> Noun '{noun}' FOUND (ID {noun_matches[0].id}). Candidate for mapping!")
                gaps.append((verb, noun))
            else:
                print(f"  -> Noun '{noun}' ALSO NOT FOUND.")
        else:
            # Verb exists, no need to map (usually)
            # print(f"Verb '{verb}' found (ID {verb_matches[0].id})")
            pass
            
    print(f"Total semantic gaps candidates: {len(gaps)}")

if __name__ == "__main__":
    check_conflicts()
