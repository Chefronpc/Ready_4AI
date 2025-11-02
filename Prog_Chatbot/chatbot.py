import os
import json
import requests
    

# KONFIGURACJA API
# ==========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/responses"
MODEL_NAME = "gpt-4.1"

if not OPENAI_API_KEY:
    raise EnvironmentError("Brak ustawionej zmiennej środowiskowej OPENAI_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}


def send_prompt(prompt: str, prev_resp_id: str = None) -> dict:
    payload = {
        "model": MODEL_NAME,
        "input": prompt,
        "previous_response_id": prev_resp_id 
    }
    response = requests.post(OPENAI_API_URL, headers=HEADERS, json=payload)
    return {"msg": response.json()['output'][0]['content'][0]['text'], "conv_id": response.json()['id']}


def get_cli_question() -> str:
    return input("\n> ").strip()
    

def main():

    prev_resp_id = None
    print("    Chatbot: Napisz cokolwiek :)")

    while True:
        my_msg = get_cli_question()
        if my_msg == "quit":
            break
        rsp_msg = send_prompt(my_msg, prev_resp_id=prev_resp_id)
        prev_resp_id = rsp_msg["conv_id"]
        print(f"\n{rsp_msg["msg"]}")


if __name__ == "__main__":
    main()

