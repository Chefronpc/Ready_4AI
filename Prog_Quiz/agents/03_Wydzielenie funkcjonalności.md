[[_Projektowanie aplikacji quizu w Pythonie]]
### 1. Moduł **Interfejsu użytkownika (UI_Text)**

**Odpowiedzialność:** komunikacja człowiek ↔ program w konsoli.  
**Funkcje:**

- Wyświetlenie powitania i instrukcje.
- Pobranie od użytkownika:
    - tematu quizu,
    - liczby pytań.
- Wyświetlenie kolejnych pytań i czterech możliwych odpowiedzi.
- Pobranie odpowiedzi użytkownika (a/b/c/d).
- Wyświetlenie wyników końcowych oraz poprawnych odpowiedzi.  

	**Wejście/Wyjście:**
- Wejście: dane użytkownika (temat, liczba pytań, odpowiedzi)
- Wyjście: wynik i informacja zwrotna

---

### 2. Moduł **AI_Generator**

**Odpowiedzialność:** generowanie treści quizu z wykorzystaniem modelu AI.  

**Funkcje:**
- Przyjęcie tematu i liczby pytań od użytkownika.    
- Wysłanie zapytania do modelu (prompt).
- Odbiór odpowiedzi i walidacja struktury JSON (zgodność z oczekiwanym formatem).
- Zwrócenie listy pytań i odpowiedzi w formacie np.:
    `[   {"question": "...", "a": "...", "b": "...", "c": "...", "d": "...", "correct": "b"},   ... ]`

**Wejście/Wyjście:**
- Wejście: temat, liczba pytań
- Wyjście: lista pytań i odpowiedzi

---

### 3. Moduł **Quiz_Logic**

**Odpowiedzialność:** obsługa przebiegu quizu (logika gry).  

**Funkcje:**
- Iterowanie przez listę pytań.
- Odbiór odpowiedzi użytkownika (poprzez UI_Text).
- Sprawdzenie poprawności (porównanie z kluczem „correct”).
- Zliczanie punktów (poprawne / błędne).
- Przechowywanie listy błędnych odpowiedzi.  
    
    **Wejście/Wyjście:**
- Wejście: lista pytań, odpowiedzi użytkownika
- Wyjście: wynik końcowy, lista błędów

---

### 4. Moduł **Result_Processor**

**Odpowiedzialność:** analiza wyników i prezentacja podsumowania.  

**Funkcje:**
- Zliczanie liczby poprawnych i błędnych odpowiedzi.
- Generowanie raportu końcowego (tekstowego).
- Przekazanie raportu do modułu UI_Text do wyświetlenia.  
    
    **Wejście/Wyjście:**    
- Wejście: dane z Quiz_Logic
- Wyjście: tekst raportu końcowego

---

### 5. Moduł **Config / Constants**

**Odpowiedzialność:** przechowywanie ustawień i ograniczeń.  

**Funkcje:**
- Stałe konfiguracyjne: MIN_QUESTIONS, MAX_QUESTIONS.
- Parametry komunikacji z modelem AI pobierane z pliku .env (np. token, URL API).
- Format prompta i struktury danych.

---

### Relacje między modułami (prosty schemat przepływu)

`User ⇄ UI_Text → Quiz_Logic  ⇄  AI_Generator

Quiz_Logic → Result_Processor → UI_Text → output`


