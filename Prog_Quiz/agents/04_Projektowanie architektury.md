[[_Projektowanie aplikacji quizu w Pythonie]]
# Projekt aplikacji quizu w Pythonie

## 1) Diagram zależności modułów (blokowy / UML)

```
+------------+            +----------------+             +---------------+
|  UI_Text   |  <----->   |  Quiz_Logic    |   <----->   | AI_Generator  |
| (console)  |            | (game control) |             | (call model)  |
+-----+------+            +-------+--------+             +-------+-------+
      ^                            |                               ^
      |                            |                               |
      |                            v                               |
      |                   +--------+----------+                    |
      |                   |  Result_Processor |                    |
      |                   |  (report builder) |                    |
      |                   +--------+----------+                    |
      |                            |                               |
      +----------------------------+-------------------------------+
                                   |
                                   ^
                             +-----+------+
                             | Config /   |
                             | Constants  |
                             +------------+
```

Legenda:
- Strzałki pokazują przepływ wywołań i danych.
- `UI_Text` komunikuje się dwustronnie z `Quiz_Logic`.
- `Quiz_Logic` pobiera pytania z `AI_Generator`.
- `Result_Processor` przetwarza wyniki i zwraca raport do `UI_Text`.
- `Config / Constants` jest dostępny dla wszystkich modułów.

---

## 2) Interfejsy funkcji (Python) i kontrakty

### `config/constants.py`

```python
MIN_QUESTIONS: int = 1
MAX_QUESTIONS: int = 50

AI_API_URL: str = "https://api.example.com/v1/generate"
AI_API_KEY: str | None = None  # np. z os.environ

EXPECTED_QUESTION_KEYS = ("question", "a", "b", "c", "d", "correct")
```

### `ai_generator.py`

```python
from typing import List, TypedDict

class QuizItem(TypedDict):
    question: str
    a: str
    b: str
    c: str
    d: str
    correct: str  # 'a'|'b'|'c'|'d'

class AIServiceError(Exception): pass
class InvalidModelResponseError(Exception): pass

def generate_quiz(topic: str, n_questions: int) -> List[QuizItem]:
    """
    Wywołuje model AI i zwraca listę pytań.

    Walidacja:
    - topic nie może być pusty
    - n_questions w MIN_QUESTIONS..MAX_QUESTIONS
    - każdy QuizItem ma wszystkie klucze EXPECTED_QUESTION_KEYS
    - 'correct' ∈ {'a','b','c','d'}

    Wyjątki:
    - AIServiceError dla błędów komunikacji
    - InvalidModelResponseError dla niepoprawnego formatu odpowiedzi
    """
    ...
```

### `quiz_logic.py`

```python
from typing import Iterable, List, Tuple, Dict

def run_quiz(quiz_items: Iterable[Dict], ui) -> Tuple[int, int, List[Dict]]:
    """
    Przeprowadza quiz.

    ui: obiekt UI_Text implementujący:
        - display_question(index:int, question:str, choices:dict)
        - get_user_choice() -> str
        - show_message(msg: str)

    Zwraca:
    - liczba_poprawnych: int
    - liczba_blednych: int
    - lista_blednych: [{"index": idx, "user": 'a'..'d', "correct": 'a'..'d', "question_item": QuizItem}]
    """
    ...
```

### `ui_text.py`

```python
class UITextInterface:
    def display_welcome(self) -> None: ...
    def ask_topic(self) -> str: ...
    def ask_number_of_questions(self, min_q:int, max_q:int) -> int: ...
    def display_question(self, index:int, question:str, choices:dict) -> None: ...
    def get_user_choice(self) -> str: ...
    def display_final_report(self, report_text: str) -> None: ...
```

### `result_processor.py`

```python
from typing import List, Dict

def build_report(total: int, correct: int, wrong_items: List[Dict]) -> str:
    """
    Tworzy raport tekstowy:
    - total: liczba pytań
    - correct: liczba poprawnych
    - wrong_items: lista błędnych pytań

    Zwraca sformatowany string (multi-line)
    """
    ...
```

---

## 3) Struktura katalogów

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

---

## 4) Kolejność implementacji

1. Repo + środowisko (wirtualne, linter, pre-commit)
2. `config/constants.py`
3. `UI_Text` (prosty interfejs konsolowy)(testy jednostkowe)
4. `AI_Generator` (mock)(testy jednostkowe)
5. `Quiz_Logic` (testy jednostkowe)
6. `Result_Processor` (testy jednostkowe)
7. `AI_Generator` (real, integracja z API)
8. E2E testy i dopracowanie przepływu

---

## 5) Przykładowy przepływ `main.py`

```python
def main():
    ui = ConsoleUI()
    ui.display_welcome()

    topic = ui.ask_topic()
    n = ui.ask_number_of_questions(MIN_QUESTIONS, MAX_QUESTIONS)

    quiz_items = generate_quiz(topic, n)  # mock lub real
    correct, wrong_count, wrong_items = run_quiz(quiz_items, ui)

    report = build_report(total=n, correct=correct, wrong_items=wrong_items)
    ui.display_final_report(report)
```

---

## 6) Testy i walidacja

- Jednostkowe: `UI_Text`, `AI_Generator`, `quiz_logic`, `result_processor`, stuby/mock UI i AI
- Integracyjne: przepływ quizu z mockiem AI
- E2E: pełny przebieg z prawdziwym AI
- Walidacja AI: struktura pytań, brak duplikatów, poprawna wartość `correct`

---

## 7) Dodatkowe wytyczne

- Timeouty: 10–15s dla requestów do AI
- Retry: 2–3 próby z rosnącymi opóźnieniami
- Przycinanie długich tematów
- Sanity checks: białe znaki, brak HTML, poprawne litery odpowiedzi
- Bezpieczne logowanie: nie ujawniać API_KEY

