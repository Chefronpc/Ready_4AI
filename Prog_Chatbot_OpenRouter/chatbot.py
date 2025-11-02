import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv("OPENROUTER_API_KEY")

# KONFIGURACJA API
# ==========================
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= apikey,
)

MODEL_NAME = "minimax/minimax-m2:free"


def send_prompt(prompt: str, prev_resp_id: str = None) -> dict:
    completions = client.chat.completions.create(
        model= MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completions.choices[0].message.content #, response.id


def get_cli_question() -> str:
    return input("\n> ").strip()
    

def main():

    prev_resp_id = None
    print("    Chatbot: Napisz cokolwiek :)")

    while True:
        my_msg = get_cli_question()
        if my_msg == "quit":
            break
        #prev_resp_id,
        respones_text = send_prompt(my_msg) #, prev_resp_id=prev_resp_id)
        print(f"\n{respones_text}")


if __name__ == "__main__":
    main()

