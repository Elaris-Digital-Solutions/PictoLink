from nlp_backend.services.catalog import CatalogService
import os

catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))

# Check if these terms exist in catalog
terms_to_check = ['le', 'les', 'el', 'la', 'un', 'una', 'encantar', 'encantado']

for term in terms_to_check:
    results = catalog.find_by_term(term)
    print(f"{term:15s}: {len(results)} resultados", end="")
    if results:
        print(f" → ID {results[0].id}: '{results[0].labels.get('es', 'N/A')}'")
    else:
        print(" → NO ENCONTRADO")
