import json

ids_to_check = [32464, 4610, 2519] # 2519 is often 'plato' or similar in other catalogs, just guessing/checking.

def check_ids():
    with open('public/data/arasaac_catalog.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if data['id'] in ids_to_check:
                print(f"ID: {data['id']}")
                print(f"Label (ES): {data['labels']['es']}")
                print(f"Description/Keywords: {data.get('sources', {}).get('es', {}).get('keywords', [])}")
                print("-" * 20)

check_ids()
