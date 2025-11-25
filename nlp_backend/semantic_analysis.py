import spacy
import re

# Cargar modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("El modelo 'es_core_news_sm' no está instalado. Instálalo con: python -m spacy download es_core_news_sm")
    nlp = None

def extract_key_concepts(text):
    """
    Extrae conceptos clave de una frase usando spaCy:
    - Sustantivos
    - Verbos
    - Adjetivos relevantes
    """
    if not nlp:
        return []
    doc = nlp(text)
    concepts = set()
    # Extraer sustantivos, verbos, adjetivos relevantes
    for token in doc:
        if token.pos_ in ["NOUN", "VERB", "ADJ"] and not token.is_stop:
            lemma = token.lemma_.lower()
            concepts.add(lemma)
    # Extraer entidades nombradas (países, lugares, personas, gentilicios)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC", "PERSON", "NORP"]:
            concepts.add(ent.text.lower())
    return list(concepts)

if __name__ == "__main__":
    frase = "¿Cómo estás? Buenos días, quiero ir a pasear a un perro."
    print(extract_key_concepts(frase))
