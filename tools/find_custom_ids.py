import json

CATALOG_PATH = "nlp_backend/data/arasaac_catalog.jsonl"

TARGETS = {
    'personas': ['yo', 'tú', 'nosotros', 'papá', 'mamá', 'abuelo', 'abuela', 'hombre', 'mujer', 'niño', 'niña'],
    'saludos': ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'adiós', 'por favor', 'gracias', 'de nada'],
    'necesidades': ['baño', 'aseo', 'agua', 'beber', 'comida', 'comer', 'hambre', 'sed', 'sueño', 'dormir', 'ayuda', 'dolor', 'medicina', 'pastilla'],
    'sentimientos': ['feliz', 'triste', 'enfadado', 'miedo', 'sorpresa', 'cansado', 'contento', 'nervioso'],
    'lugares': ['casa', 'colegio', 'parque', 'calle', 'hospital', 'tienda', 'supermercado', 'cocina', 'baño', 'habitación'],
    'acciones': ['querer', 'tener', 'ir', 'estar', 'ver', 'jugar', 'coger', 'dar', 'poner', 'hacer']
}

def find_specific_ids():
    print("Loading catalog...")
    catalog = []
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                catalog.append(json.loads(line))
    
    results = {cat: [] for cat in TARGETS}
    
    for cat, terms in TARGETS.items():
        print(f"\nSearching for {cat}...")
        for term in terms:
            found = None
            # Exact match first
            for p in catalog:
                if 'es' in p.get('labels', {}) and p['labels']['es']:
                    if p['labels']['es'].lower() == term.lower():
                        found = p
                        break
            
            # If not found, try contains
            if not found:
                for p in catalog:
                    if 'es' in p.get('labels', {}) and p['labels']['es']:
                        if term.lower() in p['labels']['es'].lower():
                            found = p
                            break
            
            if found:
                results[cat].append({
                    'id': found['id'],
                    'label': term, # Use our term as label preference
                    'original_label': found['labels']['es']
                })
                print(f"  Found '{term}': {found['id']}")
            else:
                print(f"  NOT FOUND: '{term}'")

    print("\n\n// TypeScript Data:")
    print("export const CUSTOM_CATEGORY_DATA: Record<string, number[]> = {")
    for cat, items in results.items():
        ids = [str(item['id']) for item in items]
        print(f"  '{cat}': [{', '.join(ids)}],")
    print("};")

if __name__ == "__main__":
    find_specific_ids()
