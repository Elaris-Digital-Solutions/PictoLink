from nlp_backend.services.catalog import CatalogService
import os

catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))

# Find IDs for "como te sientes" and variations
phrases_to_add = {
    'como te sientes': ['cómo', 'tú', 'sentir'],
    'como estas': ['cómo', 'estar'],
    'como estás': ['cómo', 'estar'],
    'hoy': ['hoy'],
}

print("Buscando IDs:\n")

results_dict = {}
for phrase, terms in phrases_to_add.items():
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

print("\n\n=== JSON ===\n")
import json
print(json.dumps(results_dict, indent=2, ensure_ascii=False))
