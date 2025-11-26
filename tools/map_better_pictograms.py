import json

CATALOG_PATH = "nlp_backend/data/arasaac_catalog.jsonl"

# Definir términos específicos para cada categoría
CATEGORY_TERMS = {
    'mas usados': [
        'sí', 'no', 'quiero', 'necesito', 'gracias', 'por favor', 
        'hola', 'adiós', 'ayuda', 'bien', 'mal', 'más', 
        'agua', 'baño', 'comer', 'dormir'
    ],
    'personas': [
        'yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros',
        'papá', 'mamá', 'hermano', 'hermana', 'abuelo', 'abuela',
        'hijo', 'hija', 'bebé', 'niño', 'niña', 'hombre', 'mujer',
        'amigo', 'familia', 'persona'
    ],
    'saludos': [
        'hola', 'adiós', 'buenos días', 'buenas tardes', 'buenas noches',
        'hasta luego', 'bienvenido', 'gracias', 'de nada', 'por favor',
        'perdón', 'lo siento', 'felicidades', 'feliz cumpleaños'
    ],
    'necesidades': [
        'baño', 'aseo', 'agua', 'beber', 'sed',
        'comida', 'comer', 'hambre', 'desayuno', 'almuerzo', 'cena',
        'dormir', 'sueño', 'cansado', 'descansar',
        'ayuda', 'dolor', 'enfermo', 'medicina', 'médico',
        'frío', 'calor', 'vestir', 'ducha'
    ],
    'sentimientos': [
        'feliz', 'alegre', 'contento', 'triste', 'llorar',
        'enfadado', 'enojado', 'miedo', 'asustado', 'sorprendido',
        'cansado', 'aburrido', 'nervioso', 'preocupado',
        'enamorado', 'orgulloso', 'avergonzado', 'confundido'
    ],
    'lugares': [
        'casa', 'hogar', 'habitación', 'cocina', 'baño', 'salón',
        'colegio', 'escuela', 'clase', 'parque', 'jardín',
        'hospital', 'médico', 'tienda', 'supermercado', 'restaurante',
        'calle', 'ciudad', 'pueblo', 'playa', 'montaña'
    ],
    'acciones': [
        'comer', 'beber', 'dormir', 'despertar', 'levantarse',
        'ir', 'venir', 'andar', 'correr', 'saltar',
        'sentarse', 'estar de pie', 'jugar', 'trabajar', 'estudiar',
        'ver', 'mirar', 'escuchar', 'hablar', 'decir',
        'dar', 'coger', 'tomar', 'poner', 'abrir', 'cerrar',
        'leer', 'escribir', 'dibujar', 'pintar'
    ],
    'comida': [
        'agua', 'leche', 'zumo', 'café', 'té',
        'pan', 'galleta', 'tostada', 'cereales', 'pasta',
        'arroz', 'patata', 'ensalada', 'sopa', 'bocadillo',
        'manzana', 'plátano', 'naranja', 'fresa', 'uva', 'pera',
        'tomate', 'zanahoria', 'lechuga', 'cebolla',
        'carne', 'pollo', 'pescado', 'huevo', 'queso', 'yogur',
        'chocolate', 'helado', 'pastel', 'caramelo'
    ],
    'animales': [
        'perro', 'gato', 'pájaro', 'pez', 'conejo',
        'caballo', 'vaca', 'cerdo', 'oveja', 'gallina',
        'león', 'tigre', 'elefante', 'jirafa', 'mono',
        'oso', 'lobo', 'zorro', 'ratón', 'serpiente',
        'mariposa', 'abeja', 'hormiga', 'araña'
    ],
    'transporte': [
        'coche', 'carro', 'autobús', 'bus', 'tren',
        'avión', 'barco', 'bicicleta', 'moto', 'motocicleta',
        'taxi', 'ambulancia', 'camión', 'metro', 'tranvía',
        'helicóptero', 'cohete', 'patinete'
    ]
}

def find_pictograms():
    print("Cargando catálogo...")
    catalog = []
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                catalog.append(json.loads(line))
    
    print(f"Catálogo cargado: {len(catalog)} pictogramas\n")
    
    results = {}
    
    for category, terms in CATEGORY_TERMS.items():
        print(f"\n{'='*60}")
        print(f"Buscando para: {category.upper()}")
        print(f"{'='*60}")
        
        found_ids = []
        found_labels = []
        
        for term in terms:
            found = None
            
            # Búsqueda exacta primero
            for p in catalog:
                label = p.get('labels', {}).get('es', '')
                if label and label.lower() == term.lower():
                    found = p
                    break
            
            # Si no se encuentra, buscar que contenga el término
            if not found:
                for p in catalog:
                    label = p.get('labels', {}).get('es', '')
                    if label and term.lower() in label.lower():
                        found = p
                        break
            
            if found:
                found_ids.append(found['id'])
                found_labels.append(found['labels']['es'])
                print(f"  ✓ '{term}' -> ID {found['id']} ({found['labels']['es']})")
            else:
                print(f"  ✗ '{term}' -> NO ENCONTRADO")
        
        results[category] = {
            'ids': found_ids,
            'labels': found_labels,
            'count': len(found_ids)
        }
        
        print(f"\nTotal encontrados para {category}: {len(found_ids)}/{len(terms)}")
    
    # Generar código TypeScript
    print("\n\n" + "="*80)
    print("CÓDIGO TYPESCRIPT PARA CUSTOM_CATEGORY_DATA:")
    print("="*80 + "\n")
    
    print("export const CUSTOM_CATEGORY_DATA: Record<string, number[]> = {")
    for category, data in results.items():
        ids_str = ', '.join(str(id) for id in data['ids'])
        print(f"  '{category}': [{ids_str}],")
    print("};")
    
    # Resumen
    print("\n\n" + "="*80)
    print("RESUMEN:")
    print("="*80)
    for category, data in results.items():
        print(f"{category:20} -> {data['count']:3} pictogramas")

if __name__ == "__main__":
    find_pictograms()
