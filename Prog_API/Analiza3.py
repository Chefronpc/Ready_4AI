import os
import json
import uuid
from datetime import datetime
import requests

# ==========================
# KONFIGURACJA API
# ==========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/responses"
MODEL_NAME = "gpt-4o-mini"

if not OPENAI_API_KEY:
    raise EnvironmentError("Brak ustawionej zmiennej środowiskowej OPENAI_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

# ==========================
# FUNKCJE POMOCNICZE
# ==========================

def generate_text_id() -> str:
    """Generuje unikalny ID dla analizowanego tekstu"""
    return str(uuid.uuid4())

def get_timestamp() -> str:
    """Zwraca aktualny timestamp w formacie YYYY-MM-DD_HH-MM-SS"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def save_json_report(data: dict, timestamp: str):
    """Zapisuje wynik analizy do pliku JSON"""
    filename = f"Ocena_analizy_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Raport zapisany do pliku: {filename}")

# ==========================
# ANALIZA TEKSTU
# ==========================

def analyze_text(text: str) -> dict:
    """
    Wysyła tekst do modelu LLM i pobiera analizę w formacie JSON
    """
    prompt = f"""
    Analizuj poniższy tekst w języku polskim pod kątem (lista kategorii analizy):
    - spójności logicznej między zdaniami i akapitami
    - jasności argumentacji i uzasadnienia stwierdzeń
    - spójności narracyjnej i struktury tekstu
    - stylu retorycznego i tonu (formalny, emocjonalny, promocyjny)
    - emocjonalności oraz adekwatności używanego języka

    Wygeneruj odpowiedź w formacie JSON dokładnie takim jak poniżej:

    {{
      "analysis": {{
        "issues": [
          {{
            "category": "<kategoria_analizy>",
            "description": "<krótki opis problemu w kontekście kategorii>",
            "excerpt": "<fragment tekstu będący przykładem problemu>",
            "issue": "<dokładny opis problemu>",
            "offset_start": <indeks_startowy>,
            "offset_end": <indeks_końcowy>
          }}
        ],
        "confidence": "<wartość ufności modelu>"
      }},
      "report": {{
        "summary": "<ogólne podsumowanie jakości tekstu>",
        "recommendations": [
          "<zalecenie_1>",
          "<zalecenie_2>",
          "<zalecenie_3>"
        ]
      }}
    }}

    Tekst do analizy:
    \"\"\"{text}\"\"\"
    """

    payload = {
        "model": MODEL_NAME,
        "input": prompt
    }

    response = requests.post(OPENAI_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()

    # Pobieramy wygenerowany tekst z modelu
    # Struktura response może się różnić w zależności od wersji API
    try:
        model_output = result["output_text"]  # jeśli REST API zwraca output_text
        analysis_json = json.loads(model_output)
    except Exception as e:
        raise ValueError(f"Błąd parsowania odpowiedzi modelu: {e}\nOdpowiedź: {result}")

    return analysis_json

# ==========================
# GŁÓWNA FUNKCJA
# ==========================

def main():
    # Przykładowy tekst do analizy
    text_to_analyze = """
    Twoja treść tekstu do analizy wstaw tutaj. Może to być artykuł, e-mail lub inny dokument.
    """

    text_id = generate_text_id()
    timestamp = get_timestamp()

    # Analiza tekstu
    analysis_result = analyze_text(text_to_analyze)

    # Tworzenie pełnej struktury JSON
    full_report = {
        "metadata": {
            "model": MODEL_NAME,
            "language": "pl",
            "python_version": ">=3.10",
            "timestamp": timestamp
        },
        "input": {
            "text_id": text_id,
            "text": text_to_analyze
        },
        **analysis_result
    }

    # Zapis do pliku
    save_json_report(full_report, timestamp)


if __name__ == "__main__":
    main()
