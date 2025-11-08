
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