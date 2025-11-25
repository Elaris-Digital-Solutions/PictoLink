import re

# Cargar stopwords
with open('nlp_backend/stopwords_es.txt', encoding='utf-8') as f:
    STOPWORDS = set([line.strip() for line in f])

def clean_text(text):
    """Limpia el texto, elimina signos de puntuación y lo pasa a minúsculas."""
    text = re.sub(r'[¿?¡!.,;:\-]', ' ', text)
    text = text.lower()
    return text

def filter_words(text):
    """Filtra palabras irrelevantes y elimina duplicados."""
    words = clean_text(text).split()
    filtered = [w for w in words if w not in STOPWORDS]
    # Eliminar duplicados manteniendo el orden
    seen = set()
    result = []
    for w in filtered:
        if w not in seen:
            result.append(w)
            seen.add(w)
    return result

if __name__ == "__main__":
    # Ejemplo de uso
    frase = "¿Cómo estás? Buenos días, quiero ir a pasear a un perro."
    print(filter_words(frase))
