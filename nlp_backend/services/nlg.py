import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List
import os

class NLGService:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        
        model_id = "ElarisDigitalSolutions/PictoLink"
        print(f"Cargando modelo desde Hugging Face Hub: {model_id}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
            print("Modelo cargado correctamente.")
        except Exception as e:
            print(f"Error loading model from Hub: {e}")
            print("Using rule-based fallback.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_sentence(self, lemmas: List[str]) -> str:
        # Input preparation
        input_text = " ".join(lemmas)
        
        if self.model and self.tokenizer:
            try:
                input_ids = self.tokenizer.encode(input_text, return_tensors="pt", max_length=64, truncation=True)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        input_ids, 
                        max_length=64, 
                        num_beams=4, 
                        early_stopping=True,
                        no_repeat_ngram_size=2
                    )
                    
                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
                
                with open("nlg_debug.log", "a", encoding="utf-8") as f:
                    f.write(f"Raw output: '{generated_text}'\n")
                
                # Validation: Reject empty, single punctuation, or sentinel-like output
                # Explicitly check for <extra_id_0> even if skip_special_tokens=True failed
                if (generated_text and 
                    len(generated_text) > 2 and 
                    "<extra_id" not in generated_text and
                    not generated_text.startswith("<")):
                    return self._post_process(generated_text)
                else:
                    with open("nlg_debug.log", "a", encoding="utf-8") as f:
                        f.write("Output rejected. Using fallback.\n")
                    
            except Exception as e:
                with open("nlg_debug.log", "a", encoding="utf-8") as f:
                    f.write(f"Error: {e}\n")
                print(f"NLG Generation error: {e}")
        
        # Fallback if model missing or failed
        return self._fallback_generation(lemmas)
    
    def _fallback_generation(self, lemmas: List[str]) -> str:
        """
        Rule-based sentence generation as fallback.
        Applies basic Spanish grammar rules.
        """
        if not lemmas:
            return ""
        
        # Simple heuristics for Spanish
        sentence = []
        
        # Common verbs to conjugate (3rd person singular default)
        verb_map = {
            'comer': 'come',
            'beber': 'bebe',
            'jugar': 'juega',
            'dormir': 'duerme',
            'correr': 'corre',
            'saltar': 'salta',
            'caminar': 'camina',
            'ver': 've',
            'mirar': 'mira',
            'querer': 'quiere',
            'ir': 'va',
            'estar': 'está',
            'ser': 'es',
            'tener': 'tiene',
            'haber': 'hay',
            'gustar': 'le gusta',
            'encantar': 'le encanta',
            'cortar': 'corta',
            'barrer': 'barre',
            'pintar': 'pinta',
            'dibujar': 'dibuja',
            'leer': 'lee',
            'escribir': 'escribe',
            'escuchar': 'escucha',
            'hablar': 'habla'
        }

        for i, word in enumerate(lemmas):
            word_lower = word.lower()
            
            # Add article 'El' at the start if it's a noun (heuristic: not a verb/adj/pronoun)
            # This is a very rough heuristic.
            if i == 0 and word_lower not in ['yo', 'tú', 'él', 'ella', 'nosotros', 'ellos'] and word_lower not in verb_map:
                # Assume masculine for simplicity unless ends in 'a'
                if word_lower.endswith('a') and not word_lower.endswith('ista'):
                    sentence.append("La " + word.capitalize())
                else:
                    sentence.append("El " + word.capitalize())
                continue
            
            # Capitalize first word if we didn't add an article
            if i == 0:
                sentence.append(word.capitalize())
                continue

            # Handle verb conjugations
            if word_lower in verb_map:
                # Special handling for 'yo'
                if i > 0 and lemmas[i-1].lower() == 'yo':
                    if word_lower == 'comer': sentence.append('como')
                    elif word_lower == 'beber': sentence.append('bebo')
                    elif word_lower == 'jugar': sentence.append('juego')
                    elif word_lower == 'dormir': sentence.append('duermo')
                    elif word_lower == 'querer': sentence.append('quiero')
                    elif word_lower == 'ir': sentence.append('voy')
                    elif word_lower == 'estar': sentence.append('estoy')
                    elif word_lower == 'ser': sentence.append('soy')
                    elif word_lower == 'tener': sentence.append('tengo')
                    elif word_lower == 'gustar': sentence.append('me gusta')
                    else: sentence.append(word)
                else:
                    sentence.append(verb_map[word_lower])
            
            # Generic conjugation heuristic for unknown verbs
            elif word_lower.endswith('ar') or word_lower.endswith('er') or word_lower.endswith('ir'):
                # Very naive check if it's likely a verb (length > 3)
                if len(word_lower) > 3:
                    if word_lower.endswith('ar'):
                        sentence.append(word_lower[:-2] + 'a')
                    elif word_lower.endswith('er'):
                        sentence.append(word_lower[:-2] + 'e')
                    elif word_lower.endswith('ir'):
                        sentence.append(word_lower[:-2] + 'e')
                else:
                    sentence.append(word)
            else:
                sentence.append(word)
        
        result = " ".join(sentence)
        
        # Add period if not present
        if not result.endswith('.'):
            result += '.'
            
        return result
    
    def _post_process(self, text: str) -> str:
        """Clean up generated text."""
        text = text.strip()
        
        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]
        
        # Ensure it ends with punctuation
        if text and not text[-1] in '.!?':
            text += '.'
            
        return text
