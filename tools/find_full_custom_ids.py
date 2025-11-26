import json

CATALOG_PATH = "nlp_backend/data/arasaac_catalog.jsonl"

TARGETS = {
    'comida': ['agua', 'pan', 'manzana', 'plátano', 'leche', 'galleta', 'carne', 'pescado', 'huevo', 'sopa', 'zumo', 'fruta', 'verdura', 'desayuno', 'almuerzo', 'cena'],
    'animales': ['perro', 'gato', 'pájaro', 'pez', 'caballo', 'vaca', 'cerdo', 'león', 'elefante', 'jirafa', 'mono', 'tigre', 'conejo'],
    'transporte': ['coche', 'autobús', 'tren', 'avión', 'bicicleta', 'barco', 'taxi', 'moto', 'camión', 'ambulancia', 'metro'],
    'mas usados': ['sí', 'no', 'quiero', 'gracias', 'baño', 'agua', 'ayuda', 'hola', 'adiós', 'bien', 'mal', 'más', 'se acabó']
}

def find_full_ids():
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
                    'label': term
                })
                print(f"  Found '{term}': {found['id']}")
            else:
                print(f"  NOT FOUND: '{term}'")

    print("\n\n// TypeScript Data Additions:")
    for cat, items in results.items():
        ids = [str(item['id']) for item in items]
        print(f"  '{cat}': [{', '.join(ids)}],")

if __name__ == "__main__":
    find_full_ids()
