import requests

url = "https://the-one-api.dev/v2"

headers = {"Authorization": "Bearer hmeuabUApC3z5efKEaN-"}

response = requests.get(f"{url}/movie", headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")

