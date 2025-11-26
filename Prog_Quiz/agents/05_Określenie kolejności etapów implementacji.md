---
tags:
  - metodyka/
---
[[_Projektowanie aplikacji quizu w Pythonie]]
## Krok 0 — Repozytorium i środowisko

**Dlaczego:** uporządkowane repo i środowisko to fundament dla kolejnych modułów i testów.

**Co zrobić:**

- Utwórz repozytorium git.
- Struktura katalogów:

```
quiz_project/
├─ quiz/
│  ├─ __init__.py
│  ├─ ai_generator.py
│  ├─ quiz_logic.py
│  ├─ ui_text.py
│  ├─ result_processor.py
│  └─ config.py
├─ tests/
│  ├─ test_ai_generator.py
│  ├─ test_quiz_logic.py
│  ├─ test_ui_text.py
│  └─ test_result_processor.py
├─ README.md
├─ pyproject.toml
└─ requirements.txt
```

- Zainicjalizuj wirtualne środowisko (venv/virtualenv), linter (flake8/ruff) i opcjonalnie pre-commit.
- Sprawdź, że `python -m pytest` uruchamia puste testy (sanity check).

---

## Krok 1 — `config/constants.py`

**Dlaczego:** wszystkie moduły będą odwoływać się do stałych i ustawień API. Najprostszy moduł niezależny od innych.

**Co zrobić:**

- Zaimplementuj stałe:

```python
MIN_QUESTIONS: int = 1
MAX_QUESTIONS: int = 50

AI_API_URL: str = "https://api.example.com/v1/generate"
AI_API_KEY: str | None = None

EXPECTED_QUESTION_KEYS = ("question", "a", "b", "c", "d", "correct")
```

- Dodaj walidację konfiguracji (np. brak `API_KEY` → warning).
- Możesz przygotować loader środowiska (`os.getenv`) dla kluczy i endpointów.

---

## Krok 2 — `ui_text.py` (prosty interfejs konsolowy)

**Dlaczego:** `quiz_logic` i testy jednostkowe potrzebują interfejsu do komunikacji z użytkownikiem. Prosty UI pozwala szybciej testować logikę.

**Co zrobić:**

- Implementacja metod `UITextInterface`:

```python
class UITextInterface:
    def display_welcome(self) -> None: ...
    def ask_topic(self) -> str: ...
    def ask_number_of_questions(self, min_q:int, max_q:int) -> int: ...
    def display_question(self, index:int, question:str, choices:dict) -> None: ...
    def get_user_choice(self) -> str: ...
    def display_final_report(self, report_text: str) -> None: ...
```

- Walidacja wejścia użytkownika (np. pętla do momentu podania poprawnej liczby pytań lub wyboru).
- Testy manualne: sprawdzenie wyświetlania i pobierania danych.

**Uwaga:** UI nie zna szczegółów quizu — tylko kontrakt do `quiz_logic`.

---

## Krok 3 — `ai_generator.py` (mock)

**Dlaczego:** szybkie testy logiki bez zależności od API. Mock zwraca strukturę zgodną z kontraktem `QuizItem`.

**Co zrobić:**

- Implementacja funkcji `generate_quiz(topic, n_questions)`:

```python
def generate_quiz(topic: str, n_questions: int) -> List[QuizItem]:
    """Generuje syntetyczne pytania (mock)."""
    ...
```

- Walidacja:
    - `topic` nie pusty
    - `n_questions` w zakresie MIN/MAX
    - każdy QuizItem ma wszystkie klucze `EXPECTED_QUESTION_KEYS`
- Przygotuj szkielet dla implementacji realnej (`generate_quiz_real`) — nieaktywny do czasu konfiguracji API.

---

## Krok 4 — `quiz_logic.py` (z mockiem AI)

**Dlaczego:** logika quizu jest sercem aplikacji. Można testować offline, z mockiem pytań i stubem UI.

**Co zrobić:**

- Implementacja funkcji `run_quiz`:

```python
def run_quiz(quiz_items: Iterable[Dict], ui) -> Tuple[int, int, List[Dict]]:
    ...
```

- Obsługa liczenia poprawnych/niepoprawnych, lista błędnych pytań.
- Wstrzykiwanie UI (`UITextInterface`), żeby logika była niezależna od konsoli.
- Testy jednostkowe: symulacja odpowiedzi użytkownika, sprawdzenie wyników.

---

## Krok 5 — `result_processor.py`

**Dlaczego:** raport to osobny moduł, łatwo testowalny i niezależny.

**Co zrobić:**

- Implementacja funkcji `build_report`:

```python
def build_report(total: int, correct: int, wrong_items: List[Dict]) -> str:
    ...
```

- Testy jednostkowe: porównanie wynikowego stringa z oczekiwanym.

---

## Krok 6 — Integracja z realnym `ai_generator` (API)

**Dlaczego:** po działającej logice i mocku można podłączyć prawdziwe generowanie pytań.

**Co zrobić:**

- Implementacja wywołań API (timeout, retry, nagłówki z `API_KEY`).
- Wymuszenie struktury JSON w promptcie i walidacja odpowiedzi.
- Obsługa błędów modelu → fallback do lokalnego generatora lub informacja dla użytkownika.
- Kontrola kosztów: batchowanie pytań, logowanie błędów bez ujawniania klucza.

---

## Krok 7 — Testy end-to-end i dopracowanie przepływu

**Co zrobić:**

- Połącz wszystkie moduły:  
`UI_Text` → pyta o temat/liczbę → `AI_Generator` → `Quiz_Logic` → `Result_Processor` → `UI_Text`.
- Testy E2E:
    - manualny przebieg quizu
    - automatyczny scenariusz z mockami
- Obsługa wyjątków w `main()`:
    - `AIServiceError`, `InvalidModelResponseError`, `KeyboardInterrupt`
