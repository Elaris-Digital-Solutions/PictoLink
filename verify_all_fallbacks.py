"""
Script to verify all FALLBACK_MAP entries exist in the ARASAAC catalog
"""
from nlp_backend.services.catalog import CatalogService
import os

catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))

# All terms from FALLBACK_MAP (target values)
fallback_targets = {
    # Possessives
    'mío', 'mis', 'tú', 'su', 'nuestro', 'nuestra',
    
    # Pronouns
    'yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros', 'ellos',
    
    # Verbs
    'gustar',  # Used for 'encantar'
    
    # Question words
    'quién', 'cómo', 'cuándo', 'dónde', 'cuánto', 'por qué',
    
    # Adverbs/Conjunctions
    'sí', 'no', 'y', 'o', 'pero', 'mucho', 'más',
    'a', 'de', 'en', 'con', 'por', 'para',
    
    # Semantic mappings
    'educación', 'respiración', 'andar', 'pintura', 'limpieza',
    'venta', 'necesidad', 'odio', 'sentimiento', 'pensamiento', 'sabiduría',
}

# Also check PRIORITY_MAP targets
priority_targets = {
    'viaje', 'compra', 'masturbación', 'qué',
    'un', 'una', 'el', 'la', 'los', 'las',
    'gustar', 'estar'
}

all_targets = fallback_targets | priority_targets

print("="*80)
print("VERIFICACIÓN DE TÉRMINOS EN CATÁLOGO")
print("="*80)
print(f"\nTotal de términos únicos a verificar: {len(all_targets)}\n")

found = []
not_found = []

for term in sorted(all_targets):
    results = catalog.find_by_term(term)
    if results:
        found.append((term, results[0].id, results[0].labels.get('es', 'N/A')))
        status = "[OK]"
    else:
        not_found.append(term)
        status = "[NO]"
    
    print(f"{status} {term:20s}: {len(results):2d} resultados", end="")
    if results:
        print(f" -> ID {results[0].id}: '{results[0].labels.get('es', 'N/A')}'")
    else:
        print()

print("\n" + "="*80)
print("RESUMEN")
print("="*80)
print(f"[OK] Encontrados: {len(found)}/{len(all_targets)} ({len(found)/len(all_targets)*100:.1f}%)")
print(f"[NO] No encontrados: {len(not_found)}/{len(all_targets)} ({len(not_found)/len(all_targets)*100:.1f}%)")

if not_found:
    print("\n" + "="*80)
    print("TÉRMINOS NO ENCONTRADOS (REQUIEREN ATENCIÓN)")
    print("="*80)
    for term in sorted(not_found):
        print(f"  - {term}")
    print("\nEstos términos necesitan ser reemplazados por alternativas que SÍ existan en el catálogo.")
