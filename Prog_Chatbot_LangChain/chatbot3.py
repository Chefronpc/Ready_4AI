"""
Moduł chatbota wykorzystujący LangChain do prowadzenia konwersacji z użytkownikiem.

Ten moduł implementuje prostego chatbota z pamięcią kontekstową, wykorzystującego
model językowy poprzez LangChain. Chatbot zachowuje historię konwersacji dla
różnych sesji i odpowiada w humorystycznym stylu.

Główne komponenty:
- ChatHistory: Zarządza historią konwersacji dla różnych sesji
- initialize_model: Konfiguruje model językowy i integruje go z historią
- chat_loop: Obsługuje interakcję z użytkownikiem
- main: Koordynuje działanie całego programu

Użycie:
    python chatbotai_part.py
"""
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
    """Zarządza historią konwersacji dla różnych sesji.
    
    Klasa odpowiedzialna za przechowywanie i zarządzanie historiami konwersacji
    dla różnych sesji czatu. Każda sesja ma własną historię, która jest tworzona
    przy pierwszym użyciu.
    
    Attributes:
        store (Dict[str, InMemoryChatMessageHistory]): Słownik przechowujący
            historie konwersacji dla poszczególnych sesji.
    """
 
    def __init__(self):
        self.store: Dict[str, InMemoryChatMessageHistory] = {}
    
    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """Pobiera lub tworzy nową historię dla danej sesji.
        
        Args:
            session_id (str): Identyfikator sesji, dla której pobierana jest historia.
            
        Returns:
            InMemoryChatMessageHistory: Historia konwersacji dla danej sesji.
            Jeśli sesja nie istnieje, tworzona jest nowa historia.
        """
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
            self.store[session_id].add_message(SystemMessage(SYSTEM_MESSAGE))
        return self.store[session_id]


def initialize_model(chat_history: ChatHistory) -> RunnableWithMessageHistory:
    """Inicjalizuje model chatbota z historią.
    
    Funkcja konfiguruje model językowy i integruje go z systemem zarządzania
    historią konwersacji. Wykorzystuje zmienne środowiskowe do konfiguracji
    i obsługuje podstawowe błędy inicjalizacji.
    
    Args:
        chat_history (ChatHistory): Instancja klasy zarządzającej historią konwersacji.
        
    Returns:
        RunnableWithMessageHistory: Skonfigurowany model z obsługą historii.
        
    Raises:
        ValueError: Gdy chat_history jest None.
        RuntimeError: Gdy nie udało się zainicjalizować modelu lub wystąpił inny błąd.
    """
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
    """Główna pętla chatbota obsługująca interakcję z użytkownikiem.
    
    Funkcja obsługuje ciągłą interakcję z użytkownikiem, przetwarzając wprowadzane
    komendy i generując odpowiedzi za pomocą modelu. Obsługuje również sytuacje
    wyjątkowe i umożliwia eleganckie zakończenie programu.
    
    Args:
        model_with_history (RunnableWithMessageHistory): Skonfigurowany model z historią.
        config (dict): Konfiguracja sesji chatbota.
        
    Note:
        Funkcja działa w nieskończonej pętli, dopóki użytkownik nie wyda komendy
        wyjścia ('quit', 'exit', 'q') lub nie przerwie programu (Ctrl+C).
    """
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
    """Główna funkcja programu.
    
    Inicjalizuje i uruchamia chatbota, obsługując wszystkie potrzebne komponenty
    i zarządzając ich cyklem życia. Zapewnia obsługę błędów na najwyższym poziomie.
    
    Returns:
        int: Kod wyjścia programu (0 dla sukcesu, 1 dla błędu).
        
    Note:
        Funkcja obsługuje różne poziomy błędów:
        - Błędy inicjalizacji modelu
        - Błędy podczas działania chatbota
        - Nieoczekiwane błędy krytyczne
    """
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