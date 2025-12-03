# Ready4AI Chatbot Web & Desktop

Desktopowa aplikacja PySide6 stanowi lekki frontend dla backendu Flask z tego projektu. Poniżej znajdziesz kroki potrzebne do uruchomienia całości lokalnie.

## Wymagania
- Python 3.11+
- Konto i klucz API OpenAI (`OPENAI_API_KEY` w `.env`)
- Zależności z pliku `requirments.txt` (backend + desktop)

## Konfiguracja środowiska
1. Skopiuj plik `.env.example` (jeżeli istnieje) lub utwórz `.env` z wpisami:
   ```env
   OPENAI_API_KEY=twoj_klucz
   CHATBOT_BACKEND_URL=http://127.0.0.1:5000
   CHATBOT_CHAT_ENDPOINT=/chat
   ```
2. Zainstaluj pakiety:
   ```powershell
   cd c:\Project\Ready_4AI\Prog_Chatbot_Web
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirments.txt
   ```

## Uruchomienie backendu (Flask)
```powershell
python app.py
```
Serwer domyślnie nasłuchuje pod `http://127.0.0.1:5000`. Endpoint `/chat` deleguje zapytania do OpenAI korzystając z kontekstu konwersacji (`responseId`).

## Uruchomienie aplikacji desktopowej (PySide6)
```powershell
python desktop_app.py
```
Aplikacja:
- pozwala wprowadzać wiadomości do modelu,
- wyświetla historię rozmowy wraz z odpowiedziami backendu,
- zachowuje `responseId`, aby kontynuować konwersację,
- pokazuje status połączenia w dolnym pasku.

## Dodatkowe uwagi
- Skrót `Ctrl+Enter` wysyła wiadomość, przyciski "Wyślij" i "Wyczyść" sterują przepływem rozmowy.
- Błędy HTTP oraz wyjątki sieciowe są pokazywane w historii, co ułatwia diagnostykę.
- Jeżeli backend działa na innym hostcie/porcie lub masz niestandardowy endpoint, zaktualizuj zmienne środowiskowe w `.env`.
