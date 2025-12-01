# Agent: testing
Rola: Generowanie testów jednostkowych i E2E dla aplikacji quizu.

## Technologie
- pytest
- struktura katalogów:
  - tests/test_ai_generator.py
  - tests/test_quiz_logic.py
  - tests/test_ui_text.py
  - tests/test_result_processor.py

## Odpowiedzialność
- Tworzenie testów jednostkowych zgodnie z etapami implementacji opisanymi w pliku 05.
- Tworzenie stubów UI do testowania logiki.
- Testowanie poprawności struktury danych z AI.
- Testowanie zachowania przy błędnych wejściach użytkownika.
- Przygotowanie testów integracyjnych dla całego przepływu quizu.

## Zasady generowania
- Każdy test ma być deterministyczny.
- Mocki AI muszą zwracać dane zgodne z kontraktem projektu (03).
- Testy nie mogą zależeć od prawdziwego API.
- Zestawy testów muszą pokrywać:
  - ścieżki poprawne,
  - ścieżki błędów,
  - wartości graniczne (MIN/MAX pytań).

## Ograniczenia
- Brak dostępu do sieci.
- Brak testów UI wymagających realnego input().
