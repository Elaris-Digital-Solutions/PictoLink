
import json
import os
import unicodedata
from semantic_analysis import extract_key_concepts

def normalize(text):
    if text is None:
        return ""
    text = str(text).lower().strip()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    for ch in ['¿', '?', '¡', '!', '.', ',', ';', ':', '-', '_', '"', "'", '(', ')']:
        text = text.replace(ch, '')
    text = ' '.join(text.split())
    return text

META_PATH = os.path.join('data', 'embeddings', 'meta.jsonl')
FRASES_PATH = os.path.join('nlp_backend', 'frases_especiales.json')

def load_pictogram_catalog():
    """
    Carga el catálogo de pictogramas.
    Retorna dos diccionarios:
    - by_id: mapa de id -> entry
    - by_label: mapa de etiqueta_normalizada -> entry (incluye sinónimos)
    """
    by_id = {}
    by_label = {}
    
    if not os.path.exists(META_PATH):
        # Fallback for running from different directories
        meta_path_alt = os.path.join('..', 'data', 'embeddings', 'meta.jsonl')
        if os.path.exists(meta_path_alt):
            path_to_use = meta_path_alt
        else:
            print(f"Error: No se encuentra meta.jsonl en {META_PATH}")
            return {}, {}
    else:
        path_to_use = META_PATH

    with open(path_to_use, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            
            if not entry or 'id' not in entry:
                continue

            # Index by ID
            by_id[str(entry['id'])] = entry
            
            # Index by Label and Synonyms
            if 'labels' in entry and isinstance(entry['labels'], dict) and 'es' in entry['labels']:
                label = entry['labels']['es']
                if isinstance(label, str):
                    norm_label = normalize(label)
                    # Prioritize shorter IDs or specific logic if duplicates exist? 
                    # For now, just overwrite or keep first. Let's keep first to be stable.
                    if norm_label not in by_label:
                        by_label[norm_label] = entry
            
            for syn in entry.get('synonyms', {}).get('es', []):
                if isinstance(syn, str):
                    norm_syn = normalize(syn)
                    if norm_syn not in by_label:
                        by_label[norm_syn] = entry
                        
    return by_id, by_label

def load_frases_especiales():
    path_to_use = FRASES_PATH
    if not os.path.exists(path_to_use):
         path_to_use = os.path.join('nlp_backend', 'frases_especiales.json') # Try relative
    
    if os.path.exists(path_to_use):
        with open(path_to_use, encoding='utf-8') as f:
            return json.load(f)
    return {}

def map_frase_especial(frase, catalog_by_id, frases_dict):
    frase_limpia = normalize(frase)
    result = []
    pronombres = ['yo', 'tu', 'tú', 'el', 'ella', 'nosotros', 'nosotras', 'mi', 'mis', 'su', 'sus', 'nuestro', 'nuestra', 'nuestros', 'nuestras']
    
    for frase_especial, ids in frases_dict.items():
        frase_especial_limpia = normalize(frase_especial)
        # Buscar frase especial o frase especial con pronombre
        if frase_especial_limpia in frase_limpia:
            for pid in ids:
                entry = catalog_by_id.get(str(pid))
                if entry:
                    result.append(entry)
        else:
            # Buscar variantes con pronombres
            for pron in pronombres:
                variante = f"{pron} {frase_especial_limpia}"
                if variante in frase_limpia:
                    for pid in ids:
                        entry = catalog_by_id.get(str(pid))
                        if entry:
                            result.append(entry)
    
    # Remove duplicates preserving order
    unique_result = []
    seen_ids = set()
    for r in result:
        if r['id'] not in seen_ids:
            unique_result.append(r)
            seen_ids.add(r['id'])
            
    return unique_result if unique_result else None

def map_concepts_to_pictograms(concepts, catalog_by_id):
    result = []
    # This is the old "slow" way but we need it for fuzzy matching on concepts
    # Optimization: iterate only if necessary or build a better index?
    # For now, keep it but maybe use the by_label index if exact match on concept?
    
    # Let's use by_label for exact concept matches first, then fallback to partial?
    # The original code did partial matching: "concept_norm in label_norm"
    
    catalog_values = list(catalog_by_id.values()) # Cache this list?
    
    for concept in concepts:
        concept_norm = normalize(concept)
        found = False
        
        # Try exact match first (much faster)
        # We need the by_label index here, but this function signature only took catalog (values).
        # Let's just iterate for now to preserve original behavior of partial matching
        # unless we want to change that too. The user asked for "bajar las escaleras" fix.
        
        for entry in catalog_values:
            label = entry['labels']['es'] if 'labels' in entry and 'es' in entry['labels'] else ''
            label_norm = normalize(label)
            if not label_norm:
                continue
                
            synonyms = entry.get('synonyms', {}).get('es', [])
            # Filter out empty synonyms after normalization (e.g. "," becomes "")
            synonyms_norm = [normalize(s) for s in synonyms if s]
            synonyms_norm = [s for s in synonyms_norm if s] 
            
            # Coincidencia parcial: singular/plural, variantes, substring
            # STRICTER MATCHING:
            # 1. Exact match always ok
            # 2. Substring match ONLY if it matches a whole word in the target string
            
            match = False
            if concept_norm == label_norm:
                match = True
            else:
                # Check if concept_norm is a distinct word in label_norm
                # e.g. "error" in "terrorismo" -> False
                # e.g. "bajar" in "bajar las escaleras" -> True
                
                # Split label into words and check if concept is one of them
                label_words = label_norm.split()
                if concept_norm in label_words:
                    match = True
                
                # Also check synonyms
                if not match:
                    for syn in synonyms_norm:
                        if concept_norm == syn:
                            match = True
                            break
                        syn_words = syn.split()
                        if concept_norm in syn_words:
                            match = True
                            break
            
            if match:
                if not (label_norm in 'abcdefghijklmnñopqrstuvwxyz' or label_norm.startswith('letra ')):
                    result.append(entry)
                    found = True
                    break
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Mapea frases a pictogramas ARASAAC")
    parser.add_argument('--frase', type=str, required=True, help='Frase a mapear')
    args = parser.parse_args()

    # Cargar catálogos
    catalog_by_id, catalog_by_label = load_pictogram_catalog()
    frases_dict = load_frases_especiales()

    frase_norm = normalize(args.frase)
    
    # 1. Intentar coincidencia exacta de la frase completa
    if frase_norm in catalog_by_label:
        picto = catalog_by_label[frase_norm]
        print(f"Frase: {args.frase}\nPictogramas detectados (coincidencia exacta):")
        print(f"ID: {picto['id']}, Etiqueta: {picto['labels']['es']}, Imagen: {picto['image_urls']['png_color']}")
        exit(0)

    # 2. Mapear frase especial
    pictos_especial = map_frase_especial(args.frase, catalog_by_id, frases_dict)
    
    concepts = extract_key_concepts(args.frase)
    print(f"Conceptos extraídos por semantic_analysis: {concepts}")
    
    # Si hay frase especial, quitar sus conceptos de la lista de conceptos
    conceptos_especiales = set()
    if pictos_especial:
        for pict in pictos_especial:
            if 'labels' in pict and 'es' in pict['labels']:
                conceptos_especiales.add(pict['labels']['es'].lower())
    
    conceptos_filtrados = [c for c in concepts if c.lower() not in conceptos_especiales]
    
    # 3. Mapear conceptos restantes
    pictos_conceptos = map_concepts_to_pictograms(conceptos_filtrados, catalog_by_id) if conceptos_filtrados else []

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
