import os
import json
import requests
    

# KONFIGURACJA API
# ==========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/responses"
MODEL_NAME = "gpt-4o-mini"

if not OPENAI_API_KEY:
    raise EnvironmentError("Brak ustawionej zmiennej środowiskowej OPENAI_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}


def send_prompt(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "input": prompt
    }
    response = requests.post(OPENAI_API_URL, headers=HEADERS, json=payload)
    return response.json()['output'][0]['content'][0]['text']


def question(qu_talk_all: str) -> str:
    text_in = input("\n> ")
    text_in = text_in.strip()
    print("")
    return {"all": qu_talk_all + "\n" + text_in, "last": text_in}
    

def answer( text_send: str) -> str:
    an_response = send_prompt(text_send)
    result_all = text_send + "\n" + an_response
    return {"all": result_all, "last":  an_response}


def main():

    print("    Chatbot: Napisz cokolwiek :)")
    talk_all = {"all": "", "last": ""}   # Treść konwersacji

    while True:
        talk_full = question(talk_all['all'])
        if talk_full["last"] == "quit":
            break
        talk_full = answer(talk_full["all"])
        talk_hist = talk_full["all"] + "\n" + talk_full["last"]
        talk_all = {"all": talk_hist, "last": talk_full["last"]}

        print(talk_full["last"])


if __name__ == "__main__":
    main()

