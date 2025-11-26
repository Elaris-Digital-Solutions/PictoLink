import json

# Cargar catálogo
with open('nlp_backend/data/arasaac_catalog.jsonl', 'r', encoding='utf-8') as f:
    catalog = [json.loads(line) for line in f if line.strip()]

# Crear índice label -> id
label_to_id = {}
for p in catalog:
    label = p.get('labels', {}).get('es', '')
    if label:
        label_to_id[label.lower()] = p['id']

# Términos para cada categoría
categories = {
    'mas usados': ['sí', 'no', 'querer', 'gracias', 'hola', 'adiós', 'ayuda', 'agua', 'baño', 'comer', 'más'],
    'personas': ['yo', 'tú', 'papá', 'mamá', 'abuelo', 'abuela', 'hermano', 'hermana', 'niño', 'niña', 'hombre', 'mujer', 'familia'],
    'saludos': ['hola', 'adiós', 'buenos días', 'buenas tardes', 'buenas noches', 'gracias', 'por favor'],
    'necesidades': ['baño', 'agua', 'comer', 'beber', 'dormir', 'ayuda', 'dolor', 'frío', 'calor'],
    'sentimientos': ['feliz', 'triste', 'enfadado', 'miedo', 'cansado', 'contento'],
    'lugares': ['casa', 'colegio', 'parque', 'hospital', 'tienda', 'calle'],
    'acciones': ['comer', 'beber', 'dormir', 'ir', 'jugar', 'ver', 'hablar', 'dar'],
    'comida': ['agua', 'pan', 'leche', 'manzana', 'plátano', 'carne', 'pescado', 'huevo'],
    'animales': ['perro', 'gato', 'pájaro', 'caballo', 'vaca', 'león', 'elefante'],
    'transporte': ['coche', 'autobús', 'tren', 'avión', 'barco', 'bicicleta']
}

# Buscar IDs
results = {}
for cat_name, terms in categories.items():
    ids = []
    for term in terms:
        if term.lower() in label_to_id:
            ids.append(label_to_id[term.lower()])
    results[cat_name] = ids

# Imprimir resultado
print("export const CUSTOM_CATEGORY_DATA: Record<string, number[]> = {")
for cat_name, ids in results.items():
    print(f"  '{cat_name}': [{', '.join(map(str, ids))}],")
print("};")

# Imprimir iconos
print("\nexport const CATEGORY_ICONS: Record<string, number> = {")
for cat_name, ids in results.items():
    if ids:
        print(f"  '{cat_name}': {ids[0]},")
print("};")
