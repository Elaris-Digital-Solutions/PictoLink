
import json

file_path = r"c:\Users\jg153\OneDrive\Documentos\dev\PictoLink\data\embeddings\meta.jsonl"
search_term = "lavar los dientes"

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            label = data.get('labels', {}).get('es', '').lower()
            synonyms = [s.lower() for s in data.get('synonyms', {}).get('es', [])]
            
            if search_term in label or search_term in synonyms:
                print(f"ID: {data.get('id')}, Label: {data.get('labels', {}).get('es')}, Synonyms: {data.get('synonyms', {}).get('es')}")
        except:
            pass
