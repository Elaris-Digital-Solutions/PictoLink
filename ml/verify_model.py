from nlp_backend.services.nlg import NLGService

def main():
    print("Initializing NLG Service...")
    nlg = NLGService.get_instance()
    
    test_cases = [
        ["yo", "comer", "manzana"],
        ["el", "niño", "jugar", "pelota"],
        ["yo", "querer", "dormir"],
        ["perro", "grande"],
        ["ella", "estar", "feliz"]
    ]
    
    print("\n--- Testing Generation ---")
    for lemmas in test_cases:
        print(f"\nInput: {lemmas}")
        result = nlg.generate_sentence(lemmas)
        print(f"Output: {result}")

if __name__ == "__main__":
    main()
