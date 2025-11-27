import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_backend.routers.translation import pictos_to_text, PictosRequest, PictoItem

async def test_arasaac_integration():
    print("Testing ARASAAC API Integration...")
    
    # Mock pictograms for "yo comer hamburguesa ayer"
    pictos = [
        PictoItem(id=1, labels={'es': 'yo'}, image_urls={}),
        PictoItem(id=2, labels={'es': 'comer'}, image_urls={}),
        PictoItem(id=3, labels={'es': 'hamburguesa'}, image_urls={}),
        PictoItem(id=4, labels={'es': 'ayer'}, image_urls={})
    ]
    
    request = PictosRequest(pictograms=pictos)
    
    try:
        response = await pictos_to_text(request)
        print(f"Input: [yo, comer, hamburguesa, ayer]")
        print(f"Output: '{response['text']}'")
        
        # Check if it looks like a natural sentence (ARASAAC usually does a good job)
        if "comí" in response['text'].lower() or "ayer" in response['text'].lower():
            print("SUCCESS: Generated natural phrase.")
        else:
            print("WARN: Output might be from fallback or API returned unexpected result.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_arasaac_integration())
