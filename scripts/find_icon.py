import json

def find_icon(keyword):
    with open('public/data/arasaac_catalog.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if 'es' in data['labels']:
                    if keyword.lower() == data['labels']['es'].lower():
                        print(f"Found exact match: ID={data['id']}, Label={data['labels']['es']}")
            except Exception as e:
                pass

find_icon('plato')
find_icon('manzana')
