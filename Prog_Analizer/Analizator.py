"""
Ocena spójności logicznej tekstu przy uzyciu modelu LLM OpenAI (gtp-4o-mini)
"""

import os
import re
import json
import argparse
import requests


# Konfiguracja API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/responses"
MODEL_NAME = "gpt-4o-mini"
if not OPENAI_API_KEY:
    raise EnvironmentError("Brak ustawionej zmiennej środowiskowej OPENAI_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}


def analiza_tekstu(text: str) -> dict:
    prompt = f"""
    Analizuj poniższy tekst pod kątem spójności logicznej.

    Tekst do analizy:
    \"\"\"{text}\"\"\"
    """

    payload = {
        "model": "gpt-4o-mini",
        "input": prompt
    }

    response = requests.post("https://api.openai.com/v1/responses", headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()
    return result                   # Tymczasowo do testów


def get_next_number():      # Brak param - Założenie analizy plików z bieżącego katalogu. Wzór ustalony na sztywno w funkcji
    pattern = re.compile(r"Analiza_\(cli_" + r"(\d{3})\)\.txt$") 
    max = 0
    for file in os.listdir("."):
        match = pattern.search(file)
        if match:
            num = int(match.group(1))
            if num > max:
                max = num
    return max + 1


def main():
    parser = argparse.ArgumentParser(description='Analiza jakości i spójności tekstu przy użyciu modelu OpenAI - gpt-4o-mini.')
    parser.add_argument('-i', type=str, help='Input file path')
    args = parser.parse_args()

    if args.i:
        try:
            if not os.path.exists(args.i):
                print(f'Plik nie istnieje: {args.i}')
                return
            with open(args.i, 'r', encoding='utf-8') as in_f:
                text = in_f.read()
        except Exception as e:
            print(f'Błąd odczytu pliku: {e}')
            return  
    else:
        text = input('Podaj tekst do analizy: ')

    try:
        result = analiza_tekstu(text)
    except Exception as e:
        print(f'Błąd podczas analizy: {e}')
        return
    
    try:
        # Ustalanie nazwy pliku
        if args.i:
            base_name = os.path.splitext(os.path.basename(args.i))[0]
        else:
            base_name = f"cli_{get_next_number():03d}"
        fname = f"Analiza_({base_name}).txt"
        
        with open(fname, 'w', encoding='utf-8') as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
        print(f'Analiza zakończona. Wynik zapisano do: {fname}')
    except Exception as e:
        print(f'Błąd zapisu wyniku: {e}')
        return
    

if __name__ == "__main__":
    main() 