import os
import re
import json
import argparse
import requests


# Konfiguracja API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/responses"
#MODEL_NAME = "gpt-5"
MODEL_NAME = "gpt-4o-mini"
if not OPENAI_API_KEY:
    raise EnvironmentError("Brak ustawionej zmiennej środowiskowej OPENAI_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}


def analiza_tekstu(text: str) -> dict:
    prompt = f"""
       Jesteś asystentem analizy tekstu. Twoim zadaniem jest przeprowadzenie obiektywnej analizy podanego tekstu według poniższych wytycznych:
        - logiki wypowiedzi - nie tylko w obrębie zdania, lecz również zależności między zdaniami lub akapitami.
            przeanalizuj czy elementy wypowiedzi, które z kontekstu są zależne, są spójne pod względem logiki.
        - poprawności gramatycznej - poprawności budowy zdań, użytych odpowiednich odmian, porządku słów, w stosunku do oficjalnych reguł języka.
            Gdy stwierdzisz tekst o odbiegającej od normy budowie, zweryfikuj, czy może być tekstem z kategorii, slangu, odrębnej kultury lub innych typów określeń języków.
        - stylu oraz tonu wypowiedzi.       
       
       (ortograficzne -> podaj słowo z błędem oraz wersje poprawną;  gramatyczne/stylistyczne -> fragment zdania oraz poprawną postać całego zdania).
       przykład każdego błędu jako jednolity string w formacie " {{typ błędu}}: {{słowo/zdanie z błędem}} -> poprawnie: {{poprawna wersja}}".
       
       (logiki wypowiedzi -> podaj fragment wykazujący brak logiki oraz wyjasnienie lub poprawną formę)
        przykład każdego fragmentu jako string w formacie " {{fragment zdania}} -> {{objasnienie / poprawna forma}}".

    Analiza powinna być oparta **wyłącznie na treści dostarczonego tekstu** — nie dodawaj informacji spoza podanego tekstu do analizy. 


  Zakres oceny: 

    1. kategoria: Spójność logiczna
    Oceń, czy tekst jest spójny pod względem logicznym.   
    - etykiety: [przykłady: spójny, niespójny, częściowo niespójny, ... ] 
    - ocena: 1-10 (1 = wiele sprzeczności, 10 = spójny)   
    - błędy: Jeżeli jest, dołącz fragment oryginalnego tekstu z przykładową niespójnością do tego punktu
    
    2. kategoria: Poprawność gramatyczna
    Oceń poziom poprawności gramatycznej w tekście.  
    - etykiety: [błędy gramatyczne, ortograficzne, stylistyczne, ...]
    - ocena: 1-10 (1 = wiele różnych błędów, 10 = bezbłędny)
    - błędy: Jeżeli są błędy, dołącz ich treść z błęd ami do tego puntku

    3. kategoria: Ton
    Określ charakter języka
    - etykiety: [ironiczny, sarkastyczny, uprzejmy, ...]  
    - intensywność: 1-10 (1 = słabo zauważalny ton, 10 = bardzo wyraźny ton)
    
    4. kategoria: Styl
    Określ styl języka
    - etykiety: [potoczny, formalny, neutralny, ...]  
    - intensywność: 1-10 (1 = neutralny, 10 = intensywny)

  Format odpowiedzi (JSON): Zwróć dane **dokładnie w poniższej strukturze JSON**, bez dodatkowych komentarzy, tekstu, znaków specjalnych \n, \t, itp:

    {{  
        "kategorie": [
            {{
                "kategoria": "Spójność logiczna":
                "poziom": 4,
                "etykiety": [ określenia w formie listy],
                "błędy": [ ]
            }}, {{
                "kategoria": "Poprawność gramatyczna":
                "poziom": 8,
                "etykiety": [ określenia w formie listy],
                "błędy": [ ]
            }}, {{
                "kategoria": "Ton":
                "poziom": 3,
                "etykiety": [ określenia w formie listy]
            }}, {{
                "kategoria": "Styl":
                "poziom": 6,
                "etykiety": [ określenia w formie listy]
            }}
        ],
        "uwagi": "Krótki komentarz podsumowujący (1-3 zdania)."
        ]
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
    return response.json()['output'][0]['content'][0]['text']
   

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
                input_txt = in_f.read()
        except Exception as e:
            print(f'Błąd odczytu pliku: {e}')
            return  
    else:
        input_txt = input('Podaj tekst do analizy: ')

    try:
        result = analiza_tekstu(input_txt)
    except Exception as e:
        print(f'Błąd podczas analizy: {e}')
        return    

    dane = json.loads(result)
  
    rows = []
    rows.append("Wynik analizy:\n")
    
    for kategoria in dane["kategorie"]:
        rows.append(f"{kategoria['kategoria']}:")
        rows.append(f"  Poziom: {kategoria['poziom']}")
        rows.append(f"  Etykiety: {','.join(kategoria['etykiety'])}")
        if kategoria.get("błędy"):
            rows.append("  Błędy:")
            for blad in kategoria["błędy"]:
                rows.append(f"    - {blad}")
        rows.append("")  # odstęp między kategoriami
    rows.append(f"Uwagi: {dane['uwagi']}\n")
        
    text = "\n".join(rows)

    try:
        # Ustalanie nazwy pliku
        if args.i:
            base_name = os.path.splitext(os.path.basename(args.i))[0]
        else:
            base_name = f"cli_{get_next_number():03d}"
        fname = f"Analiza_({base_name}).txt"
        
        with open(fname, 'w', encoding='utf-8') as out_f:
            out_f.write(text)
        print(f'Analiza zakończona. Wynik zapisano do: {fname}')
    except Exception as e:
        print(f'Błąd zapisu wyniku: {e}')
        return
    

if __name__ == "__main__":
    main() 