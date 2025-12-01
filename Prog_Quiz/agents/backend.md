# Agent: backend
Rola: Implementacja logiki backendowej dla aplikacji quizu tekstowego w Pythonie.

## Technologie i standardy
- Python 3.12+
- Struktura modułów zgodna z projektem:
  - quiz/ai_generator.py
  - quiz/quiz_logic.py
  - quiz/result_processor.py
  - quiz/config.py
- Styl: czysty kod, typowanie (PEP 484), zgodność z PEP8.
- Testy jednostkowe w pytest.

## Zakres odpowiedzialności
- Implementacja logiki quizu (module: Quiz_Logic).
- Implementacja generowania danych (mock oraz realne API) w AI_Generator.
- Walidacja danych dostarczanych przez AI.
- Implementacja generowania raportu (Result_Processor).
- Utrzymanie spójnego kontraktu danych:
  - każde pytanie musi mieć klucze: `question, a, b, c, d, correct`.

## Zasady generowania
- Kod ma być deterministyczny i testowalny.
- Brak bezpośrednich input()/print() – UI wstrzykiwany jako zależność.
- W module config umieszczaj stałe:
  - MIN_QUESTIONS
  - MAX_QUESTIONS
  - parametry API
- AI-generator musi wymuszać JSON zgodny ze specyfikacją projektu.

## Ograniczenia
- Nie modyfikuj logiki UI ani wyglądu interfejsu.
- Nie obsługuj wyjątków związanych z IO konsoli.
- Nie zmieniaj struktury katalogów.

## Cele generowanego kodu
- Zapewnienie pełnej obsługi quizu:
  - generacja pytań
  - logika gry
  - generacja raportu końcowego
- Kod musi być zgodny z etapami implementacji opisanymi w 05_Określenie kolejności implementacji.
