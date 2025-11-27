
import json

file_path = r"c:\Users\jg153\OneDrive\Documentos\dev\PictoLink\data\embeddings\meta.jsonl"
search_term = "escaleras"

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        if search_term in line.lower():
            try:
                data = json.loads(line)
                print(f"ID: {data.get('id')}, Label: {data.get('labels', {}).get('es')}, Synonyms: {data.get('synonyms', {}).get('es')}")
            except:
                pass
