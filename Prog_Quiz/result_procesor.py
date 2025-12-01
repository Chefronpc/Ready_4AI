from typing import List, Dict


def build_report(total: int, correct: int, wrong_items: List[Dict]) -> str:
    """
    Tworzy raport tekstowy z wynikami quizu.
    
    Args:
        total: Liczba wszystkich pytań w quizie
        correct: Liczba poprawnych odpowiedzi
        wrong_items: Lista słowników z informacjami o błędnych odpowiedziach.
                     Każdy słownik powinien zawierać:
                     - index: numer pytania (1-based)
                     - user: odpowiedź użytkownika ('a'/'b'/'c'/'d')
                     - correct: poprawna odpowiedź ('a'/'b'/'c'/'d')
                     - question: treść pytania
                     - correct_text: tekst poprawnej odpowiedzi
    
    Returns:
        Sformatowany string z raportem (multi-line)
    
    Raises:
        ValueError: Jeśli parametry są nieprawidłowe
    """
    # Walidacja wejścia
    if not isinstance(total, int) or total < 0:
        raise ValueError("Total musi być nieujemną liczbą całkowitą")
    
    if not isinstance(correct, int) or correct < 0:
        raise ValueError("Correct musi być nieujemną liczbą całkowitą")
    
    if correct > total:
        raise ValueError("Liczba poprawnych nie może być większa niż total")
    
    if not isinstance(wrong_items, list):
        raise ValueError("Wrong_items musi być listą")
    
    # Obliczenia
    wrong = len(wrong_items)
    
    # Walidacja spójności danych
    if correct + wrong != total:
        raise ValueError("Suma poprawnych i błędnych odpowiedzi musi być równa total")
    
    percentage = (correct / total * 100) if total > 0 else 0
    
    # Budowanie raportu
    report_lines = []
    
    # Nagłówek statystyk
    report_lines.append("")
    report_lines.append("  📊 Statystyki:")
    report_lines.append(f"     • Wszystkie pytania: {total}")
    report_lines.append(f"     • Poprawne: {correct}")
    report_lines.append(f"     • Błędne: {wrong}")
    report_lines.append(f"     • Wynik procentowy: {percentage:.1f}%")
    
    # Ocena
    if percentage >= 90:
        grade = "🏆 DOSKONALE!"
    elif percentage >= 75:
        grade = "🎉 BARDZO DOBRZE!"
    elif percentage >= 60:
        grade = "👍 DOBRZE!"
    elif percentage >= 50:
        grade = "📚 ŚREDNIO - POTRZEBA WIĘCEJ NAUKI"
    else:
        grade = "💪 NIE PODDAWAJ SIĘ - ĆWICZ DALEJ!"
    
    report_lines.append("")
    report_lines.append(f"  🎯 Ocena: {grade}")
    
    # Lista błędów
    if wrong_items:
        report_lines.append("")
        report_lines.append("  ❌ Błędne odpowiedzi:")
        
        for item in wrong_items:
            report_lines.append("")
            report_lines.append(f"     Pytanie {item['index']}: {item['question']}")
            report_lines.append(f"     • Twoja odpowiedź: {item['user'].upper()}")
            report_lines.append(f"     • Poprawna odpowiedź: {item['correct'].upper()} - {item['correct_text']}")
    else:
        report_lines.append("")
        report_lines.append("  🌟 Gratulacje! Wszystkie odpowiedzi były poprawne!")
    
    report_lines.append("")
    
    return "\n".join(report_lines)
