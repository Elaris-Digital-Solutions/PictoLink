import json

CATALOG_PATH = "nlp_backend/data/arasaac_catalog.jsonl"

# Cargar catálogo
print("Cargando catálogo...")
catalog = []
with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            catalog.append(json.loads(line))

print(f"Total: {len(catalog)} pictogramas\n")

# Crear índice por etiqueta
index = {}
for p in catalog:
    label = p.get('labels', {}).get('es', '')
    if label:
        index[label.lower()] = p['id']

# Definir términos para cada categoría
CATEGORIES = {
    'mas usados': ['sí', 'no', 'querer', 'necesitar', 'gracias', 'por favor', 'hola', 'adiós', 'ayuda', 'bien', 'mal', 'más', 'agua', 'baño', 'comer', 'dormir'],
    'personas': ['yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros', 'papá', 'mamá', 'hermano', 'hermana', 'abuelo', 'abuela', 'hijo', 'hija', 'bebé', 'niño', 'niña', 'hombre', 'mujer', 'amigo', 'familia', 'persona'],
    'saludos': ['hola', 'adiós', 'buenos días', 'buenas tardes', 'buenas noches', 'hasta luego', 'bienvenido', 'gracias', 'de nada', 'por favor', 'perdón', 'lo siento'],
    'necesidades': ['baño', 'aseo', 'agua', 'beber', 'sed', 'comida', 'comer', 'hambre', 'desayuno', 'almuerzo', 'cena', 'dormir', 'sueño', 'cansado', 'ayuda', 'dolor', 'enfermo', 'medicina', 'médico', 'frío', 'calor'],
    'sentimientos': ['feliz', 'alegre', 'contento', 'triste', 'llorar', 'enfadado', 'enojado', 'miedo', 'asustado', 'sorprendido', 'cansado', 'aburrido', 'nervioso', 'preocupado', 'enamorado', 'orgulloso'],
    'lugares': ['casa', 'hogar', 'habitación', 'cocina', 'baño', 'salón', 'colegio', 'escuela', 'clase', 'parque', 'jardín', 'hospital', 'tienda', 'supermercado', 'restaurante', 'calle', 'ciudad'],
    'acciones': ['comer', 'beber', 'dormir', 'ir', 'venir', 'andar', 'correr', 'saltar', 'sentarse', 'jugar', 'trabajar', 'estudiar', 'ver', 'mirar', 'escuchar', 'hablar', 'dar', 'coger', 'tomar', 'poner', 'abrir', 'cerrar', 'leer', 'escribir'],
    'comida': ['agua', 'leche', 'zumo', 'pan', 'galleta', 'pasta', 'arroz', 'patata', 'ensalada', 'sopa', 'manzana', 'plátano', 'naranja', 'fresa', 'tomate', 'zanahoria', 'carne', 'pollo', 'pescado', 'huevo', 'queso', 'yogur', 'chocolate', 'helado'],
    'animales': ['perro', 'gato', 'pájaro', 'pez', 'conejo', 'caballo', 'vaca', 'cerdo', 'oveja', 'gallina', 'león', 'tigre', 'elefante', 'jirafa', 'mono', 'oso', 'lobo', 'zorro', 'ratón'],
    'transporte': ['coche', 'autobús', 'tren', 'avión', 'barco', 'bicicleta', 'moto', 'taxi', 'ambulancia', 'camión', 'metro']
}

results = {}

for cat_name, terms in CATEGORIES.items():
    print(f"\n{'='*60}")
    print(f"Categoría: {cat_name.upper()}")
    print(f"{'='*60}")
    
    ids = []
    found_terms = []
    
    for term in terms:
        if term.lower() in index:
            pid = index[term.lower()]
            ids.append(pid)
            found_terms.append(term)
            print(f"  ✓ {term:20} -> ID {pid}")
        else:
            # Buscar parcial
            found = False
            for label, pid in index.items():
                if term.lower() in label:
                    ids.append(pid)
                    found_terms.append(f"{term} ({label})")
                    print(f"  ~ {term:20} -> ID {pid} (encontrado como '{label}')")
                    found = True
                    break
            if not found:
                print(f"  ✗ {term:20} -> NO ENCONTRADO")
    
    results[cat_name] = ids
    print(f"\nTotal: {len(ids)}/{len(terms)} encontrados")

# Generar código TypeScript
print("\n\n" + "="*80)
print("CÓDIGO TYPESCRIPT:")
print("="*80 + "\n")

print("export const CUSTOM_CATEGORY_DATA: Record<string, number[]> = {")
for cat_name, ids in results.items():
    if ids:
        ids_str = ', '.join(str(id) for id in ids)
        print(f"  '{cat_name}': [{ids_str}],")
print("};")
