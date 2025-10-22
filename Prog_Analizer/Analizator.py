"""
Ocena spójności logicznej tekstu przy uzyciu modelu LLM OpenAI (gtp-4o-mini)
"""

import os
import json
import argparse
import requests


def main():
    parser = argparse.ArgumentParser(description='Analiza jakości i spójności tekstu przy użyciu modelu OpenAI - gpt-4o-mini.')
    parser.add_argument('--input-file', type=str, help='Input file path')
    parser.add_argument('--output-file', type=str, help='Output file path')
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, 'r', encoding='utf-8') as in_f:
            text = in_f.read()
    else:
        text = input('Podaj tekst do analizy: ')

    try:
        result = "Testowa odpowiedź modelu językowego."
        #result = analiza_tekstu(text)
    except Exception as e:
        print(f'Błąd podczas analizy: {e}')
        return
    
    try:
        if args.input_file:
            base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        else:
            base_name = f"cli_{round}"
        fname = f"Analiza_({base_name}).txt"
        with open(fname, 'w', encoding='utf-8') as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
        print(f'Analiza zakończona. Wynik zapisano do: {fname}')
    except Exception as e:
        print(f'Błąd zapisu wyniku: {e}')
        return
    

if __name__ == "__main__":
    main() 