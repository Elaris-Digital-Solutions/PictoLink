import json

CATALOG_PATH = "nlp_backend/data/arasaac_catalog.jsonl"

CATEGORIES = [
    'animal', 'food', 'person', 'family', 'emotion', 'action', 'object',
    'place', 'transport', 'nature', 'leisure', 'work', 'health', 'communication',
    'clothes', 'building facility', 'gastronomy'
]

# Manual overrides for better icons if simple search fails or is generic
# We will try to find these specific terms first
PREFERRED_TERMS = {
    'animal': 'perro',
    'food': 'comida',
    'person': 'persona',
    'family': 'familia',
    'emotion': 'emoción',
    'action': 'verbo', # Abstract, maybe 'hacer'?
    'object': 'cosa',
    'place': 'lugar',
    'transport': 'transporte',
    'nature': 'naturaleza',
    'leisure': 'ocio',
    'work': 'trabajo',
    'health': 'salud',
    'communication': 'comunicación',
    'clothes': 'ropa',
    'building facility': 'edificio',
    'gastronomy': 'restaurante'
}

def find_icons():
    print("Loading catalog...")
    catalog = []
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                catalog.append(json.loads(line))
    
    results = {}
    
    for cat in CATEGORIES:
        term = PREFERRED_TERMS.get(cat, cat)
        found = None
        
        # Try exact match first
        for p in catalog:
            if 'es' in p.get('labels', {}) and p['labels']['es']:
                # labels['es'] is a string, not a list of keywords
                if term.lower() == p['labels']['es'].lower():
                    found = p
                    break
        
        # If not found, try contains
        if not found:
            for p in catalog:
                if 'es' in p.get('labels', {}) and p['labels']['es']:
                    if term.lower() in p['labels']['es'].lower():
                        found = p
                        break
                    if found: break
        
        if found:
            results[cat] = {
                'id': found['id'],
                'term': term,
                'image': found['image_urls']['png_color']
            }
            print(f"Found for {cat} ({term}): {found['id']}")
        else:
            print(f"NOT FOUND for {cat} ({term})")

    print("\nMapping for TypeScript:")
    print("export const CATEGORY_ICONS: Record<string, number> = {")
    for cat, data in results.items():
        print(f"  '{cat}': {data['id']}, // {data['term']}")
    print("};")

if __name__ == "__main__":
    find_icons()
