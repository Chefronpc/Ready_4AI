import os
from openai import OpenAI, APIError
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


def get_chat_response(messages: list) -> str | None:
    try:
        completions = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        return completions.choices[0].message.content
    except APIError as e:
        print(f"Błąd API: {e}")
        return None
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
        return None


def get_cli_question() -> str:
    return input("\n> ").strip()


def main():
    print("    Chatbot: Napisz cokolwiek :) Aby zakończyć, wpisz 'quit'.")
    conversation_history = []

    while True:
        my_msg = get_cli_question()
        if my_msg == "quit":
            break

        conversation_history.append({"role": "user", "content": my_msg})

        response_text = get_chat_response(conversation_history)
        if response_text:
            print(f"\nChatbot: {response_text}")
            conversation_history.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main()
