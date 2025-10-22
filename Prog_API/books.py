import requests
import json

url = "https://wolnelektury.pl/api/audiobooks/"

#headers = {"Authorization": "Bearer hmeuabUApC3z5efKEaN-"}

response = requests.get(f"{url}") #, headers=headers)

if response.status_code == 200:
    data = response.json()
    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
else:
    print(f"Error: {response.status_code}")

