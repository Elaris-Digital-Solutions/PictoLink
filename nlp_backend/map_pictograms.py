
import json
import os
import unicodedata
from semantic_analysis import extract_key_concepts

def normalize(text):
    text = text.lower().strip()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    for ch in ['¿', '?', '¡', '!', '.', ',', ';', ':', '-', '_', '"', "'", '(', ')']:
        text = text.replace(ch, '')
    text = ' '.join(text.split())
    return text

META_PATH = os.path.join('data', 'embeddings', 'meta.jsonl')
FRASES_PATH = os.path.join('nlp_backend', 'frases_especiales.json')

def load_pictogram_catalog():
    catalog = {}
    with open(META_PATH, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            if (
                not entry or
                'labels' not in entry or
                not isinstance(entry['labels'], dict) or
                'es' not in entry['labels'] or
                not isinstance(entry['labels']['es'], str)
            ):
                continue
            label = entry['labels']['es'].lower()
            catalog[label] = entry
            # Añadir sinónimos
            for syn in entry.get('synonyms', {}).get('es', []):
                if isinstance(syn, str):
                    catalog[syn.lower()] = entry
    return catalog

def load_frases_especiales():
    with open(FRASES_PATH, encoding='utf-8') as f:
        return json.load(f)

def map_frase_especial(frase, catalog, frases_dict):
    # usa la función global normalize

    frase_limpia = normalize(frase)
    result = []
    pronombres = ['yo', 'tu', 'tú', 'el', 'ella', 'nosotros', 'nosotras', 'mi', 'mis', 'su', 'sus', 'nuestro', 'nuestra', 'nuestros', 'nuestras']
    for frase_especial, ids in frases_dict.items():
        frase_especial_limpia = normalize(frase_especial)
        # Buscar frase especial o frase especial con pronombre
        if frase_especial_limpia in frase_limpia:
            for pid in ids:
                found = False
                for entry in catalog.values():
                    if str(entry.get('id')) == str(pid) or int(entry.get('id')) == int(pid):
                        result.append(entry)
                        import json
                        import os
                        import unicodedata
                        from semantic_analysis import extract_key_concepts
                        import unicodedata

                        # usa la función global normalize

        else:
            # Buscar variantes con pronombres
            for pron in pronombres:
                variante = f"{pron} {frase_especial_limpia}"
                if variante in frase_limpia:
                    for pid in ids:
                        found = False
                        for entry in catalog.values():
                            if str(entry.get('id')) == str(pid) or int(entry.get('id')) == int(pid):
                                result.append(entry)
                                found = True
                                break
                        if not found:
                            print(f"Advertencia: No se encontró pictograma para el id {pid}")
    if result:
        return result
    return None

def map_concepts_to_pictograms(concepts, catalog):
    result = []
    for concept in concepts:
        concept_norm = normalize(concept)
        for entry in catalog.values():
            label = entry['labels']['es'] if 'labels' in entry and 'es' in entry['labels'] else ''
            label_norm = normalize(label)
            synonyms = entry.get('synonyms', {}).get('es', [])
            synonyms_norm = [normalize(s) for s in synonyms if s]
            # Coincidencia parcial: singular/plural, variantes, substring
            if (concept_norm in label_norm or label_norm in concept_norm or
                any(concept_norm in syn or syn in concept_norm for syn in synonyms_norm)):
                if not (label_norm in 'abcdefghijklmnñopqrstuvwxyz' or label_norm.startswith('letra ')):
                    result.append(entry)
                    break
    return result
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Mapea frases a pictogramas ARASAAC")
    parser.add_argument('--frase', type=str, required=True, help='Frase a mapear')
    args = parser.parse_args()

    # Cargar frases especiales
    with open('nlp_backend/frases_especiales.json', encoding='utf-8') as f:
        frases_dict = json.load(f)

    # Cargar catálogo
    catalog = {}
    with open('data/embeddings/meta.jsonl', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            catalog[str(entry['id'])] = entry

    # Mapear frase especial primero
    pictos_especial = map_frase_especial(args.frase, catalog, frases_dict)
    concepts = extract_key_concepts(args.frase)
    print(f"Conceptos extraídos por semantic_analysis: {concepts}")
    # Si hay frase especial, quitar sus conceptos de la lista de conceptos
    conceptos_especiales = set()
    if pictos_especial:
        for pict in pictos_especial:
            if 'labels' in pict and 'es' in pict['labels']:
                conceptos_especiales.add(pict['labels']['es'].lower())
    conceptos_filtrados = [c for c in concepts if c.lower() not in conceptos_especiales]
    pictos_conceptos = map_concepts_to_pictograms(conceptos_filtrados, catalog) if conceptos_filtrados else []

    if pictos_especial:
        print(f"Frase: {args.frase}\nPictogramas detectados (frase especial):")
        for pict in pictos_especial:
            print(f"ID: {pict['id']}, Etiqueta: {pict['labels']['es']}, Imagen: {pict['image_urls']['png_color']}")
        if pictos_conceptos:
            print(f"Pictogramas adicionales (conceptos):")
            for pict in pictos_conceptos:
                print(f"ID: {pict['id']}, Etiqueta: {pict['labels']['es']}, Imagen: {pict['image_urls']['png_color']}")
    else:
        if pictos_conceptos:
            print(f"Frase: {args.frase}\nPictogramas detectados (conceptos):")
            for pict in pictos_conceptos:
                print(f"ID: {pict['id']}, Etiqueta: {pict['labels']['es']}, Imagen: {pict['image_urls']['png_color']}")
        else:
            print(f"Frase: {args.frase}\nNo se detectaron pictogramas para los conceptos extraídos.")
