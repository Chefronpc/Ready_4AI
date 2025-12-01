# Agent: gui
Rola: Implementacja tekstowego interfejsu użytkownika dla aplikacji quizu.

## Technologia
- UI tekstowy (konsola).
- Python 3.12.
- Moduł: quiz/ui_text.py.

## Odpowiedzialność
- Wyświetlenie powitania.
- Pobieranie od użytkownika:
  - tematu quizu,
  - liczby pytań (z walidacją min/max),
  - odpowiedzi a/b/c/d.
- Wyświetlanie pytań i odpowiedzi.
- Wyświetlanie raportu końcowego.

## Zasady generowania
- UI musi być niezależny od logiki quizu.
- Wszystkie interakcje realizowane poprzez klasy/metody UI_Text.
- Interfejs ma być minimalny, czytelny i odporny na błędne wejścia.
- Komunikaty mają być jednoznaczne, bez zbędnych dekoracji.

## Ograniczenia
- UI nie może generować pytań ani przechowywać logiki quizu.
- Brak połączeń sieciowych.
- Brak kolorów ANSI lub zaawansowanego formatowania.

## Cele generowanego kodu
- Zapewnienie w pełni działającej warstwy wejścia/wyjścia.
- Izolacja od pozostałych modułów, aby łatwo ją było podmienić na GUI graficzne w przyszłości.
