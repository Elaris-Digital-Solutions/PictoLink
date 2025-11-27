import json
import os

META_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'embeddings', 'meta.jsonl')

CATEGORIES = {
    "personas": ["yo", "tú", "él", "ella", "nosotros", "ellos", "mamá", "papá", "abuelo", "abuela", "niño", "niña", "bebé", "hombre", "mujer", "amigo", "amiga", "familia", "profesor", "doctor"],
    "saludos": ["hola", "adiós", "buenos días", "buenas tardes", "buenas noches", "por favor", "gracias", "de nada", "perdón", "hasta luego", "bienvenido", "¿qué tal?", "beso", "abrazo"],
    "necesidades": ["baño", "inodoro", "ducha", "lavarse", "comer", "beber", "dormir", "ayuda", "dolor", "medicinas", "descansar", "vestirse", "desvestirse", "pañal", "sed", "hambre"],
    "sentimientos": ["feliz", "triste", "enfadado", "miedo", "sorpresa", "cansado", "aburrido", "nervioso", "contento", "llorar", "reír", "amor", "gustar", "odiar", "calma"],
    "lugares": ["casa", "colegio", "parque", "hospital", "calle", "tienda", "supermercado", "cocina", "habitación", "baño", "salón", "jardín", "restaurante", "playa", "piscina"],
    "acciones": ["ir", "venir", "querer", "tener", "estar", "ser", "hacer", "ver", "oír", "hablar", "jugar", "trabajar", "estudiar", "comprar", "esperar", "parar", "ayudar", "buscar"],
    "comida": ["agua", "pan", "leche", "fruta", "manzana", "plátano", "carne", "pescado", "pollo", "huevo", "arroz", "pasta", "galleta", "zumo", "desayuno", "comida", "cena"],
    "animales": ["perro", "gato", "pájaro", "pez", "caballo", "vaca", "cerdo", "oveja", "gallina", "león", "elefante", "jirafa", "mono", "oso", "conejo"],
    "transporte": ["coche", "autobús", "tren", "avión", "barco", "bicicleta", "moto", "taxi", "ambulancia", "camión", "furgoneta", "metro", "silla de ruedas", "andando"]
}

def load_catalog():
    catalog = {}
    with open(META_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                if 'labels' in entry and 'es' in entry['labels']:
                    label = entry['labels']['es'].lower()
                    # Store shortest ID for each label to prefer simple pictograms? 
                    # Or store all and filter later. Let's store the first one found or prefer lower IDs.
                    if label not in catalog:
                        catalog[label] = []
                    catalog[label].append(entry)
            except:
                pass
    return catalog

def find_best_match(term, catalog):
    term = term.lower()
    if term in catalog:
        # Sort by ID length (heuristic: shorter IDs are often older/core?) or just take first
        # Actually, let's look for exact match first
        matches = catalog[term]
        # Prefer matches that don't have complex descriptions if possible, but we only have labels here.
        # Just return the first one for now.
        return matches[0]['id']
    
    # Try synonyms? (Not implemented in this simple script, but catalog has them)
    return None

def main():
    catalog = load_catalog()
    results = {}
    
    for category, terms in CATEGORIES.items():
        results[category] = []
        print(f"Processing {category}...")
        for term in terms:
            pid = find_best_match(term, catalog)
            if pid:
                results[category].append(pid)
            else:
                print(f"  Warning: No match found for '{term}'")
    
    with open('category_ids.txt', 'w', encoding='utf-8') as f:
        for cat, ids in results.items():
            f.write(f"'{cat}': {json.dumps(ids)},\n")
    print("Results written to category_ids.txt")

if __name__ == "__main__":
    main()
