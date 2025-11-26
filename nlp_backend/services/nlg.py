import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import List

class NLGService:
    _instance = None
    
    def __init__(self, model_name: str = "google/mt5-small"):
        # Disable model loading for now to avoid <extra_id_0> issues
        # and memory overhead. Using rule-based fallback.
        print("NLG Service initialized (Rule-based mode).")
        self.model = None
        self.tokenizer = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_sentence(self, lemmas: List[str]) -> str:
        if not self.model or not self.tokenizer:
            return self._fallback_generation(lemmas)
        
        # Try multiple prompting strategies
        prompts = [
            f"Forma una frase con estas palabras: {' '.join(lemmas)}",
            f"Escribe una oración usando: {' '.join(lemmas)}",
            " ".join(lemmas)  # Simple concatenation as last resort
        ]
        
        for prompt in prompts:
            try:
                input_ids = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        input_ids, 
                        max_length=100, 
                        num_beams=5, 
                        early_stopping=True,
                        no_repeat_ngram_size=2,
                        temperature=0.7,
                        do_sample=False
                    )
                    
                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
                
                # Check if generation is valid (not empty, not just special tokens, not same as input)
                if generated_text and len(generated_text) > 3 and generated_text != prompt:
                    # Additional validation: check if it's not just repeating the prompt
                    if not generated_text.startswith("Forma una frase") and not generated_text.startswith("Escribe una"):
                        return self._post_process(generated_text)
            except Exception as e:
                print(f"Error with prompt '{prompt[:30]}...': {e}")
                continue
        
        # If all prompts fail, use rule-based fallback
        print("NLG model failed, using rule-based fallback")
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
        
        for i, word in enumerate(lemmas):
            word_lower = word.lower()
            
            # Capitalize first word
            if i == 0:
                sentence.append(word.capitalize())
            # Handle common verb conjugations
            elif word_lower in ['querer', 'ir', 'estar', 'ser', 'tener']:
                # Try to conjugate based on subject (very basic)
                if lemmas[0].lower() == 'yo':
                    conjugations = {
                        'querer': 'quiero',
                        'ir': 'voy',
                        'estar': 'estoy',
                        'ser': 'soy',
                        'tener': 'tengo'
                    }
                    sentence.append(conjugations.get(word_lower, word))
                elif lemmas[0].lower() in ['él', 'ella']:
                    conjugations = {
                        'querer': 'quiere',
                        'ir': 'va',
                        'estar': 'está',
                        'ser': 'es',
                        'tener': 'tiene'
                    }
                    sentence.append(conjugations.get(word_lower, word))
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
