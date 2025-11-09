
Wprowadzone następujące zmiany w strukturze kodu:

    Dodano klasę ChatHistory:

    Wydzielono zarządzanie historią do osobnej klasy
    Dodano typowanie dla lepszej czytelności
    Zaimplementowano metodę get_session_history
    Wydzielono inicjalizację modelu:

    Utworzono funkcję initialize_model
    Funkcja zwraca skonfigurowany model
    Wydzielono główną pętlę chatbota:

    Utworzono funkcję chat_loop
    Wydzielono logikę interakcji z użytkownikiem
    Dodano główną funkcję main():

    Zorganizowano inicjalizację komponentów
    Dodano prawidłowe kody zwrotne (0 dla sukcesu, 1 dla błędu)
    Dodano zabezpieczenie wykonania kodu:

    Dodano konstrukcję if __name__ == "__main__":
    Wywołanie głównej funkcji main()
    Uporządkowano importy:

    Dodano import typing.Dict
    Uproszczono import SystemMessage

    Te zmiany znacznie poprawiły strukturę kodu, czyniąc go bardziej modułowym i łatwiejszym w utrzymaniu.
    Każda funkcja ma teraz pojedynczą odpowiedzialność, a kod jest lepiej zorganizowany.


Zmiany funkcjonalności (Poprawa interakcji z uzytkownikiem i czytelnośc kodu):

    Ulepszono formatowanie wyjścia:
        Zmieniono format wyświetlania odpowiedzi asystenta z konkatenacji na f-string
        Dodano lepsze odstępy w komunikatach, metodę strip() do czyszczenia wejścia, walidację pustego wejścia
        Ujednolicono styl wyświetlania komunikatów
        Rozszerzono listę komend wyjścia ('quit', 'exit', 'q')

    Usprawnienia w zarządzaniu konfiguracją:
        Wykorzystanie stałej DEFAULT_CONFIG zamiast bezpośredniego definiowania konfiguracji
        Wykorzystanie stałej SYSTEM_MESSAGE w klasie ChatHistory
        Wykorzystanie MODEL_CONFIG w funkcji initialize_model

    Dodano lepsze komunikaty dla użytkownika:
        Informacja o uruchomieniu chatbota
        Informacja o dostępnych komendach
        Czytelniejsze komunikaty błędów
        Komunikat pożegnalny przy wyjściu

    Ogólne usprawnienia:
        Dodano docstring z opisem modułu
        Uporządkowano importy
        Usunięto nieużywane importy (HumanMessage, AIMessage)
        Dodano typ Optional do importów (przygotowanie pod przyszłe rozszerzenia)


Zmiany w dokumentacji:

    Rozszerzono dokumentację modułu:
        Dodano szczegółowy opis funkcjonalności,instrukcję użycia
        Wymieniono główne komponenty, ogólną strukturę programu

    Rozbudowano dokumentację klasy ChatHistory:
        Dodano szczegółowy opis klasy, dokumentację metod, informacje o typach danych
        Opisano atrybuty klasy
        
    Rozszerzono dokumentację funkcji initialize_model:
        Dodano szczegółowy opis działania, informację o zwracanej wartości
        Opisano parametry wejściowe, możliwe wyjątki

    Rozbudowano dokumentację funkcji chat_loop:
        Dodano szczegółowy opis interakcji, uwagi o działaniu pętli
        Opisano parametry funkcji, obsługę komend

    Rozszerzono dokumentację funkcji main:
        Dodano szczegółowy opis działania, informacje o obsłudze błędów
        Opisano wartości zwracane, kody wyjścia

    Dokumentacja jest teraz:
        Bardziej szczegółowa, zorganizowana
        Zgodna z konwencjami Python (docstrings)
        Zawiera informacje o typach, błędów, przykłady użycia