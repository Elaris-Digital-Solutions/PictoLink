import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_backend.routers.translation import text_to_pictos, TextRequest
from nlp_backend.services.catalog import CatalogService

async def main():
    print("Cargando catálogo de pictogramas... (esto puede tardar unos segundos)")
    catalog = CatalogService.get_instance()
    
    # Load real data
    meta_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'embeddings', 'meta.jsonl')
    catalog.load_data(meta_path)
    
    print("\n--- Sistema de Prueba Interactivo ---")
    print("Escribe una frase para traducirla a pictogramas.")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        text = input("Frase: ").strip()
        if text.lower() == 'salir':
            break
        
        if not text:
            continue
            
        try:
            request = TextRequest(text=text)
            response = await text_to_pictos(request)
            pictos = response['pictograms']
            
            print(f"\nResultado ({len(pictos)} pictogramas):")
            for p in pictos:
                label = p.labels.get('es', 'Sin etiqueta')
                print(f" - [{p.id}] {label}")
            print("-" * 30 + "\n")
            
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSaliendo...")
