**Projekt: Prog_Quiz**

- Krótkie narzędzie do generowania i przeprowadzania quizów z użyciem usługi AI.

**Skrót zmian**
- `config.py`: ładowanie ustawień z `.env` (`API_URL`, `API_KEY`).
- `.env`: szablon pliku środowiskowego (do uzupełnienia lokalnie).
- `ai_generator.py`: typy i szkielet funkcji `generate_quiz` (do implementacji).
- `quiz_logic.py`: szkielet `run_quiz` (do implementacji).
- `result_procesor.py`: szkielet `build_report` (do implementacji).
- `ui_text.py`: definicja interfejsu `UITextInterface` (implementacja UI wymagana).

**Konfiguracja**
- Uzupełnij `Prog_Quiz/.env` przed uruchomieniem aplikacji.

**Dalsze kroki (skrótowo)**
- Implementować kolejne moduły (generator, logikę quizu, UI, formatowanie raportu) i dodać testy jednostkowe.
