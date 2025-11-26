import json

CATALOG_PATH = "nlp_backend/data/arasaac_catalog.jsonl"

# Términos específicos para cada categoría
CATEGORIES = {
    'mas usados': ['sí', 'no', 'querer', 'necesitar', 'gracias', 'por favor', 'hola', 'adiós', 'ayuda', 'bien', 'mal', 'más', 'agua', 'baño', 'comer', 'dormir'],
    'personas': ['yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros', 'papá', 'mamá', 'hermano', 'hermana', 'abuelo', 'abuela', 'hijo', 'hija', 'bebé', 'niño', 'niña', 'hombre', 'mujer', 'amigo', 'familia', 'persona'],
    'saludos': ['hola', 'adiós', 'buenos días', 'buenas tardes', 'buenas noches', 'hasta luego', 'bienvenido', 'gracias', 'de nada', 'por favor', 'perdón', 'lo siento', 'felicidades', 'feliz cumpleaños'],
    'necesidades': ['baño', 'aseo', 'agua', 'beber', 'sed', 'comida', 'comer', 'hambre', 'desayuno', 'almuerzo', 'cena', 'dormir', 'sueño', 'cansado', 'descansar', 'ayuda', 'dolor', 'enfermo', 'medicina', 'médico', 'frío', 'calor', 'vestir', 'ducha'],
    'sentimientos': ['feliz', 'alegre', 'contento', 'triste', 'llorar', 'enfadado', 'enojado', 'miedo', 'asustado', 'sorprendido', 'cansado', 'aburrido', 'nervioso', 'preocupado', 'enamorado', 'orgulloso', 'avergonzado', 'confundido'],
    'lugares': ['casa', 'hogar', 'habitación', 'cocina', 'baño', 'salón', 'colegio', 'escuela', 'clase', 'parque', 'jardín', 'hospital', 'médico', 'tienda', 'supermercado', 'restaurante', 'calle', 'ciudad', 'pueblo', 'playa', 'montaña'],
    'acciones': ['comer', 'beber', 'dormir', 'despertar', 'levantarse', 'ir', 'venir', 'andar', 'correr', 'saltar', 'sentarse', 'estar de pie', 'jugar', 'trabajar', 'estudiar', 'ver', 'mirar', 'escuchar', 'hablar', 'decir', 'dar', 'coger', 'tomar', 'poner', 'abrir', 'cerrar', 'leer', 'escribir', 'dibujar', 'pintar'],
    'comida': ['agua', 'leche', 'zumo', 'café', 'té', 'pan', 'galleta', 'tostada', 'cereales', 'pasta', 'arroz', 'patata', 'ensalada', 'sopa', 'bocadillo', 'manzana', 'plátano', 'naranja', 'fresa', 'uva', 'pera', 'tomate', 'zanahoria', 'lechuga', 'cebolla', 'carne', 'pollo', 'pescado', 'huevo', 'queso', 'yogur', 'chocolate', 'helado', 'pastel', 'caramelo'],
    'animales': ['perro', 'gato', 'pájaro', 'pez', 'conejo', 'caballo', 'vaca', 'cerdo', 'oveja', 'gallina', 'león', 'tigre', 'elefante', 'jirafa', 'mono', 'oso', 'lobo', 'zorro', 'ratón', 'serpiente', 'mariposa', 'abeja', 'hormiga', 'araña'],
    'transporte': ['coche', 'carro', 'autobús', 'bus', 'tren', 'avión', 'barco', 'bicicleta', 'moto', 'motocicleta', 'taxi', 'ambulancia', 'camión', 'metro', 'tranvía', 'helicóptero', 'cohete', 'patinete']
}

print("Cargando catálogo...")
catalog = []
with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            catalog.append(json.loads(line))

print(f"Catálogo cargado: {len(catalog)} pictogramas\n")

results = {}

for cat_name, terms in CATEGORIES.items():
    ids = []
    for term in terms:
        found = None
        # Búsqueda exacta
        for p in catalog:
            label = p.get('labels', {}).get('es', '')
            if label and label.lower() == term.lower():
                found = p
                break
        
        # Búsqueda parcial
        if not found:
            for p in catalog:
                label = p.get('labels', {}).get('es', '')
                if label and term.lower() in label.lower():
                    found = p
                    break
        
        if found:
            ids.append(found['id'])
    
    results[cat_name] = ids

# Generar código TypeScript
print("export const CUSTOM_CATEGORY_DATA: Record<string, number[]> = {")
for cat_name, ids in results.items():
    ids_str = ', '.join(str(id) for id in ids)
    print(f"  '{cat_name}': [{ids_str}],")
print("};")
