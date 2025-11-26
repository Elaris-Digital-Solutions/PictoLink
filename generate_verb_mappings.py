"""
Script to generate verb conjugation mappings for all verbs in the ARASAAC catalog.
This prevents spaCy lemmatization errors by creating explicit mappings.
"""
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService
import os
import json

# Initialize services
catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))
nlp = NLPService.get_instance()

# Common verb conjugations that spaCy often gets wrong
CONJUGATION_PATTERNS = {
    # Present tense
    'sientes': 'sentir',  # tú form often wrong
    'siento': 'sentir',
    'sienten': 'sentir',
    
    # Add more patterns as we discover them
}

# Find all verbs in catalog
print("Buscando verbos en el catálogo...")
verbs_in_catalog = []

# Iterate through catalog's pictograms dictionary
for picto_id, picto in catalog.pictograms.items():
    label = picto.labels.get('es', '').lower()
    # Check if it's a verb (infinitive ending in -ar, -er, -ir)
    if label.endswith(('ar', 'er', 'ir')) and len(label) > 3:
        verbs_in_catalog.append(label)

# Remove duplicates
verbs_in_catalog = sorted(list(set(verbs_in_catalog)))

print(f"\nEncontrados {len(verbs_in_catalog)} verbos en el catálogo")
print(f"Primeros 20: {verbs_in_catalog[:20]}")

# Test problematic conjugations
print("\n\n=== TESTING PROBLEMATIC CONJUGATIONS ===\n")

test_conjugations = [
    ('sientes', 'sentir'),
    ('dormiste', 'dormir'),
    ('estas', 'estar'),
    ('estoy', 'estar'),
]

problematic_mappings = {}

for conjugation, expected_infinitive in test_conjugations:
    # Process with spaCy
    tokens = nlp.process_text(conjugation)
    if tokens:
        spacy_lemma = tokens[0]['lemma']
        
        # Check if lemma exists in catalog
        lemma_in_catalog = bool(catalog.find_by_term(spacy_lemma))
        expected_in_catalog = bool(catalog.find_by_term(expected_infinitive))
        
        if spacy_lemma != expected_infinitive:
            print(f"❌ '{conjugation}':")
            print(f"   spaCy lemma: '{spacy_lemma}' (in catalog: {lemma_in_catalog})")
            print(f"   Expected: '{expected_infinitive}' (in catalog: {expected_in_catalog})")
            
            if expected_in_catalog:
                problematic_mappings[conjugation] = expected_infinitive
        else:
            print(f"✅ '{conjugation}' → '{spacy_lemma}' (correct)")

print(f"\n\n=== PRIORITY_MAP ADDITIONS NEEDED ===\n")
print(json.dumps(problematic_mappings, indent=2, ensure_ascii=False))
