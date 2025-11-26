# Prog_Quiz

Interaktywna aplikacja quizowa z wykorzystaniem AI do generowania pytań.

## Opis projektu

Aplikacja tekstowa (CLI) umożliwiająca przeprowadzanie quizów na dowolny temat. Pytania są generowane dynamicznie przez model AI na podstawie wybranej przez użytkownika tematyki.

## Funkcjonalności

- **Generowanie pytań przez AI**: Automatyczne tworzenie pytań quizowych na wybrany temat
- **Interaktywny quiz**: Pytania wielokrotnego wyboru (A/B/C/D)
- **Natychmiastowy feedback**: Informacja zwrotna po każdej odpowiedzi
- **Raport końcowy**: Szczegółowe podsumowanie wyników z listą błędnych odpowiedzi
- **Walidacja danych**: Sprawdzanie poprawności wejścia użytkownika

## Struktura projektu

```
Prog_Quiz/
├── quiz.py              # Główny plik aplikacji
├── config.py            # Konfiguracja (MIN/MAX pytań, API)
├── ai_generator.py      # Generator pytań przez AI
├── quiz_logic.py        # Logika quizu (Question, Quiz)
├── ui_text.py           # Interfejs użytkownika (CLI)
├── result_procesor.py   # Generowanie raportu końcowego
├── tests/               # Testy jednostkowe
│   ├── test_ai_generator.py
│   ├── test_quiz_logic.py
│   ├── test_ui_text.py
│   └── test_result_procesor.py
├── agents/              # Dokumentacja projektowa
├── .env                 # Konfiguracja API (klucz, URL)
├── .gitignore
├── requirements.txt
└── README.md
```

## Wymagania

- Python 3.12+
- Klucz API OpenAI (lub kompatybilnego serwisu)

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki projektu

2. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

3. Skonfiguruj plik `.env`:
```env
API_URL=https://api.openai.com/v1/completions
API_KEY=twoj-klucz-api
```

## Uruchomienie

```bash
python quiz.py
```

## Konfiguracja

W pliku `config.py` możesz dostosować:
- `MIN_QUESTIONS`: Minimalna liczba pytań (domyślnie: 1)
- `MAX_QUESTIONS`: Maksymalna liczba pytań (domyślnie: 30)

## Architektura

Projekt składa się z 5 głównych modułów:

### 1. `config.py`
Przechowuje stałe konfiguracyjne i parametry API.

### 2. `ui_text.py` - Interfejs użytkownika
- Wyświetlanie komunikatów
- Pobieranie danych od użytkownika
- Walidacja wejścia
- Wyświetlanie pytań i wyników

### 3. `ai_generator.py` - Generator pytań AI
- Komunikacja z API modelu AI
- Walidacja odpowiedzi z modelu
- Obsługa błędów sieciowych
- Formatowanie pytań do standardowej struktury

### 4. `quiz_logic.py` - Logika quizu
- Klasa `Question`: Reprezentacja pytania z walidacją
- Klasa `Quiz`: Zarządzanie przebiegiem quizu
- Sprawdzanie poprawności odpowiedzi
- Zliczanie punktów

### 5. `result_procesor.py` - Processor wyników
- Generowanie raportu końcowego
- Ocena procentowa
- Formatowanie listy błędnych odpowiedzi

## Testy

Uruchomienie testów jednostkowych:

```bash
pytest
```

Uruchomienie testów z pokryciem kodu:

```bash
pytest --cov
```

Testy obejmują:
- Walidację danych wejściowych
- Logikę quizu
- Generowanie raportów
- Interfejs użytkownika
- Komunikację z API (mock)

## Zasady projektowe

Projekt został zbudowany zgodnie z następującymi zasadami:

1. **Separacja odpowiedzialności**: Każdy moduł ma jasno określone zadanie
2. **Testowalność**: Wszystkie moduły są łatwo testowalne (dependency injection)
3. **Walidacja**: Każdy moduł waliduje swoje dane wejściowe
4. **Obsługa błędów**: Dedykowane wyjątki dla różnych typów błędów
5. **Czytelny kod**: PEP 8, typowanie (Type Hints), docstringi

## Bezpieczeństwo

- Klucz API jest przechowywany w pliku `.env` (nie commitowany do repozytorium)
- Walidacja wszystkich danych wejściowych użytkownika
- Obsługa błędów sieciowych i timeoutów

## Planowane rozszerzenia

- Tryb offline z bazą gotowych pytań
- Eksport wyników do pliku
- Obsługa różnych języków
- Różne poziomy trudności pytań
- Statystyki historyczne

## Licencja

Projekt edukacyjny - Ready_4AI

## Kontakt

W razie pytań lub problemów, utwórz issue w repozytorium projektu.
