import os
import requests

# 🔹 Konfiguracja – ustaw swój klucz API w zmiennej środowiskowej
API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

def analyze_text(text: str) -> str:
    """
    Funkcja wysyła tekst do modelu LLM i zwraca analizę sprzeczności logicznych.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",   # możesz użyć gpt-5, gpt-4o-mini itp.
        "messages": [
            {"role": "system", "content": "Jesteś analitykiem logiki tekstu."},
            {"role": "user", "content": f"Przeanalizuj poniższy tekst i wskaż sprzeczności logiczne lub niespójności:\n\n{text}"}
        ],
        "temperature": 0.2  # niska temperatura = bardziej precyzyjna, mniej twórcza odpowiedź
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Błąd API: {response.status_code} {response.text}"

def main():
    print("=== Analizator sprzeczności logicznych w tekście ===")
    user_text = input("Wklej tekst do analizy:\n> ")

    print("\n⏳ Analizuję tekst, proszę czekać...\n")
    analysis = analyze_text(user_text)

    print("=== Wynik analizy ===")
    print(analysis)

if __name__ == "__main__":
    main()
