import requests

# Replace this with a real set ID for testing
set_id = 12345  # <-- put a valid tcgId here

url = f"https://infinite-api.tcgplayer.com/priceguide/set/24073/cards/?rows=5000&productTypeID=1"

try:
    response = requests.get(url)
    response.raise_for_status()  # Will raise an error if status is 4xx or 5xx

    if response.text.strip():
        print("Response JSON:")
        print(response.json())  # Pretty raw, can wrap in json.dumps if needed
    else:
        print("Empty response from API.")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")

except Exception as e:
    print(f"General error: {e}")
