import pytest
from result_procesor import build_report


# ===== TESTY PODSTAWOWEJ FUNKCJONALNOŚCI =====

def test_build_report_all_correct():
    """Test raportu gdy wszystkie odpowiedzi są poprawne"""
    report = build_report(total=5, correct=5, wrong_items=[])
    
    assert "Wszystkie pytania: 5" in report
    assert "Poprawne: 5" in report
    assert "Błędne: 0" in report
    assert "100.0%" in report
    assert "DOSKONALE" in report
    assert "Gratulacje! Wszystkie odpowiedzi były poprawne!" in report


def test_build_report_all_wrong():
    """Test raportu gdy wszystkie odpowiedzi są błędne"""
    wrong_items = [
        {
            "index": 1,
            "user": "a",
            "correct": "b",
            "question": "Pytanie 1?",
            "correct_text": "Odpowiedź B"
        }
    ]
    
    report = build_report(total=1, correct=0, wrong_items=wrong_items)
    
    assert "Wszystkie pytania: 1" in report
    assert "Poprawne: 0" in report
    assert "Błędne: 1" in report
    assert "0.0%" in report
    assert "NIE PODDAWAJ SIĘ" in report
    assert "Pytanie 1" in report
    assert "Twoja odpowiedź: A" in report
    assert "Poprawna odpowiedź: B - Odpowiedź B" in report


def test_build_report_mixed_results():
    """Test raportu z mieszanymi wynikami"""
    wrong_items = [
        {
            "index": 2,
            "user": "c",
            "correct": "d",
            "question": "Które jest poprawne?",
            "correct_text": "Opcja D"
        },
        {
            "index": 4,
            "user": "a",
            "correct": "b",
            "question": "Co to jest?",
            "correct_text": "Opcja B"
        }
    ]
    
    report = build_report(total=5, correct=3, wrong_items=wrong_items)
    
    assert "Wszystkie pytania: 5" in report
    assert "Poprawne: 3" in report
    assert "Błędne: 2" in report
    assert "60.0%" in report
    assert "DOBRZE" in report
    assert "Pytanie 2" in report
    assert "Pytanie 4" in report


# ===== TESTY GRADACJI OCEN =====

@pytest.mark.parametrize("total,correct,expected_grade", [
    (10, 9, "DOSKONALE"),     # 90%
    (10, 10, "DOSKONALE"),    # 100%
    (100, 90, "DOSKONALE"),   # 90%
    (10, 8, "BARDZO DOBRZE"), # 80%
    (20, 15, "BARDZO DOBRZE"),# 75%
    (10, 7, "DOBRZE"),        # 70%
    (10, 6, "DOBRZE"),        # 60%
    (20, 13, "DOBRZE"),       # 65%
    (10, 5, "ŚREDNIO"),       # 50%
    (20, 11, "ŚREDNIO"),      # 55%
    (10, 4, "NIE PODDAWAJ SIĘ"), # 40%
    (10, 0, "NIE PODDAWAJ SIĘ"), # 0%
])
def test_build_report_grade_thresholds(total, correct, expected_grade):
    """Test progów oceniania"""
    wrong_count = total - correct
    wrong_items = [
        {
            "index": i+1,
            "user": "a",
            "correct": "b",
            "question": f"Pytanie {i+1}",
            "correct_text": "Poprawna"
        }
        for i in range(wrong_count)
    ]
    
    report = build_report(total=total, correct=correct, wrong_items=wrong_items)
    assert expected_grade in report


# ===== TESTY WALIDACJI WEJŚCIA =====

def test_build_report_invalid_total_negative():
    """Test walidacji ujemnej wartości total"""
    with pytest.raises(ValueError, match="nieujemną liczbą całkowitą"):
        build_report(total=-1, correct=0, wrong_items=[])


def test_build_report_invalid_total_not_int():
    """Test walidacji typu total"""
    with pytest.raises(ValueError, match="nieujemną liczbą całkowitą"):
        build_report(total="5", correct=0, wrong_items=[])


def test_build_report_invalid_correct_negative():
    """Test walidacji ujemnej wartości correct"""
    with pytest.raises(ValueError, match="nieujemną liczbą całkowitą"):
        build_report(total=5, correct=-1, wrong_items=[])


def test_build_report_invalid_correct_not_int():
    """Test walidacji typu correct"""
    with pytest.raises(ValueError, match="nieujemną liczbą całkowitą"):
        build_report(total=5, correct=3.5, wrong_items=[])


def test_build_report_correct_greater_than_total():
    """Test walidacji gdy correct > total"""
    with pytest.raises(ValueError, match="nie może być większa niż total"):
        build_report(total=5, correct=10, wrong_items=[])


def test_build_report_wrong_items_not_list():
    """Test walidacji typu wrong_items"""
    with pytest.raises(ValueError, match="musi być listą"):
        build_report(total=5, correct=3, wrong_items="not a list")


def test_build_report_inconsistent_data():
    """Test walidacji spójności danych"""
    wrong_items = [
        {
            "index": 1,
            "user": "a",
            "correct": "b",
            "question": "Test?",
            "correct_text": "B"
        }
    ]
    
    # correct + len(wrong_items) != total
    with pytest.raises(ValueError, match="musi być równa total"):
        build_report(total=5, correct=3, wrong_items=wrong_items)


