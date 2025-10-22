import requests

url = "https://jsonplaceholder.typicode.com/posts/"

while True:
    inp = input("enter -> odczyt WebSerwis\nnext -> następna funkcja\n>> ")

    if inp == "next":
        break
    elif inp == "":
        continue

    response = requests.get(f"{url}{inp}")

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}")


while True:
    in_titile  = input("Podaj tytuł: ")
    in_body    = input("Podaj treść: ")

    if in_titile == "next" or in_body == "next":
        break
    elif in_titile == "" or in_body == "":
        continue

    data = {
        "title": in_titile,
        "body": in_body,
        "userId": 1
    }

    response = requests.post(url, json=data)

    if response.status_code == 201:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}")


