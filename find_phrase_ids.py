from nlp_backend.services.catalog import CatalogService
import os

catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))

# Find IDs for common expressions we want to add
terms_to_find = {
    # Greetings and common phrases
    'cómo estás': ['cómo', 'estar'],
    'qué tal': ['cómo', 'estar'],  # Map to same as "cómo estás"
    'tal': ['bien', 'bueno'],  # Fallback for "tal" alone
    
    # Verbs that need fixing
    'dormir': ['dormir'],
    'dormiste': ['dormir'],
    'durmiendo': ['dormir'],
    
    # Common colloquial expressions
    'de nada': ['de', 'nada'],
    'por favor': ['por favor'],
    'gracias': ['gracias'],
    'perdón': ['perdón'],
    'disculpa': ['perdón'],
    
    # Time expressions
    'qué hora es': ['qué', 'hora', 'ser'],
    'ahora': ['ahora'],
    'luego': ['luego'],
    'después': ['después'],
    
    # Common verbs
    'hacer': ['hacer'],
    'ir': ['ir'],
    'venir': ['venir'],
    'estar': ['estar'],
}

print("Buscando IDs para frases especiales:\n")

results_dict = {}
for phrase, terms in terms_to_find.items():
    print(f"\n'{phrase}' -> {terms}")
    ids = []
    for term in terms:
        results = catalog.find_by_term(term)
        if results:
            ids.append(str(results[0].id))
            print(f"  [OK] '{term}' -> ID {results[0].id}: '{results[0].labels.get('es', 'N/A')}'")
        else:
            print(f"  [NO] '{term}' -> NO ENCONTRADO")
    
    if ids:
        results_dict[phrase] = ids

print("\n\n=== JSON para frases_especiales.json ===\n")
import json
print(json.dumps(results_dict, indent=2, ensure_ascii=False))
