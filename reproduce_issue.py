import requests
import json

def main():
    url = "http://127.0.0.1:8001/api/v1/pictos-to-text"
    
    payload = {
        "pictograms": [
            {
                "id": 1, 
                "labels": {"es": "abuelo"}, 
                "image_urls": {}
            },
            {
                "id": 2, 
                "labels": {"es": "comer"}, 
                "image_urls": {}
            },
            {
                "id": 3, 
                "labels": {"es": "naranja"}, 
                "image_urls": {}
            }
        ]
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=2, ensure_ascii=False)
        print("Response saved to result.json")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
