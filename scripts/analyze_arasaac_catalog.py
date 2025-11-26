"""
Script para analizar el catálogo ARASAAC y generar mapeos de categorías
basados en las necesidades del usuario final.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path
import re

# Definición de categorías y palabras clave
CATEGORY_KEYWORDS = {
    'mas_usados': {
        'keywords': ['yo', 'tú', 'hola', 'adiós', 'sí', 'no', 'querer', 'necesitar', 'ayuda', 'gracias'],
        'priority': 1,
        'limit': 25
    },
    'necesidades_basicas': {
        'keywords': ['hambre', 'sed', 'dolor', 'ayuda', 'cansado', 'sueño', 'dormir', 'descansar'],
        'priority': 1,
        'limit': 20
    },
    'baño': {
        'keywords': ['baño', 'inodoro', 'váter', 'pañal', 'lavarse', 'ducha', 'jabón', 'toalla', 'papel'],
        'priority': 1,
        'limit': 15
    },
    'emociones': {
        'keywords': ['feliz', 'triste', 'enojado', 'enfadado', 'asustado', 'sorprendido', 'contento', 'alegre', 'llorar', 'reír'],
        'priority': 1,
        'limit': 25
    },
    'saludos': {
        'keywords': ['hola', 'adiós', 'buenos días', 'buenas tardes', 'buenas noches', 'gracias', 'por favor', 'perdón'],
        'priority': 1,
        'limit': 12
    },
    'familia': {
        'keywords': ['mamá', 'papá', 'madre', 'padre', 'hermano', 'hermana', 'abuelo', 'abuela', 'tío', 'tía', 'primo', 'bebé'],
        'priority': 2,
        'limit': 20
    },
    'personas': {
        'keywords': ['niño', 'niña', 'bebé', 'doctor', 'médico', 'maestro', 'profesor', 'amigo', 'persona', 'hombre', 'mujer'],
        'priority': 2,
        'limit': 25
    },
    'comida': {
        'keywords': ['comer', 'beber', 'agua', 'pan', 'leche', 'fruta', 'manzana', 'plátano', 'carne', 'pollo', 'arroz', 'pasta', 'sopa', 'jugo', 'café'],
        'priority': 1,
        'limit': 40
    },
    'lugares': {
        'keywords': ['casa', 'escuela', 'colegio', 'parque', 'hospital', 'tienda', 'supermercado', 'iglesia', 'playa', 'ciudad'],
        'priority': 2,
        'limit': 25
    },
    'verbos': {
        'keywords': ['ir', 'venir', 'hacer', 'tener', 'querer', 'poder', 'comer', 'beber', 'dormir', 'jugar', 'ver', 'oír', 'hablar', 'caminar', 'correr'],
        'priority': 1,
        'limit': 50
    },
    'deportes': {
        'keywords': ['fútbol', 'baloncesto', 'nadar', 'natación', 'correr', 'jugar', 'pelota', 'balón', 'deporte', 'gimnasia'],
        'priority': 3,
        'limit': 20
    },
    'animales': {
        'keywords': ['perro', 'gato', 'pájaro', 'pez', 'caballo', 'vaca', 'cerdo', 'oveja', 'conejo', 'ratón', 'león', 'elefante'],
        'priority': 3,
        'limit': 30
    },
    'pronombres': {
        'keywords': ['yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros', 'ellos', 'ellas', 'mi', 'tu', 'su'],
        'priority': 2,
        'limit': 10
    },
    'tiempo': {
        'keywords': ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo', 'hoy', 'mañana', 'ayer', 'día', 'noche', 'tarde', 'hora'],
        'priority': 2,
        'limit': 20
    },
    'transporte': {
        'keywords': ['coche', 'carro', 'auto', 'autobús', 'bus', 'bicicleta', 'tren', 'avión', 'barco', 'moto'],
        'priority': 3,
        'limit': 15
    }
}

# IDs específicos conocidos (de la configuración actual)
KNOWN_IDS = {
    'mas_usados': [5584, 5596, 5441, 6653, 34567, 34568, 2275, 32464, 39122, 28669, 32301],
    'personas': [31807, 6997, 38961, 38962, 38963, 38964, 38965, 38966, 38968, 38969, 38970, 38971, 38972],
    'saludos': [34567, 34568, 6554, 6556, 6555, 6653, 6724],
    'necesidades_basicas': [39122, 32464, 28669, 32465, 32466, 2275, 32467, 32468, 32469],
    'emociones': [35545, 35546, 35547, 35548, 35549, 35550],
    'lugares': [6964, 6965, 6966, 6967, 6968, 6969],
    'verbos': [28669, 32465, 32466, 7004, 7007, 7006, 2345],
    'comida': [32464, 32470, 32471, 32472, 32473, 32474, 32475, 32476],
    'animales': [38967, 38968, 38969, 38970, 38971, 38972, 38973],
    'transporte': [6981, 6982, 6983, 6984, 6985, 6986],
    'baño': [2275],  # Baño/inodoro
}


def normalize_text(text):
    """Normaliza texto para comparación"""
    if not text:
        return ""
    text = text.lower().strip()
    # Remover acentos
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', 'ü': 'u'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def matches_keywords(label, keywords):
    """Verifica si una etiqueta coincide con alguna palabra clave"""
    normalized_label = normalize_text(label)
    for keyword in keywords:
        normalized_keyword = normalize_text(keyword)
        if normalized_keyword in normalized_label or normalized_label in normalized_keyword:
            return True
    return False


def analyze_catalog(catalog_path):
    """
    Analiza el catálogo ARASAAC completo
    """
    print(f"📊 Analizando catálogo: {catalog_path}")
    
    # Estadísticas generales
    total_pictograms = 0
    categories_native = Counter()
    
    # Mapeo a nuevas categorías
    category_mappings = defaultdict(list)
    
    # Leer catálogo línea por línea
    with open(catalog_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
                
            try:
                picto = json.loads(line)
                total_pictograms += 1
                
                picto_id = picto.get('id')
                label_es = picto.get('labels', {}).get('es', '')
                
                if not label_es:
                    continue
                
                # Analizar categorías nativas de ARASAAC
                native_cats = picto.get('sources', {}).get('es', {}).get('raw', {}).get('categories', [])
                for cat in native_cats:
                    categories_native[cat] += 1
                
                # Mapear a nuevas categorías basadas en keywords
                for category, config in CATEGORY_KEYWORDS.items():
                    keywords = config['keywords']
                    limit = config['limit']
                    
                    # Verificar si ya tenemos suficientes pictogramas
                    if len(category_mappings[category]) >= limit:
                        continue
                    
                    # Primero agregar IDs conocidos
                    if picto_id in KNOWN_IDS.get(category, []):
                        if picto_id not in [p['id'] for p in category_mappings[category]]:
                            category_mappings[category].append({
                                'id': picto_id,
                                'label': label_es,
                                'source': 'known_id'
                            })
                        continue
                    
                    # Luego buscar por keywords
                    if matches_keywords(label_es, keywords):
                        if picto_id not in [p['id'] for p in category_mappings[category]]:
                            category_mappings[category].append({
                                'id': picto_id,
                                'label': label_es,
                                'source': 'keyword_match'
                            })
                
                # Progreso cada 1000 pictogramas
                if line_num % 1000 == 0:
                    print(f"  Procesados: {line_num} pictogramas...")
                    
            except json.JSONDecodeError as e:
                print(f"⚠️  Error en línea {line_num}: {e}")
                continue
    
    print(f"\n✅ Análisis completado!")
    print(f"   Total de pictogramas: {total_pictograms}")
    print(f"   Categorías nativas encontradas: {len(categories_native)}")
    
    return category_mappings, categories_native


def generate_report(category_mappings, categories_native, output_dir):
    """
    Genera reportes del análisis
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Reporte de categorías nativas
    print("\n📝 Generando reporte de categorías nativas...")
    native_report_path = output_dir / "native_categories_report.txt"
    with open(native_report_path, 'w', encoding='utf-8') as f:
        f.write("CATEGORÍAS NATIVAS DE ARASAAC\n")
        f.write("=" * 50 + "\n\n")
        for cat, count in categories_native.most_common(50):
            f.write(f"{cat}: {count} pictogramas\n")
    print(f"   ✅ Guardado en: {native_report_path}")
    
    # Reporte de mapeo a nuevas categorías
    print("\n📝 Generando reporte de nuevas categorías...")
    mapping_report_path = output_dir / "category_mappings_report.txt"
    with open(mapping_report_path, 'w', encoding='utf-8') as f:
        f.write("MAPEO A NUEVAS CATEGORÍAS\n")
        f.write("=" * 50 + "\n\n")
        
        for category in sorted(category_mappings.keys()):
            pictos = category_mappings[category]
            config = CATEGORY_KEYWORDS[category]
            
            f.write(f"\n{category.upper()} (Prioridad: {config['priority']}, Límite: {config['limit']})\n")
            f.write("-" * 50 + "\n")
            f.write(f"Pictogramas encontrados: {len(pictos)}\n\n")
            
            for i, picto in enumerate(pictos[:20], 1):  # Mostrar primeros 20
                f.write(f"  {i}. ID {picto['id']}: {picto['label']} ({picto['source']})\n")
            
            if len(pictos) > 20:
                f.write(f"  ... y {len(pictos) - 20} más\n")
    
    print(f"   ✅ Guardado en: {mapping_report_path}")
    
    # Generar archivo JSON para usar en la aplicación
    print("\n📝 Generando archivo JSON de categorías...")
    json_output_path = output_dir / "category_mappings.json"
    
    # Convertir a formato simple (solo IDs)
    simple_mappings = {}
    for category, pictos in category_mappings.items():
        simple_mappings[category] = [p['id'] for p in pictos]
    
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(simple_mappings, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Guardado en: {json_output_path}")
    
    # Resumen en consola
    print("\n" + "=" * 60)
    print("RESUMEN DE CATEGORÍAS")
    print("=" * 60)
    for category in sorted(category_mappings.keys(), key=lambda x: CATEGORY_KEYWORDS[x]['priority']):
        pictos = category_mappings[category]
        config = CATEGORY_KEYWORDS[category]
        priority_stars = "⭐" * config['priority']
        coverage = len(pictos) / config['limit'] * 100
        
        print(f"{priority_stars} {category:20s}: {len(pictos):3d}/{config['limit']:3d} ({coverage:5.1f}%)")


def main():
    """
    Función principal
    """
    print("\n" + "=" * 60)
    print("ANÁLISIS DE CATÁLOGO ARASAAC")
    print("Generación de Categorías Optimizadas para Usuarios")
    print("=" * 60 + "\n")
    
    # Rutas
    catalog_path = Path("nlp_backend/data/arasaac_catalog.jsonl")
    output_dir = Path("analysis_results")
    
    if not catalog_path.exists():
        print(f"❌ Error: No se encontró el catálogo en {catalog_path}")
        return
    
    # Ejecutar análisis
    category_mappings, categories_native = analyze_catalog(catalog_path)
    
    # Generar reportes
    generate_report(category_mappings, categories_native, output_dir)
    
    print("\n✅ Proceso completado exitosamente!")
    print(f"📁 Resultados guardados en: {output_dir}/")


if __name__ == "__main__":
    main()
