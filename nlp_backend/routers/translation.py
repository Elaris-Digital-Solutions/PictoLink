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

    # 0. Check for special phrases (Exact match with normalization)
    import json
    import os
    import unicodedata

    def normalize_text(text: str) -> str:
        # Remove accents and lowercase
        text = text.lower().strip()
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        # Keep only alphanumeric and spaces
        text = ''.join(c for c in text if c.isalnum() or c.isspace())
        return text.strip()

    try:
        # Path relative to this file: ../../frases_especiales.json
        # But safer to find it relative to the package root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        phrases_path = os.path.join(base_dir, "frases_especiales.json")
        
        if os.path.exists(phrases_path):
            with open(phrases_path, 'r', encoding='utf-8') as f:
                special_phrases = json.load(f)
                
            normalized_input = normalize_text(request.text)
            
            # Check for substring matches (longest first to prioritize longer phrases)
            matched_phrase = None
            matched_ids = None
            
            # Sort phrases by length (longest first) to match longer phrases first
            sorted_phrases = sorted(special_phrases.items(), key=lambda x: len(x[0]), reverse=True)
            
            for phrase, picto_ids in sorted_phrases:
                normalized_phrase = normalize_text(phrase)
                # Check if phrase is in the input (substring match)
                if normalized_phrase in normalized_input:
                    print(f"Substring match found for special phrase: '{phrase}' in '{request.text}'")
                    matched_phrase = normalized_phrase
                    matched_ids = picto_ids
                    break
            
            if matched_ids:
                result_pictos = []
                # Add pictograms for the matched phrase
                for pid in matched_ids:
                    try:
                        pid_int = int(pid)
                        picto = catalog.get_by_id(pid_int)
                        if picto:
                            result_pictos.append(picto)
                    except ValueError:
                        continue
                
                # Process remaining words (words not in the matched phrase)
                if matched_phrase:
                    # Remove the matched phrase from input and process remaining words
                    remaining_text = normalized_input.replace(matched_phrase, '').strip()
                    if remaining_text:
                        print(f"Processing remaining text: '{remaining_text}'")
                        # Process remaining text normally
                        remaining_tokens = nlp.process_text(remaining_text)
                        # Continue to normal token processing below for remaining words
                        tokens = remaining_tokens
                    else:
                        # Only the special phrase, return immediately
                        if result_pictos:
                            return {"pictograms": result_pictos}
                        
                # If we have result_pictos from special phrase, we'll add them first
                # and continue processing remaining tokens below
                if result_pictos and not remaining_text:
                    return {"pictograms": result_pictos}
    except Exception as e:
        print(f"Error checking special phrases: {e}")
    
    # Store special phrase pictograms to prepend later
    special_phrase_pictos = result_pictos if 'result_pictos' in locals() and result_pictos else []
        
    # 1. Process text (lemmatize)
    tokens = nlp.process_text(request.text)
    
    result_pictos = []
    
    # 2. Map tokens to pictograms
    
    # Priority mappings: Semantic overrides that should ALWAYS apply
    # (even if the base form exists in catalog)
    PRIORITY_MAP = {
        # Semantic shifts (verb -> noun)
        'viajar': 'viaje',
        'comprar': 'compra',
        'masturbar': 'masturbación',
        
        # Grammar corrections (conjunction -> question word)
        'que': 'qué',
        
        # Article fixes (prevent mapping to numbers/pronouns)
        'un': 'un',        # Article, not número 'uno'
        'una': 'una',
        'el': 'el',        # Article, not pronoun 'él'
        'la': 'la',        # Article, not pronoun 'ella'
        'los': 'los',
        'las': 'las',
        
        # Verb fixes (prevent fuzzy match to wrong forms)
        # Note: 'encantar' doesn't exist in catalog, map to 'gustar' instead
        'encanta': 'gustar',     # Map to 'gustar' (similar meaning, exists in catalog)
        'encantan': 'gustar',
        'gusta': 'gustar',       # Ensure correct verb form
        'gustan': 'gustar',
    }
    
    # Fallback mappings: For words missing from catalog
    FALLBACK_MAP = {
        # Possessives (replaced 'nuestra' with 'nuestro' - doesn't exist in catalog)
        'mi': 'mío', 'mis': 'mis',
        'tu': 'tú', 'tus': 'tú',
        'su': 'su', 'sus': 'su',
        'nuestro': 'nuestro', 'nuestra': 'nuestro',  # 'nuestra' doesn't exist, use 'nuestro'
        
        # Articles removed - should be found in catalog via lemma
        # (Removed: 'el', 'la', 'los', 'las', 'al', 'del', 'un', 'una', etc.)
        
        # Pronouns (removed 'la' mapping - conflicts with article)
        # Note: 'le' and 'les' don't exist in catalog, map to 'él' as fallback
        'yo': 'yo', 'me': 'yo', 'mí': 'yo',
        'tú': 'tú', 'te': 'tú', 'ti': 'tú',
        'él': 'él', 'lo': 'él',
        'ella': 'ella',
        'nosotros': 'nosotros', 'nos': 'nosotros',
        'vosotros': 'vosotros', 'os': 'vosotros',
        'ellos': 'ellos',
        
        # Verbs missing from catalog (map to similar verbs)
        'encantar': 'gustar',  # 'encantar' doesn't exist, use 'gustar'
        
        # Question words (replaced 'cuánto' with 'mucho' - doesn't exist in catalog)
        'quién': 'quién', 'quien': 'quién',
        'cómo': 'cómo', 'como': 'cómo',
        'cuándo': 'cuándo', 'cuando': 'cuándo',
        'dónde': 'dónde', 'donde': 'dónde',
        'cuánto': 'mucho', 'cuanto': 'mucho',  # 'cuánto' doesn't exist, use 'mucho'
        'por qué': 'por qué', 'porque': 'por qué',
        
        # Adverbs/Conjunctions
        'sí': 'sí', 'si': 'sí',
        'no': 'no',
        'y': 'y', 'o': 'o',
        'pero': 'pero',
        'muy': 'mucho',
        'más': 'más',
        'a': 'a', 'de': 'de', 'en': 'en', 'con': 'con', 'por': 'por', 'para': 'para',
        
        # Other semantic mappings (all replaced with existing terms)
        'educar': 'educación',
        'respirar': 'respirar',      # Changed from 'respiración' (doesn't exist)
        'caminar': 'andar',
        'pintar': 'pintura',
        'limpiar': 'limpieza',
        'vender': 'vender',          # Changed from 'venta' (doesn't exist)
        'necesitar': 'necesitar',    # Changed from 'necesidad' (doesn't exist)
        'odiar': 'odiar',            # Changed from 'odio' (doesn't exist)
        'sentir': 'sentimiento',
        'pensar': 'pensamiento',
        'saber': 'saber',            # Changed from 'sabiduría' (doesn't exist)
    }

    for token in tokens:
        text_lower = token['text'].lower()
        matches = []
            
        # Strategy 0: Check PRIORITY_MAP for semantic overrides
        if text_lower in PRIORITY_MAP:
             mapped_term = PRIORITY_MAP[text_lower]
             matches = catalog.find_by_term(mapped_term)
             if matches:
                 print(f"Priority mapping: '{text_lower}' -> '{mapped_term}'")
        
        # Strategy 1: Search by lemma (spaCy knows best for conjugations!)
        if not matches:
            matches = catalog.find_by_term(token['lemma'])
        
        # Strategy 2: Search by original text if no match
        if not matches:
            matches = catalog.find_by_term(token['text'])
            
        # Strategy 2.5: Handle reflexive verbs (cepillarme -> cepillar + yo)
        if not matches:
            text = token['text'].lower()
            reflexive_pronouns = {
                'me': 'yo',
                'te': 'tú', 
                'se': 'él',
                'nos': 'nosotros',
                'os': 'vosotros'
            }
            
            for suffix, pronoun in reflexive_pronouns.items():
                if text.endswith(suffix) and len(text) > len(suffix) + 3:
                    stem = text[:-len(suffix)]
                    
                    # Check PRIORITY_MAP for stem FIRST (e.g. masturbar -> masturbación)
                    if stem in PRIORITY_MAP:
                        matches = catalog.find_by_term(PRIORITY_MAP[stem])
                        if matches:
                            print(f"Reflexive Priority mapping: '{text}' -> '{stem}' -> '{PRIORITY_MAP[stem]}'")
                            result_pictos.append(matches[0])
                            # Add pronoun
                            pronoun_matches = catalog.find_by_term(pronoun)
                            if pronoun_matches:
                                result_pictos.append(pronoun_matches[0])
                            matches = []  # Clear to prevent double-add
                            break
                            
                    # Then check catalog for stem
                    matches = catalog.find_by_term(stem)
                    
                    # If exact stem match fails, try fuzzy (handles banar -> bañar)
                    if not matches:
                        matches = catalog.find_fuzzy(stem, threshold=85)
                        
                    if matches:
                        print(f"Reflexive match: '{text}' -> '{stem}'")
                        result_pictos.append(matches[0])
                        # Add pronoun
                        pronoun_matches = catalog.find_by_term(pronoun)
                        if pronoun_matches:
                            result_pictos.append(pronoun_matches[0])
                        matches = []  # Clear to prevent double-add
                        break
            
        # Strategy 2.6: Handle diminutives (solito -> solo, gatito -> gato, panecillo -> pan)
        if not matches:
            text = token['text'].lower()
            # Order matters: check longer suffixes first (cito before ito)
            diminutive_rules = [
                ('citos', ''), ('citas', ''), ('cito', ''), ('cita', ''), # amorcito -> amor
                ('itos', 'os'), ('itas', 'as'), ('ito', 'o'), ('ita', 'a'), # gatito -> gato
                ('illos', 'os'), ('illas', 'as'), ('illo', 'o'), ('illa', 'a'), # chiquillo -> chico
                ('icos', 'os'), ('icas', 'as'), ('ico', 'o'), ('ica', 'a')  # perrico -> perro
            ]
            
            for suffix, replacement in diminutive_rules:
                if text.endswith(suffix) and len(text) > len(suffix) + 2:
                    # Try replacement
                    stem = text[:-len(suffix)] + replacement
                    matches = catalog.find_by_term(stem)
                    if matches:
                        print(f"Diminutive match: '{text}' -> '{stem}'")
                        break
                    
                    # Try just stripping suffix (sometimes works for words ending in consonant + ito)
                    if replacement != '':
                        stem_stripped = text[:-len(suffix)]
                        matches = catalog.find_by_term(stem_stripped)
                        if matches:
                            print(f"Diminutive match (stripped): '{text}' -> '{stem_stripped}'")
                            break
                            
        # Strategy 2.7: FALLBACK_MAP for words missing in catalog
        if not matches:
            text = token['text'].lower()
            if text in FALLBACK_MAP:
                mapped_term = FALLBACK_MAP[text]
                matches = catalog.find_by_term(mapped_term)
                if matches:
                    print(f"Fallback mapping: '{text}' -> '{mapped_term}'")
            
        # Strategy 3: Fuzzy Search (New)
        if not matches:
            # Only try fuzzy if the word is long enough to avoid noise
            if len(token['text']) > 3:
                matches = catalog.find_fuzzy(token['text'])
            
        if matches:
            picto = matches[0]
            print(f"Token '{token['text']}' matched '{picto.labels.get('es', 'unknown')}' (ID: {picto.id})")
            result_pictos.append(picto)
        else:
            print(f"Token '{token['text']}' found NO MATCH")
    
    # Combine special phrase pictograms with regular pictograms
    final_pictos = special_phrase_pictos + result_pictos
    
    return {"pictograms": final_pictos}

@router.post("/pictos-to-text", response_model=TextResponse)
async def pictos_to_text(request: PictosRequest):
    # MVP: Simple concatenation
    words = []
    for picto in request.pictograms:
        if 'es' in picto.labels:
            words.append(picto.labels['es'])
            
    if not words:
        return {"text": ""}
        
    # Basic formatting
    text = " ".join(words)
    text = text.capitalize() + "."
    
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
