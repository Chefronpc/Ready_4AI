from typing import Dict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# Stałe konfiguracyjne
DEFAULT_CONFIG = {
    "configurable": {
        "session_id": "Ready4AI"
    }
}

SYSTEM_MESSAGE = "Odpowiadaj z humorem"

MODEL_CONFIG = {
    "model": "gpt-4.1-nano",
    "model_provider": "openai",
    "verbose": True
}


class ChatHistory:
    """Zarządza historią konwersacji dla różnych sesji."""
    def __init__(self):
        self.store: Dict[str, InMemoryChatMessageHistory] = {}
    
    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """Pobiera lub tworzy nową historię dla danej sesji."""
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
            self.store[session_id].add_message(SystemMessage(SYSTEM_MESSAGE))
        return self.store[session_id]


def initialize_model(chat_history: ChatHistory) -> RunnableWithMessageHistory:
    """Inicjalizuje model chatbota z historią."""
    if not chat_history:
        raise ValueError("Brak historii czatu, wartość ""None""")

    try:
        load_dotenv()
        model = init_chat_model(**MODEL_CONFIG)
        if not model:
            raise RuntimeError("Nie udało się zainicjalizować modelu")
        
        return RunnableWithMessageHistory(
            model,
            chat_history.get_session_history
        )
    except Exception as e:
        raise RuntimeError(f"Błąd podczas inicjalizacji modelu: {e}")


def chat_loop(model_with_history: RunnableWithMessageHistory, config: dict) -> None:
    """Główna pętla chatbota obsługująca interakcję z użytkownikiem."""
    print("Chatbot został uruchomiony. Wpisz 'quit' aby zakończyć.")
    
    while True:
        try:
            user_input = input("\nTy: ").strip()
            
            if user_input.lower() in ('quit', 'exit', 'q'):
                print("Do widzenia!")
                break
                
            if not user_input:
                continue
            
            response = model_with_history.invoke(user_input, config)
            print(f"Asystent: {response.content}")
            
        except KeyboardInterrupt:
            print("\nProgram został przerwany przez użytkownika.")
            break
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
            print("Spróbuj ponownie lub wpisz 'quit' aby zakończyć.")


def main() -> int:
    """Główna funkcja programu."""
    try:
        chat_history = ChatHistory()
        try:
            model_with_history = initialize_model(chat_history)
        except RuntimeError as e:
            print(f"Błąd inicjalizacji modelu: {e}")
            return 1
        except Exception as e:
            print(f"Nieoczekiwany błąd podczas inicjalizacji: {e}")
            return 1
        
        try:
            chat_loop(model_with_history, DEFAULT_CONFIG)
        except Exception as e:
            print(f"Błąd podczas działania chatbota: {e}")
            return 1

    except Exception as e:
        print(f"Krytyczny błąd: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    main()