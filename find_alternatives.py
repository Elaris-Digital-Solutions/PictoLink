from nlp_backend.services.catalog import CatalogService
import os

catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))

# Find alternatives for missing terms
missing_terms = {
    'cuánto': ['cuanto', 'cantidad', 'mucho', 'número'],
    'las': ['la', 'ellas', 'los'],  # Try singular or other articles
    'necesidad': ['necesitar', 'necesario', 'ayuda'],
    'nuestra': ['nuestro', 'nosotros'],
    'odio': ['odiar', 'enojo', 'enfado', 'rabia'],
    'respiración': ['respirar', 'aire', 'pulmón'],
    'sabiduría': ['saber', 'sabio', 'inteligente', 'conocimiento'],
    'venta': ['vender', 'compra', 'tienda', 'comercio']
}

print("Buscando alternativas para términos faltantes:\n")

for missing, alternatives in missing_terms.items():
    print(f"\n{missing}:")
    for alt in alternatives:
        results = catalog.find_by_term(alt)
        if results:
            print(f"  [OK] {alt:20s} -> ID {results[0].id}: '{results[0].labels.get('es', 'N/A')}'")
        else:
            print(f"  [NO] {alt:20s} -> NO ENCONTRADO")
