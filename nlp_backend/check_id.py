
import json

file_path = r"c:\Users\jg153\OneDrive\Documentos\dev\PictoLink\data\embeddings\meta.jsonl"
target_id = 2654

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('id') == target_id:
                print(json.dumps(data, indent=2, ensure_ascii=False))
                break
        except:
            pass
