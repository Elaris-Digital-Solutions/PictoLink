"""
Automatic verb conjugation generator for PRIORITY_MAP
Generates conjugations for all verbs in ARASAAC catalog and identifies spaCy lemmatization errors
"""
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService
import os
import json
from verbecc.conjugator import Conjugator
# Initialize services
catalog = CatalogService.get_instance()
catalog.load_data(os.path.join('nlp_backend', 'data', 'arasaac_catalog.jsonl'))
nlp = NLPService.get_instance()
cg = Conjugator(lang='es')

print("Extrayendo verbos del catalogo...")
verbs_in_catalog = []
for picto_id, picto in catalog.pictograms.items():
    label = picto.labels.get('es', '').lower()
    if label.endswith(('ar', 'er', 'ir')) and len(label) > 3:
        verbs_in_catalog.append(label)

verbs_in_catalog = sorted(list(set(verbs_in_catalog)))
print(f"Encontrados {len(verbs_in_catalog)} verbos\n")

# Generate conjugations for common tenses
print("Generando conjugaciones para los primeros 50 verbos...\n")

problematic_conjugations = {}
total_conjugations_tested = 0
errors_found = 0

for verb in verbs_in_catalog[:50]:  # Test first 50
    try:
        # Conjugate verb
        conjugated = cg.conjugate(verb)
        
        # Extract common forms that users might type
        forms_to_test = []
        
        # Present tense (presente indicativo)
        if 'indicativo' in conjugated and 'presente' in conjugated['indicativo']:
            presente = conjugated['indicativo']['presente']
            forms_to_test.extend([
                ('yo', presente.get('1s', '')),
                ('tu', presente.get('2s', '')),
                ('el', presente.get('3s', '')),
                ('nosotros', presente.get('1p', '')),
                ('ellos', presente.get('3p', ''))
            ])
        
        # Preterite (preterito)
        if 'indicativo' in conjugated and 'pretérito' in conjugated['indicativo']:
            preterito = conjugated['indicativo']['pretérito']
            forms_to_test.extend([
                ('yo_pret', preterito.get('1s', '')),
                ('tu_pret', preterito.get('2s', '')),
            ])
        
        # Gerund
        if 'gerundio' in conjugated:
            forms_to_test.append(('gerundio', conjugated['gerundio']))
        
        # Test each conjugation
        for person, conjugation in forms_to_test:
            if not conjugation or conjugation == verb:
                continue
                
            total_conjugations_tested += 1
            
            # Test with spaCy
            tokens = nlp.process_text(conjugation)
            if tokens:
                spacy_lemma = tokens[0]['lemma']
                
                # Check if spaCy gets it wrong
                if spacy_lemma != verb:
                    # Verify the verb exists in catalog
                    if catalog.find_by_term(verb):
                        errors_found += 1
                        problematic_conjugations[conjugation] = verb
                        print(f"[ERROR] '{conjugation}' -> spaCy: '{spacy_lemma}' | Correcto: '{verb}'")
    
    except Exception as e:
        print(f"[SKIP] Error conjugando '{verb}': {e}")
        continue

print(f"\n\n=== RESUMEN ===")
print(f"Verbos probados: 50")
print(f"Conjugaciones testeadas: {total_conjugations_tested}")
print(f"Errores encontrados: {errors_found} ({errors_found/total_conjugations_tested*100:.1f}%)")
print(f"\n=== PRIMERAS 20 CONJUGACIONES PROBLEMATICAS ===\n")

for i, (conj, verb) in enumerate(list(problematic_conjugations.items())[:20], 1):
    print(f"{i:2d}. '{conj}' -> '{verb}'")

# Save to file
output_file = 'verb_conjugation_mappings.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(problematic_conjugations, f, indent=2, ensure_ascii=False)

print(f"\n\nGuardado {len(problematic_conjugations)} mapeos en '{output_file}'")
print(f"\nPara agregar a PRIORITY_MAP en translation.py")
