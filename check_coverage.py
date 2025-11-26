import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.services.catalog import CatalogService

def check_coverage():
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    common_words = [
        # Pronouns
        "yo", "tu", "tú", "el", "él", "ella", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas", "usted", "ustedes",
        "me", "te", "se", "nos", "os", "le", "les", "lo", "la", "los", "las",
        # Possessives
        "mi", "mis", "tu", "tus", "su", "sus", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro",
        # Prepositions
        "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", "en", "entre", "hacia", "hasta", "mediante", "para", "por", "según", "sin", "so", "sobre", "tras",
        # Conjunctions
        "y", "e", "ni", "o", "u", "pero", "mas", "sino", "porque", "pues", "si", "que",
        # Adverbs
        "sí", "no", "también", "tampoco", "muy", "mucho", "poco", "más", "menos", "aquí", "allí", "allá", "ahora", "luego", "después", "ayer", "hoy", "mañana", "siempre", "nunca",
        # Articles
        "un", "una", "unos", "unas",
        # Question words
        "qué", "quién", "cuál", "cómo", "cuándo", "dónde", "cuánto", "por qué"
    ]
    
    missing = []
    found = []
    
    print("\n--- Checking Coverage ---")
    for word in common_words:
        matches = catalog.find_by_term(word)
        if matches:
            found.append(f"{word} -> ID {matches[0].id} ({matches[0].labels.get('es', 'unknown')})")
        else:
            missing.append(word)
            
    print(f"\nFound {len(found)}/{len(common_words)} words.")
    
    print("\n--- MISSING WORDS ---")
    for word in missing:
        print(f"MISSING: {word}")
        # Try fuzzy to see if there's a close match we can map to
        fuzzy = catalog.find_fuzzy(word, threshold=90)
        if fuzzy:
            print(f"  -> Suggestion: {fuzzy[0].labels.get('es')} (ID {fuzzy[0].id})")
        else:
            print("  -> No close match found.")

if __name__ == "__main__":
    check_coverage()
