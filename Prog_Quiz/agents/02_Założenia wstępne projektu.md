[[_Projektowanie aplikacji quizu w Pythonie]]
#### Zadanie: Stworzyć aplikację quizu tematycznego
##### Wymagania funkcjonalne:
- Generowanie pytań i odpowiedzi przez model AI
- Pytanie użytkownika o tematykę oraz ilość pytań w quizie
- Do każdego pytania powinny być cztery możliwe odpowiedzi, z których poprawna jest tylko 1
- Po udzieleniu odpowiedzi na wszystkie pytania, wyświetl wynik (liczba poprawnych i niepoprawnych odpowiedzi)
- Wyświetl poprawne odpowiedzi na te pytania, gdzie została udzielona błędna odpowiedź
##### Wymagania niefunkcjonalne:
- Zdefiniowanie stałej minimalnej i maksymalnej liczby pytań możliwych do wygenerowania.
- Aplikacja ma działać w trybie tekstowym w konsoli


## Klasyfikacja wymagań

| Wymaganie                                                                                                        | Typ                 | Uzasadnienie                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Generowanie pytań i odpowiedzi przez model AI**                                                                | **Funkcjonalne**    | To główna funkcja systemu – generowanie zawartości quizu.                                                                          |
| **Pytanie użytkownika o tematykę oraz ilość pytań w quizie**                                                     | **Funkcjonalne**    | System wykonuje konkretną akcję: pobranie danych wejściowych od użytkownika.                                                       |
| **Do każdego pytania powinny być cztery możliwe odpowiedzi, z których poprawna jest tylko jedna**                | **Funkcjonalne**    | Określa sposób generowania i walidacji danych – to logiczna funkcjonalność systemu.                                                |
| **Po udzieleniu odpowiedzi na wszystkie pytania, wyświetl wynik (liczba poprawnych i niepoprawnych odpowiedzi)** | **Funkcjonalne**    | To konkretne działanie aplikacji po zakończeniu quizu.                                                                             |
| **Wyświetl poprawne odpowiedzi na te pytania, gdzie została udzielona błędna odpowiedź**                         | **Funkcjonalne**    | Kolejna akcja aplikacji po zakończeniu quizu, zależna od wcześniejszego wyniku.                                                    |
| **Zdefiniowanie stałej minimalnej i maksymalnej liczby pytań możliwych do wygenerowania**                        | **Niefunkcjonalne** | To ograniczenie parametrów działania (warunek wstępny), nie funkcja — definiuje regułę poprawności.                                |
| **Aplikacja ma działać w trybie tekstowym w konsoli**                                                            | **Niefunkcjonalne** | Dotyczy sposobu interakcji z użytkownikiem, czyli _interfejsu_, a nie logiki biznesowej. To cecha techniczna (UI/UX), nie funkcja. |
