import httpx
import logging

logger = logging.getLogger(__name__)

class ArasaacService:
    _instance = None
    BASE_URL = "https://api.arasaac.org/api"

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def generate_phrase(self, keywords: list[str]) -> str:
        """
        Generates a natural language phrase from a list of keywords using the ARASAAC API.
        Endpoint: GET /phrases/flex/{language}/{phrase}
        """
        if not keywords:
            return ""

        import urllib.parse
        
        # Join keywords with spaces and encode for URL
        phrase_raw = " ".join(keywords)
        phrase_encoded = urllib.parse.quote(phrase_raw)
        
        url = f"{self.BASE_URL}/phrases/flex/es/{phrase_encoded}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                
                if response.status_code != 200:
                    logger.warning(f"ARASAAC API Error {response.status_code}: {response.text}")
                    return ""
                
                data = response.json()
                
                if isinstance(data, dict):
                    if 'phrase' in data:
                        return data['phrase']
                    elif 'text' in data:
                        return data['text']
                    elif 'msg' in data:
                        return data['msg']
                
                if isinstance(data, str):
                    return data
                else:
                    logger.warning(f"Unexpected ARASAAC response format: {data}")
                    return ""
                    
        except httpx.RequestError as e:
            logger.error(f"ARASAAC API connection error: {e}")
            return ""
        except Exception as e:
            logger.error(f"ARASAAC API unexpected error: {e}")
            return ""
