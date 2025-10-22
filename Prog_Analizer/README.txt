

    Ocena spójności logicznej tekstu przy użyciu modelu LLM OpenAI (gpt-4o-mini).
    Realizuje proces: Pobranie danych -> Analiza -> Raport

    Wymagania:
        pakiety z pliku requirments.text

    Opis działania:
        1. Program wczytuje dane z wiersza poleceń lub pliku wejściowego. Zależne od podania parametru -i
        2. "Odbiera" testowy wynik analizy i zapisuje raport w pliku tekstowym o nazwie zależnej od użycia parametru -i
            a. Analiza_(cli_xxx).txt        # Dane wejściowe pobierane z CLI (xxx - numeracja 1-1000) 
            b. Analiza_(tekst).txt          # Dane wejściowe pobierane z pliku tekstowego
    
    Przykład użycia:Uruchomienie:
        py Analizator.py                    # Dane wejściowe pobierane z CLI
        py Analizator.py -i tekst.txt       # Dane wejściowe pobrane z pliku tekst.txt

    Info:
        autonumeracja zatrzymuje się na 1000 -> nadpisywanie analizy o tym numerze