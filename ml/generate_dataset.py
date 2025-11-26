import json
import random
import os
from typing import List, Dict

# Configuration
OUTPUT_FILE = "ml/dataset_picto_v1.jsonl"
CATALOG_PATH = "nlp_backend/data/arasaac_catalog.jsonl"
NUM_SAMPLES = 50

# Templates for synthetic generation
# {S} = Subject, {V} = Verb, {O} = Object, {Adj} = Adjective
TEMPLATES = [
    # Simple SVO
    {
        "pattern": ["{S}", "{V}", "{O}"],
        "targets": [
            "El {S} {V} {O}.",
            "Un {S} {V} {O}.",
            "El {S} está {V_gerund} {O}."
        ]
    },
    # SV
    {
        "pattern": ["{S}", "{V}"],
        "targets": [
            "El {S} {V}.",
            "El {S} está {V_gerund}."
        ]
    },
    # S V Adj
    {
        "pattern": ["{S}", "{V}", "{Adj}"],
        "targets": [
            "El {S} es {Adj}.",
            "El {S} está {Adj}."
        ]
    },
    # Imperative / Request (Yo querer X)
    {
        "pattern": ["yo", "querer", "{O}"],
        "targets": [
            "Yo quiero {O}.",
            "Quiero {O}.",
            "Me gustaría {O}."
        ]
    },
    {
        "pattern": ["yo", "querer", "{V}"],
        "targets": [
            "Yo quiero {V}.",
            "Quiero {V}.",
            "Me gustaría {V}."
        ]
    }
]

def load_catalog(path: str) -> Dict[str, List[str]]:
    """Loads nouns, verbs, adjectives from catalog."""
    nouns = []
    verbs = []
    adjectives = []
    
    print(f"Loading catalog from {path}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    labels = data.get('labels', {})
                    tags = data.get('tags', [])
                    
                    if 'es' in labels:
                        word = labels['es']
                        
                        # Simple POS tagging based on tags/categories
                        # This is heuristic and noisy, but sufficient for v1
                        is_verb = False
                        is_adj = False
                        is_noun = True # Default
                        
                        # Check keywords for type (if available)
                        # Or infer from tags
                        
                        # Heuristic: Verbs often end in ar/er/ir and don't have article
                        if word.endswith(('ar', 'er', 'ir')) and ' ' not in word:
                            # Check if it's likely a verb
                            verbs.append(word)
                            is_noun = False
                        
                        if 'adjective' in tags or 'qualifier' in tags:
                            adjectives.append(word)
                            is_noun = False
                            
                        if is_noun and ' ' not in word:
                            nouns.append(word)
                            
                except Exception:
                    continue
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return {"nouns": [], "verbs": [], "adjectives": []}
        
    print(f"Loaded {len(nouns)} nouns, {len(verbs)} verbs, {len(adjectives)} adjectives.")
    return {
        "nouns": nouns,
        "verbs": verbs,
        "adjectives": adjectives
    }

def conjugate_verb(verb: str, tense: str = "present_3s") -> str:
    """Very basic conjugation for synthetic data."""
    # This is a placeholder. In a real scenario, use a library like `pattern-es` or `spacy`.
    # For now, we'll just return the infinitive or a simple heuristic.
    
    if tense == "gerund":
        if verb.endswith("ar"): return verb[:-2] + "ando"
        if verb.endswith("er"): return verb[:-2] + "iendo"
        if verb.endswith("ir"): return verb[:-2] + "iendo"
        return verb
        
    # Present 3rd person singular (El come)
    if verb.endswith("ar"): return verb[:-2] + "a"
    if verb.endswith("er"): return verb[:-2] + "e"
    if verb.endswith("ir"): return verb[:-2] + "e"
    
    return verb

def generate_sample(vocab: Dict[str, List[str]]) -> Dict:
    template = random.choice(TEMPLATES)
    pattern = template["pattern"]
    target_template = random.choice(template["targets"])
    
    source_words = []
    target_words = target_template
    
    replacements = {}
    
    # Fill slots
    if "{S}" in str(pattern) or "{S}" in target_template:
        s = random.choice(vocab["nouns"]) if vocab["nouns"] else "persona"
        replacements["{S}"] = s
    
    if "{O}" in str(pattern) or "{O}" in target_template:
        o = random.choice(vocab["nouns"]) if vocab["nouns"] else "cosa"
        replacements["{O}"] = o
        
    if "{Adj}" in str(pattern) or "{Adj}" in target_template:
        adj = random.choice(vocab["adjectives"]) if vocab["adjectives"] else "bueno"
        replacements["{Adj}"] = adj
        
    if "{V}" in str(pattern) or "{V}" in target_template:
        v = random.choice(vocab["verbs"]) if vocab["verbs"] else "hacer"
        replacements["{V}"] = v # Infinitive for source
        
        # Conjugate for target if needed (simplified)
        # We replace {V} in target with conjugated form if it's not "querer {V}" structure
        # But our templates are simple. Let's handle specific keys.
        
        v_gerund = conjugate_verb(v, "gerund")
        replacements["{V_gerund}"] = v_gerund
        
        # If target has {V} and it's not the infinitive slot (like "Quiero {V}"), we might need conjugation
        # For this script, we'll assume {V} in target is 3rd person unless context implies otherwise
        # But wait, "El {S} {V}" -> {V} should be conjugated.
        # "Quiero {V}" -> {V} should be infinitive.
        
        # Let's do a quick hack:
        if "El {S}" in target_template or "Un {S}" in target_template:
             replacements["{V}"] = conjugate_verb(v, "present_3s")
        else:
             replacements["{V}"] = v # Keep infinitive
             
    
    # Build Source
    real_source = []
    for token in pattern:
        if token in replacements:
            real_source.append(replacements[token])
        else:
            real_source.append(token) # Literal like "yo", "querer"
            
    # Build Target
    real_target = target_template
    for key, val in replacements.items():
        real_target = real_target.replace(key, val)
        
    return {
        "source": " ".join(real_source),
        "target": real_target
    }

def main():
    if not os.path.exists("ml"):
        os.makedirs("ml")
        
    vocab = load_catalog(CATALOG_PATH)
    
    if not vocab["nouns"]:
        print("Warning: Vocabulary empty. Checking path...")
        # Fallback for testing if catalog missing
        vocab = {
            "nouns": ["gato", "perro", "niño", "manzana", "pelota", "casa"],
            "verbs": ["comer", "jugar", "dormir", "saltar", "ver"],
            "adjectives": ["grande", "rojo", "feliz", "rápido"]
        }
    
    print(f"Generating {NUM_SAMPLES} samples...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for _ in range(NUM_SAMPLES):
            sample = generate_sample(vocab)
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            
    print(f"Done. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
