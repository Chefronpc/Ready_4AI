from json import load
from typing import Dict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()
store = {}

class ChatHistory:
    """Zarządza historią konwersacji dla różnych sesji."""
    def __init__(self):
        self.store: Dict[str, InMemoryChatMessageHistory] = {}
    
    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """Pobiera lub tworzy nową historię dla danej sesji."""
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
            self.store[session_id].add_message(SystemMessage("Odpowiadaj z humorem"))
        return self.store[session_id]


def initialize_model(chat_history: ChatHistory) -> RunnableWithMessageHistory:
    """Inicjalizuje model chatbota z historią."""
    load_dotenv()
    model = init_chat_model(model="gpt-4.1-nano", model_provider="openai", verbose=True)
    return RunnableWithMessageHistory(
        model,
        chat_history.get_session_history
    )


def chat_loop(model_with_history: RunnableWithMessageHistory, config: dict) -> None:
    """Główna pętla chatbota obsługująca interakcję z użytkownikiem."""
    while True:
        user_input = input("Ty: ")
        response = model_with_history.invoke(user_input, config)
        print("Asystent: " + response.content)


def main():
    """Główna funkcja programu."""
    config = {"configurable": {"session_id": "Ready4AI"}}
    chat_history = ChatHistory()
    model_with_history = initialize_model(chat_history)
    chat_loop(model_with_history, config)


if __name__ == "__main__":
    main()