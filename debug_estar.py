from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService
import os

# Load services
catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))
nlp = NLPService.get_instance()

# Test 1: Check if 'estar' exists in catalog
print("=== TEST 1: Búsqueda de 'estar' en catálogo ===")
results = catalog.find_by_term('estar')
print(f"Resultados para 'estar': {len(results)}")
for r in results[:3]:
    print(f"  - ID {r.id}: {r.labels.get('es', 'N/A')}")

# Test 2: Check lemmatization of 'estas'
print("\n=== TEST 2: Lemmatización de 'estas' ===")
tokens = nlp.process_text('como estas')
for t in tokens:
    print(f"  text='{t['text']}', lemma='{t['lemma']}', pos={t['pos']}")

# Test 3: Check what 'este' returns
print("\n=== TEST 3: Búsqueda de 'este' en catálogo ===")
results_este = catalog.find_by_term('este')
print(f"Resultados para 'este': {len(results_este)}")
for r in results_este[:3]:
    print(f"  - ID {r.id}: {r.labels.get('es', 'N/A')}")

# Test 4: Full mapping process for "como estas"
print("\n=== TEST 4: Mapeo completo de 'como estas' ===")
import asyncio
from nlp_backend.routers.translation import text_to_pictos, TextRequest

result = asyncio.run(text_to_pictos(TextRequest(text='como estas')))
print(f"Pictogramas: {[p.labels['es'] for p in result['pictograms']]}")
