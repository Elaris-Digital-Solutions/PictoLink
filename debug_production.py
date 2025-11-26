import asyncio
from nlp_backend.routers.translation import text_to_pictos, TextRequest
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService
import os

# Initialize services
catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))
nlp = NLPService.get_instance()

# Test the problematic phrases
test_phrases = [
    "Quiero muchisimo un asado",
    "a mi amigo le encanta la verga",
    "a mi amigo le encanta el pene"
]

print("=== TESTING PROBLEMATIC PHRASES ===\n")

for phrase in test_phrases:
    print(f"Input: '{phrase}'")
    
    # Get tokens
    tokens = nlp.process_text(phrase)
    print("Tokens:")
    for t in tokens:
        print(f"  {t['text']:15s} → lemma={t['lemma']:15s} pos={t['pos']}")
    
    # Get mapping
    result = asyncio.run(text_to_pictos(TextRequest(text=phrase)))
    labels = [p.labels['es'] for p in result['pictograms']]
    print(f"Mapped to: {', '.join(labels)}")
    print()
