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
       Jesteś asystentem analizy tekstu. Twoim zadaniem jest przeprowadzenie obiektywnej analizy podanego tekstu w kontekście spójnosci logicznej, poprawności gramatycznej, stylu oraz tonu.
  Analiza powinna być oparta **wyłącznie na treści dostarczonego tekstu** — nie dodawaj informacji spoza podanego tekstu do analizy. 

  Zakres oceny: 

    1. Spójność logiczna
    Oceń, czy tekst jest spójny pod względem logicznym.   
    - etykiety: [przykłady: spójny, niespójny, częściowo niespójny, ... ] 
    - ocena: 1-10 (1 = wiele sprzeczności, 10 = spójny)   
    
    2. **Poprawność gramatyczna**  
    Oceń poziom poprawności gramatycznej w tekście.  
    - dominujące_błędy: [gramatyczne, ortograficzne, stylistyczne, ...]
    - ocena: 1-10 (1 = wiele różnych błędów, 10 = bezbłędny)  

    3. **Ton**  
    Określ charakter języka
    - etykiety: [ironiczny, sarkastyczny, uprzejmy, ...]  
    - intensywność: 1-10 (1 = słabo zauważalny ton, 10 = bardzo wyraźny ton)
    
    4. **Styl**  
    Określ styl języka
    - etykiety: [potoczny, formalny, neutralny, ...]  
    - intensywność: 1-10 (1 = neutralny, 10 = intensywny)


  Format odpowiedzi (JSON):

    Zwróć dane **dokładnie w poniższej strukturze JSON**, bez dodatkowych komentarzy ani tekstu:

    {{
    "analiza_artykulu": 
       {{
        "kategoria": {{
        "ocena": int,
        "etykieta": [string, ...]
        }},
         {{
          ...
         }},
         .... ,
        "meta": {{
        "uwagi": "krótki komentarz (1-2 zdania podsumowania oceny)"
        }}
    }}
    }}

  
    ### Zasady:
    - Etykietę nadaj zgodną z kategorią i dopasuj do skali i uzyskanej oceny.
    - Jeśli czegoś nie da się ocenić — użyj wartości neutralnych (np. ocena = 5).
    - Używaj języka polskiego w odpowiedzi.

  
    Analizowany tekst:

    """

    payload = {
        "model": "gpt-4o-mini",
        "input": prompt + text
    }

    response = requests.post("https://api.openai.com/v1/responses", headers=HEADERS, json=payload)
    response.raise_for_status()
    response = response.json()
    return response


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
        
        

        #output = result["analiza_artykulu"][0]
        #comments = result["analiza_artykulu"][0]["meta"][0]["Uwagi"]
        output = "-"
        comments = "-"
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
            json.dump(f"{print(type(result))}    Analiza tekstu:\n\n {output} \n\nUwagi: \n{comments}", out_f, ensure_ascii=False, indent=2)
        print(f'Analiza zakończona. Wynik zapisano do: {fname}')
    except Exception as e:
        print(f'Błąd zapisu wyniku: {e}')
        return
    

if __name__ == "__main__":
    main() 