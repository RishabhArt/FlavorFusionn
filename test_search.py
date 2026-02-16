import requests
import json

# Test the search API
url = "http://localhost:5000/api/search"
headers = {"Content-Type": "application/json"}

# Test with common ingredients
data = {
    "ingredients": ["chicken", "rice"],
    "dietary": "",
    "difficulty": "",
    "max_time": 999,
    "servings": 0
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Results found: {len(result.get('results', []))}")
        if result.get('results'):
            for i, recipe in enumerate(result['results'][:3]):
                print(f"{i+1}. {recipe['name']} - {recipe.get('match_score', 'N/A')}% match")
    
except Exception as e:
    print(f"Error: {e}")
