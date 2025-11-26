import sys
import os
import asyncio

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from nlp_backend.routers.translation import text_to_pictos, TextRequest
from nlp_backend.services.catalog import CatalogService
from nlp_backend.services.nlp import NLPService

async def run_50_phrase_test():
    # Initialize services
    print("Inicializando servicios...")
    catalog = CatalogService.get_instance()
    data_path = os.path.join("nlp_backend", "data", "arasaac_catalog.jsonl")
    catalog.load_data(data_path)
    
    nlp = NLPService.get_instance()
    
    # 50 Test Phrases - Diverse scenarios
    test_cases = [
        # === NECESIDADES BÁSICAS (10) ===
        {"input": "tengo hambre", "category": "Necesidades Básicas"},
        {"input": "quiero agua", "category": "Necesidades Básicas"},
        {"input": "necesito ir al baño", "category": "Necesidades Básicas"},
        {"input": "tengo sed", "category": "Necesidades Básicas"},
        {"input": "quiero dormir", "category": "Necesidades Básicas"},
        {"input": "necesito ayuda", "category": "Necesidades Básicas"},
        {"input": "me duele la cabeza", "category": "Necesidades Básicas"},
        {"input": "tengo frío", "category": "Necesidades Básicas"},
        {"input": "tengo calor", "category": "Necesidades Básicas"},
        {"input": "quiero comer", "category": "Necesidades Básicas"},
        
        # === EMOCIONES Y SENTIMIENTOS (10) ===
        {"input": "estoy contento", "category": "Emociones"},
        {"input": "me siento mal", "category": "Emociones"},
        {"input": "estoy cansado", "category": "Emociones"},
        {"input": "tengo miedo", "category": "Emociones"},
        {"input": "estoy enfadado", "category": "Emociones"},
        {"input": "me gusta jugar", "category": "Emociones"},
        {"input": "no me gusta", "category": "Emociones"},
        {"input": "estoy aburrido", "category": "Emociones"},
        {"input": "me siento bien", "category": "Emociones"},
        {"input": "estoy nervioso", "category": "Emociones"},
        
        # === PREGUNTAS (10) ===
        {"input": "donde esta mama", "category": "Preguntas"},
        {"input": "que quieres", "category": "Preguntas"},
        {"input": "cuando vamos", "category": "Preguntas"},
        {"input": "quien es", "category": "Preguntas"},
        {"input": "como estas", "category": "Preguntas"},
        {"input": "cuanto cuesta", "category": "Preguntas"},
        {"input": "donde vives", "category": "Preguntas"},
        {"input": "que hora es", "category": "Preguntas"},
        {"input": "por que lloras", "category": "Preguntas"},
        {"input": "que haces", "category": "Preguntas"},
        
        # === COMANDOS Y PETICIONES (10) ===
        {"input": "dame la pelota", "category": "Comandos"},
        {"input": "abre la puerta", "category": "Comandos"},
        {"input": "ven aqui", "category": "Comandos"},
        {"input": "mira esto", "category": "Comandos"},
        {"input": "espera un momento", "category": "Comandos"},
        {"input": "ayudame por favor", "category": "Comandos"},
        {"input": "cierra la ventana", "category": "Comandos"},
        {"input": "sientate aqui", "category": "Comandos"},
        {"input": "escucha esto", "category": "Comandos"},
        {"input": "trae mi mochila", "category": "Comandos"},
        
        # === ACTIVIDADES DIARIAS (10) ===
        {"input": "voy a la escuela", "category": "Actividades"},
        {"input": "quiero ver la tele", "category": "Actividades"},
        {"input": "me lavo las manos", "category": "Actividades"},
        {"input": "voy a cepillarme los dientes", "category": "Actividades"},
        {"input": "quiero jugar con mis amigos", "category": "Actividades"},
        {"input": "necesito hacer los deberes", "category": "Actividades"},
        {"input": "voy a vestirme", "category": "Actividades"},
        {"input": "quiero salir al parque", "category": "Actividades"},
        {"input": "me voy a duchar", "category": "Actividades"},
        {"input": "voy a desayunar", "category": "Actividades"},
        
        # === GRAMÁTICA COMPLEJA Y CASOS ESPECIALES (10) ===
        {"input": "mi perro es grande", "category": "Gramática Compleja"},
        {"input": "la casa de mi abuela", "category": "Gramática Compleja"},
        {"input": "quiero el libro rojo", "category": "Gramática Compleja"},
        {"input": "no quiero ir", "category": "Gramática Compleja"},
        {"input": "me gusta mucho", "category": "Gramática Compleja"},
        {"input": "voy a comprar pan", "category": "Gramática Compleja"},
        {"input": "tengo dos hermanos", "category": "Gramática Compleja"},
        {"input": "mi mama esta trabajando", "category": "Gramática Compleja"},
        {"input": "quiero jugar con la pelota", "category": "Gramática Compleja"},
        {"input": "el gato esta durmiendo", "category": "Gramática Compleja"},
    ]
    
    print(f"\n{'='*80}")
    print(f"EJECUTANDO TEST DE 50 FRASES")
    print(f"{'='*80}\n")
    
    passed = 0
    failed = 0
    results_by_category = {}
    
    for i, case in enumerate(test_cases, 1):
        text = case["input"]
        category = case["category"]
        
        # Initialize category stats
        if category not in results_by_category:
            results_by_category[category] = {"passed": 0, "failed": 0, "total": 0}
        
        # Call the router directly
        request = TextRequest(text=text)
        response = await text_to_pictos(request)
        
        result_labels = [p.labels['es'].lower() for p in response["pictograms"]]
        
        # Check if we got any results
        if len(result_labels) > 0:
            status = "✅ PASS"
            passed += 1
            results_by_category[category]["passed"] += 1
            color = "\033[92m"  # Green
        else:
            status = "❌ FAIL"
            failed += 1
            results_by_category[category]["failed"] += 1
            color = "\033[91m"  # Red
        
        results_by_category[category]["total"] += 1
        
        reset = "\033[0m"
        print(f"{color}{status}{reset} [{i:2d}/50] [{category:20s}] '{text}'")
        print(f"      → Pictogramas: {', '.join(result_labels) if result_labels else '(ninguno)'}")
        print()
    
    # Summary
    print(f"\n{'='*80}")
    print(f"RESUMEN POR CATEGORÍA")
    print(f"{'='*80}\n")
    
    for category in sorted(results_by_category.keys()):
        stats = results_by_category[category]
        percentage = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"{category:25s}: {stats['passed']:2d}/{stats['total']:2d} ({percentage:5.1f}%)")
    
    print(f"\n{'='*80}")
    print(f"RESUMEN GENERAL")
    print(f"{'='*80}\n")
    
    total_percentage = (passed / 50 * 100) if 50 > 0 else 0
    print(f"✅ Frases exitosas: {passed}/50 ({total_percentage:.1f}%)")
    print(f"❌ Frases fallidas:  {failed}/50 ({(100-total_percentage):.1f}%)")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(run_50_phrase_test())
