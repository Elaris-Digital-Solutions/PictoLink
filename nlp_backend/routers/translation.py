from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

router = APIRouter()

class TextRequest(BaseModel):
    text: str

class PictoItem(BaseModel):
    id: int
    labels: dict
    image_urls: dict

class PictosResponse(BaseModel):
    pictograms: List[PictoItem]

class PictosRequest(BaseModel):
    pictograms: List[PictoItem]

class TextResponse(BaseModel):
    text: str

@router.post("/text-to-pictos", response_model=PictosResponse)
async def text_to_pictos(request: TextRequest):
    catalog = CatalogService.get_instance()
    nlp = NLPService.get_instance()
    
    if not catalog.loaded:
        raise HTTPException(status_code=503, detail="Catalog not loaded yet")

    import unicodedata
    import numpy as np

    def normalize_text(text: str) -> str:
        # Remove accents and lowercase
        text = text.lower().strip()
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        # Keep only alphanumeric and spaces
        text = ''.join(c for c in text if c.isalnum() or c.isspace())
        return text.strip()

    # 1. Pre-process text
    doc = nlp.process_text(request.text)
    token_texts = [t['text'] for t in doc]
    token_lemmas = [t['lemma'] for t in doc]
    
    final_pictos = []
    i = 0
    n = len(token_texts)
    
    # Stopwords to ignore (unless part of a phrase)
    STOPWORDS = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'al', 'del', 'de', 'a', 'en', 'con', 'por', 'para', 'y', 'o'
    }

    # Priority mappings (Semantic overrides & Conjugations)
    PRIORITY_MAP = {
        'viajar': 'viaje', 'comprar': 'compra', 'masturbar': 'masturbación',
        'que': 'qué', 
        'encanta': 'gustar', 'encantan': 'gustar', 'gusta': 'gustar', 'gustan': 'gustar',
        'come': 'comer', 'comes': 'comer', 'comen': 'comer', 'comemos': 'comer',
        'bebe': 'beber', 'bebes': 'beber', 'beben': 'beber',
        'duerme': 'dormir', 'duermen': 'dormir', 'juega': 'jugar', 'juegan': 'jugar',
        'quiero': 'querer', 'quieres': 'querer', 'quiere': 'querer', 'queremos': 'querer', 'quieren': 'querer',
        'tengo': 'tener', 'tienes': 'tener', 'tiene': 'tener', 'tenemos': 'tener', 'tienen': 'tener',
        'voy': 'ir', 'vas': 'ir', 'va': 'ir', 'vamos': 'ir', 'van': 'ir',
        'soy': 'ser', 'eres': 'ser', 'es': 'ser', 'somos': 'ser', 'son': 'ser',
        'estoy': 'estar', 'estás': 'estar', 'está': 'estar', 'estamos': 'estar', 'están': 'estar',
        'lavo': 'lavar', 'lavas': 'lavar', 'lava': 'lavar', 'lavamos': 'lavar', 'lavan': 'lavar',
        'cepillo': 'cepillar', 'cepillas': 'cepillar', 'cepilla': 'cepillar',
        'ducho': 'duchar', 'duchas': 'duchar', 'ducha': 'duchar',
        'baño': 'bañar', 'bañas': 'bañar', 'baña': 'bañar',
        'visto': 'vestir', 'vistes': 'vestir', 'viste': 'vestir',
        'pongo': 'poner', 'pones': 'poner', 'pone': 'poner',
        'quito': 'quitar', 'quitas': 'quitar', 'quita': 'quitar',
    }
    
    FALLBACK_MAP = {
        'mi': 'mío', 'mis': 'mis', 'tu': 'tú', 'tus': 'tú', 'su': 'su', 'sus': 'su',
        'nuestro': 'nuestro', 'nuestra': 'nuestro',
        'yo': 'yo', 'me': 'yo', 'mí': 'yo', 'tú': 'tú', 'te': 'tú', 'ti': 'tú',
        'él': 'él', 'lo': 'él', 'ella': 'ella', 'nosotros': 'nosotros', 'nos': 'nosotros',
        'vosotros': 'vosotros', 'os': 'vosotros', 'ellos': 'ellos',
        'encantar': 'gustar',
        'quién': 'quién', 'quien': 'quién', 'cómo': 'cómo', 'como': 'cómo',
        'cuándo': 'cuándo', 'cuando': 'cuándo', 'dónde': 'dónde', 'donde': 'dónde',
        'cuánto': 'mucho', 'cuanto': 'mucho',
        'por qué': 'por qué', 'porque': 'por qué',
        'sí': 'sí', 'si': 'sí', 'no': 'no', 'pero': 'pero',
        'muy': 'mucho', 'más': 'más',
    }

    # Context embedding for re-ranking
    context_embedding = None
    if catalog.semantic_engine:
        try:
            context_embedding = catalog.semantic_engine.get_embedding(request.text)
        except Exception:
            pass

    while i < n:
        match_found = False
        
        # Strategy 1: Longest Matching N-gram (Phrase Matching)
        max_gram = min(5, n - i)
        
        for k in range(max_gram, 1, -1):
            phrase_tokens = token_texts[i : i+k]
            phrase_text = " ".join(phrase_tokens)
            normalized_phrase = normalize_text(phrase_text)
            
            matches = catalog.find_by_term(normalized_phrase)
            
            if not matches and k > 1:
                phrase_lemmas = token_lemmas[i : i+k]
                lemma_phrase = " ".join(phrase_lemmas)
                normalized_lemma_phrase = normalize_text(lemma_phrase)
                matches = catalog.find_by_term(normalized_lemma_phrase)
            
            if matches:
                print(f"Phrase match found: '{phrase_text}' -> '{matches[0].labels.get('es')}'")
                final_pictos.append(matches[0])
                i += k
                match_found = True
                break
        
        if match_found:
            continue
            
        # Process single token
        current_token = doc[i]
        text_lower = current_token['text'].lower()
        lemma_lower = current_token['lemma'].lower()
        matches = []
        
        # Check Stopwords (Skip if found)
        if text_lower in STOPWORDS:
            print(f"Skipping stopword: '{text_lower}'")
            i += 1
            continue
        
        # Strategy 2: Priority Map
        if text_lower in PRIORITY_MAP:
            mapped_term = PRIORITY_MAP[text_lower]
            matches = catalog.find_by_term(mapped_term)
            if matches:
                print(f"Priority mapping: '{text_lower}' -> '{mapped_term}'")
        
        # Strategy 3: Lemma Search
        if not matches:
            matches = catalog.find_by_term(lemma_lower)
            
        # Strategy 4: Original Text Search
        if not matches:
            matches = catalog.find_by_term(text_lower)
            
        # Strategy 5: Reflexive Verbs
        if not matches:
            reflexive_pronouns = {'me': 'yo', 'te': 'tú', 'se': 'él', 'nos': 'nosotros', 'os': 'vosotros'}
            for suffix, pronoun in reflexive_pronouns.items():
                if text_lower.endswith(suffix) and len(text_lower) > len(suffix) + 3:
                    stem = text_lower[:-len(suffix)]
                    stem_term = PRIORITY_MAP.get(stem, stem)
                    stem_matches = catalog.find_by_term(stem_term)
                    
                    if not stem_matches:
                         stem_matches = catalog.find_fuzzy(stem_term, threshold=85)
                         
                    if stem_matches:
                        print(f"Reflexive match: '{text_lower}' -> '{stem}'")
                        final_pictos.append(stem_matches[0])
                        # Add pronoun
                        pronoun_matches = catalog.find_by_term(pronoun)
                        if pronoun_matches:
                            final_pictos.append(pronoun_matches[0])
                        match_found = True
                        break
            if match_found:
                i += 1
                continue

        # Strategy 6: Diminutives
        if not matches:
             diminutive_rules = [
                ('citos', ''), ('citas', ''), ('cito', ''), ('cita', ''),
                ('itos', 'os'), ('itas', 'as'), ('ito', 'o'), ('ita', 'a'),
                ('illos', 'os'), ('illas', 'as'), ('illo', 'o'), ('illa', 'a'),
                ('icos', 'os'), ('icas', 'as'), ('ico', 'o'), ('ica', 'a')
            ]
             for suffix, replacement in diminutive_rules:
                if text_lower.endswith(suffix) and len(text_lower) > len(suffix) + 2:
                    stem = text_lower[:-len(suffix)] + replacement
                    matches = catalog.find_by_term(stem)
                    if matches:
                        print(f"Diminutive match: '{text_lower}' -> '{stem}'")
                        break
                    
                    # Try just stripping suffix (sometimes works for words ending in consonant + ito)
                    if replacement != '':
                        stem_stripped = text_lower[:-len(suffix)]
                        matches = catalog.find_by_term(stem_stripped)
                        if matches:
                            print(f"Diminutive match (stripped): '{text_lower}' -> '{stem_stripped}'")
                            break
        
        # Strategy 7: Fallback Map
        if not matches and text_lower in FALLBACK_MAP:
             mapped_term = FALLBACK_MAP[text_lower]
             matches = catalog.find_by_term(mapped_term)
             if matches:
                 print(f"Fallback mapping: '{text_lower}' -> '{mapped_term}'")

        # Strategy 8: Semantic Search
        if not matches and catalog.semantic_engine:
             if len(text_lower) > 2 and not current_token['is_stop']:
                 print(f"Trying semantic search for '{text_lower}'...")
                 semantic_matches = catalog.search_semantic(text_lower, limit=5)
                 if semantic_matches:
                     matches = [m[0] for m in semantic_matches if m[1] > 0.4]

        # Strategy 9: Fuzzy Search (Restricted)
        if not matches:
            if len(text_lower) > 4:
                matches = catalog.find_fuzzy(text_lower)

        # Re-ranking
        if matches and len(matches) > 1 and context_embedding is not None:
             try:
                scores = []
                for m in matches:
                    label = m.labels.get('es', '')
                    if label:
                        label_emb = catalog.semantic_engine.get_vector_by_id(m.id)
                        if label_emb is None:
                            label_emb = catalog.semantic_engine.get_embedding(label)
                        score = np.dot(context_embedding, label_emb)
                        scores.append((score, m))
                if scores:
                    scores.sort(key=lambda x: x[0], reverse=True)
                    matches = [scores[0][1]]
             except Exception:
                 pass

        if matches:
            final_pictos.append(matches[0])
        else:
            print(f"Token '{text_lower}' found NO MATCH")
            
        i += 1

    return {"pictograms": final_pictos}

@router.post("/pictos-to-text", response_model=TextResponse)
async def pictos_to_text(request: PictosRequest):
    from nlp_backend.services.nlg import NLGService
    
    lemmas = []
    for picto in request.pictograms:
        if 'es' in picto.labels:
            lemmas.append(picto.labels['es'])
            
    if not lemmas:
        return {"text": ""}
        
    # Use NLG to generate natural sentence
    nlg = NLGService.get_instance()
    text = nlg.generate_sentence(lemmas)
    
    return {"text": text}

@router.get("/search", response_model=PictosResponse)
async def search_pictograms(q: str):
    catalog = CatalogService.get_instance()
    if not catalog.loaded:
        raise HTTPException(status_code=503, detail="Catalog not loaded yet")
        
    matches = catalog.find_by_term(q)
    # Limit results to 20
    return {"pictograms": matches[:20]}

@router.get("/autocomplete", response_model=List[str])
async def autocomplete(q: str):
    catalog = CatalogService.get_instance()
    if not catalog.loaded:
        return []
        
    return catalog.search_autocomplete(q)