# ===== TESTY FORMATOWANIA =====

def test_build_report_multiple_wrong_answers():
    """Test formatowania wielu błędnych odpowiedzi"""
    wrong_items = [
        {
            "index": 1,
            "user": "a",
            "correct": "b",
            "question": "Pierwsze pytanie?",
            "correct_text": "Pierwsza poprawna"
        },
        {
            "index": 3,
            "user": "c",
            "correct": "d",
            "question": "Trzecie pytanie?",
            "correct_text": "Trzecia poprawna"
        },
        {
            "index": 5,
            "user": "b",
            "correct": "a",
            "question": "Piąte pytanie?",
            "correct_text": "Piąta poprawna"
        }
    ]
    
    report = build_report(total=5, correct=2, wrong_items=wrong_items)
    
    # Sprawdź obecność wszystkich pytań
    assert "Pytanie 1:" in report
    assert "Pytanie 3:" in report
    assert "Pytanie 5:" in report
    
    # Sprawdź formatowanie odpowiedzi
    assert "A" in report  # user choices uppercase
    assert "B" in report
    assert "C" in report
    assert "D" in report


def test_build_report_percentage_formatting():
    """Test formatowania procentów"""
    # Test różnych wartości procentowych
    report1 = build_report(total=3, correct=2, wrong_items=[{
        "index": 1, "user": "a", "correct": "b", 
        "question": "Q?", "correct_text": "B"
    }])
    assert "66.7%" in report1
    
    report2 = build_report(total=7, correct=5, wrong_items=[
        {"index": i, "user": "a", "correct": "b", "question": "Q?", "correct_text": "B"}
        for i in range(2)
    ])
    assert "71.4%" in report2


def test_build_report_edge_case_zero_questions():
    """Test przypadku brzegowego - zero pytań"""
    report = build_report(total=0, correct=0, wrong_items=[])
    
    assert "Wszystkie pytania: 0" in report
    assert "Poprawne: 0" in report
    assert "Błędne: 0" in report


def test_build_report_single_question_correct():
    """Test pojedynczego pytania - poprawna odpowiedź"""
    report = build_report(total=1, correct=1, wrong_items=[])
    
    assert "Wszystkie pytania: 1" in report
    assert "Poprawne: 1" in report
    assert "100.0%" in report
    assert "DOSKONALE" in report
    assert "Gratulacje" in report


def test_build_report_single_question_wrong():
    """Test pojedynczego pytania - błędna odpowiedź"""
    wrong_items = [{
        "index": 1,
        "user": "a",
        "correct": "b",
        "question": "Jedyne pytanie?",
        "correct_text": "Poprawna B"
    }]
    
    report = build_report(total=1, correct=0, wrong_items=wrong_items)
    
    assert "Wszystkie pytania: 1" in report
    assert "Błędne: 1" in report
    assert "0.0%" in report
    assert "Jedyne pytanie?" in report


# ===== TESTY ZAWARTOŚCI RAPORTU =====

def test_build_report_contains_icons():
    """Test obecności ikon emoji w raporcie"""
    report = build_report(total=5, correct=5, wrong_items=[])
    
    assert "📊" in report  # Statystyki
    assert "🎯" in report  # Ocena
    assert "🌟" in report  # Gratulacje


def test_build_report_contains_wrong_answer_icon():
    """Test obecności ikony błędnej odpowiedzi"""
    wrong_items = [{
        "index": 1,
        "user": "a",
        "correct": "b",
        "question": "Test?",
        "correct_text": "B"
    }]
    
    report = build_report(total=1, correct=0, wrong_items=wrong_items)
    assert "❌" in report


def test_build_report_structure():
    """Test struktury raportu"""
    wrong_items = [{
        "index": 1,
        "user": "a",
        "correct": "b",
        "question": "Test?",
        "correct_text": "B"
    }]
    
    report = build_report(total=2, correct=1, wrong_items=wrong_items)
    
    # Sprawdź sekcje raportu w odpowiedniej kolejności
    stats_pos = report.find("Statystyki")
    grade_pos = report.find("Ocena")
    wrong_pos = report.find("Błędne odpowiedzi")
    
    assert stats_pos > 0
    assert grade_pos > stats_pos
    assert wrong_pos > grade_pos


# ===== TESTY WYDAJNOŚCIOWE =====

def test_build_report_large_number_of_wrong_answers():
    """Test dużej liczby błędnych odpowiedzi"""
    wrong_items = [
        {
            "index": i+1,
            "user": "a",
            "correct": "b",
            "question": f"Pytanie numer {i+1}?",
            "correct_text": f"Poprawna odpowiedź {i+1}"
        }
        for i in range(50)
    ]
    
    report = build_report(total=50, correct=0, wrong_items=wrong_items)
    
    assert "Wszystkie pytania: 50" in report
    assert "Błędne: 50" in report
    # Sprawdź, czy wszystkie pytania są w raporcie
    for i in range(1, 51):
        assert f"Pytanie {i}" in report or f"Pytanie numer {i}" in report
