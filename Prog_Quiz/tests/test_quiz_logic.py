import pytest
from quiz_logic import (
    Question, Quiz, QuizBackend,
    QuizException, InvalidQuestionError, InvalidAnswerError,
    QuizStateError, EmptyQuizError
)


# ===== TESTY KLASY QUESTION =====

def test_question_is_correct():
    """Test podstawowej funkcjonalności sprawdzania poprawności odpowiedzi"""
    q = Question("2+2=", ["3", "4", "5"], 1)
    assert q.is_correct(1)
    assert not q.is_correct(0)
    assert not q.is_correct(2)


def test_question_valid_creation():
    """Test tworzenia poprawnego pytania z różnymi konfiguracjami"""
    q1 = Question("Test?", ["A", "B"], 0)
    assert q1.text == "Test?"
    assert q1.options == ["A", "B"]
    assert q1.correct_index == 0
    assert q1.points == 1
    
    q2 = Question("  Spacja?  ", ["A", "B", "C"], 2, points=5)
    assert q2.text == "Spacja?"
    assert q2.points == 5


def test_question_empty_text():
    """Test walidacji pustego tekstu pytania"""
    with pytest.raises(InvalidQuestionError, match="Tekst pytania nie może być pusty"):
        Question("", ["A", "B"], 0)
    
    with pytest.raises(InvalidQuestionError, match="Tekst pytania nie może być pusty"):
        Question("   ", ["A", "B"], 0)


def test_question_invalid_options():
    """Test walidacji nieprawidłowych opcji odpowiedzi"""
    # Za mało opcji
    with pytest.raises(InvalidQuestionError, match="co najmniej 2 opcje"):
        Question("Test?", ["A"], 0)
    
    # Pusta lista
    with pytest.raises(InvalidQuestionError, match="co najmniej 2 opcje"):
        Question("Test?", [], 0)
    
    # Nie lista
    with pytest.raises(InvalidQuestionError, match="co najmniej 2 opcje"):
        Question("Test?", "AB", 0)
    
    # Pusta opcja
    with pytest.raises(InvalidQuestionError, match="niepustymi stringami"):
        Question("Test?", ["A", ""], 0)
    
    # Opcja ze spacjami
    with pytest.raises(InvalidQuestionError, match="niepustymi stringami"):
        Question("Test?", ["A", "   "], 0)


def test_question_invalid_correct_index():
    """Test walidacji nieprawidłowego indeksu poprawnej odpowiedzi"""
    # Indeks ujemny
    with pytest.raises(InvalidQuestionError, match="musi być w zakresie"):
        Question("Test?", ["A", "B"], -1)
    
    # Indeks poza zakresem
    with pytest.raises(InvalidQuestionError, match="musi być w zakresie"):
        Question("Test?", ["A", "B"], 2)
    
    # Nie integer
    with pytest.raises(InvalidQuestionError, match="musi być w zakresie"):
        Question("Test?", ["A", "B"], "0")


def test_question_invalid_points():
    """Test walidacji nieprawidłowej liczby punktów"""
    # Ujemne punkty
    with pytest.raises(InvalidQuestionError, match="Punkty muszą być liczbą dodatnią"):
        Question("Test?", ["A", "B"], 0, points=-1)
    
    # Zero punktów
    with pytest.raises(InvalidQuestionError, match="Punkty muszą być liczbą dodatnią"):
        Question("Test?", ["A", "B"], 0, points=0)
    
    # String zamiast liczby
    with pytest.raises(InvalidQuestionError, match="Punkty muszą być liczbą dodatnią"):
        Question("Test?", ["A", "B"], 0, points="5")


def test_question_is_correct_invalid_answer():
    """Test walidacji nieprawidłowego indeksu odpowiedzi"""
    q = Question("Test?", ["A", "B", "C"], 1)
    
    # Indeks ujemny
    with pytest.raises(InvalidAnswerError, match="musi być w zakresie"):
        q.is_correct(-1)
    
    # Indeks poza zakresem
    with pytest.raises(InvalidAnswerError, match="musi być w zakresie"):
        q.is_correct(3)
    
    # Nie integer
    with pytest.raises(InvalidAnswerError, match="musi być liczbą całkowitą"):
        q.is_correct("1")


# ===== TESTY KLASY QUIZ =====

def test_quiz_basic_flow():
    """Test podstawowego przepływu quizu"""
    questions = [
        Question("2+2=", ["3", "4", "5"], 1),
        Question("Stolica Polski?", ["Kraków", "Warszawa", "Gdańsk"], 1),
    ]
    quiz = Quiz(questions)
    quiz.start()
    
    assert quiz.get_current_question().text == "2+2="
    assert not quiz.is_finished()
    
    quiz.answer_current(1)  # poprawna odpowiedź
    assert quiz.score == 1
    assert quiz.current == 1
    
    quiz.answer_current(0)  # błędna odpowiedź
    assert quiz.score == 1
    assert quiz.is_finished()
    
    summary = quiz.get_summary()
    assert summary["score"] == 1
    assert summary["max_score"] == 2
    assert summary["answers"] == [1, 0]


def test_quiz_empty_questions():
    """Test tworzenia quizu z pustą listą pytań"""
    with pytest.raises(EmptyQuizError, match="co najmniej jedno pytanie"):
        Quiz([])


def test_quiz_invalid_questions_type():
    """Test walidacji typu listy pytań"""
    # Nie lista
    with pytest.raises(EmptyQuizError, match="przekazane jako lista"):
        Quiz("not a list")
    
    # Lista z nieprawidłowymi elementami
    with pytest.raises(InvalidQuestionError, match="obiektami Question"):
        Quiz([Question("Test?", ["A", "B"], 0), "not a question"])


def test_quiz_restart():
    """Test resetowania quizu"""
    questions = [
        Question("Q1", ["A", "B"], 0),
        Question("Q2", ["A", "B"], 1),
    ]
    quiz = Quiz(questions)
    quiz.start()
    
    quiz.answer_current(0)
    quiz.answer_current(1)
    assert quiz.is_finished()
    assert quiz.score == 2
    
    # Restart
    quiz.start()
    assert quiz.current == 0
    assert quiz.score == 0
    assert quiz.answers == [None, None]
    assert not quiz.is_finished()


def test_quiz_answer_after_finished():
    """Test próby odpowiedzi po zakończeniu quizu"""
    questions = [Question("Test?", ["A", "B"], 0)]
    quiz = Quiz(questions)
    quiz.start()
    
    quiz.answer_current(0)
    assert quiz.is_finished()
    
    # Próba odpowiedzi po zakończeniu
    with pytest.raises(QuizStateError, match="został już zakończony"):
        quiz.answer_current(0)


def test_quiz_answer_with_invalid_index():
    """Test odpowiedzi z nieprawidłowym indeksem"""
    questions = [Question("Test?", ["A", "B"], 0)]
    quiz = Quiz(questions)
    quiz.start()
    
    # Indeks poza zakresem
    with pytest.raises(InvalidAnswerError, match="musi być w zakresie"):
        quiz.answer_current(5)
    
    # Indeks ujemny
    with pytest.raises(InvalidAnswerError, match="musi być w zakresie"):
        quiz.answer_current(-1)


def test_quiz_different_points():
    """Test quizu z różnymi punktacjami pytań"""
    questions = [
        Question("Easy", ["A", "B"], 0, points=1),
        Question("Medium", ["A", "B"], 1, points=2),
        Question("Hard", ["A", "B"], 0, points=5),
    ]
    quiz = Quiz(questions)
    quiz.start()
    
    quiz.answer_current(0)  # 1 punkt
    quiz.answer_current(1)  # 2 punkty
    quiz.answer_current(1)  # 0 punktów (błędna)
    
    assert quiz.score == 3
    assert quiz.get_summary()["max_score"] == 8


def test_quiz_get_current_question_at_end():
    """Test pobierania bieżącego pytania na końcu quizu"""
    questions = [Question("Test?", ["A", "B"], 0)]
    quiz = Quiz(questions)
    quiz.start()
    
    quiz.answer_current(0)
    assert quiz.get_current_question() is None


# ===== TESTY KLASY QUIZBACKEND =====

def test_quiz_backend_basic():
    """Test podstawowej funkcjonalności backendu"""
    backend = QuizBackend()
    result = {"score": 2, "max_score": 2}
    
    backend.save_result("user1", result)
    assert backend.get_result("user1") == result
    assert backend.get_result("user2") is None


def test_quiz_backend_multiple_users():
    """Test obsługi wielu użytkowników"""
    backend = QuizBackend()
    
    backend.save_result("user1", {"score": 5})
    backend.save_result("user2", {"score": 8})
    backend.save_result("user3", {"score": 3})
    
    assert backend.get_result("user1") == {"score": 5}
    assert backend.get_result("user2") == {"score": 8}
    assert backend.get_result("user3") == {"score": 3}


def test_quiz_backend_overwrite_result():
    """Test nadpisywania wyniku użytkownika"""
    backend = QuizBackend()
    
    backend.save_result("user1", {"score": 5})
    assert backend.get_result("user1") == {"score": 5}
    
    backend.save_result("user1", {"score": 10})
    assert backend.get_result("user1") == {"score": 10}


def test_quiz_backend_invalid_user_id():
    """Test walidacji ID użytkownika"""
    backend = QuizBackend()
    
    # Pusty string
    with pytest.raises(ValueError, match="niepustym stringiem"):
        backend.save_result("", {"score": 5})
    
    with pytest.raises(ValueError, match="niepustym stringiem"):
        backend.save_result("   ", {"score": 5})
    
    # Nie string
    with pytest.raises(ValueError, match="niepustym stringiem"):
        backend.save_result(123, {"score": 5})
    
    # Get z pustym ID
    with pytest.raises(ValueError, match="niepustym stringiem"):
        backend.get_result("")


def test_quiz_backend_invalid_result_type():
    """Test walidacji typu wyniku"""
    backend = QuizBackend()
    
    # Nie dict
    with pytest.raises(ValueError, match="Wynik musi być słownikiem"):
        backend.save_result("user1", "not a dict")
    
    with pytest.raises(ValueError, match="Wynik musi być słownikiem"):
        backend.save_result("user1", [1, 2, 3])


def test_quiz_backend_whitespace_handling():
    """Test obsługi spacji w ID użytkownika"""
    backend = QuizBackend()
    
    backend.save_result("  user1  ", {"score": 5})
    assert backend.get_result("user1") == {"score": 5}
    assert backend.get_result("  user1  ") == {"score": 5}


# ===== TESTY INTEGRACYJNE =====

def test_full_quiz_scenario():
    """Test pełnego scenariusza użycia quizu"""
    # Przygotowanie pytań
    questions = [
        Question("Pytanie 1", ["A", "B", "C"], 0, points=1),
        Question("Pytanie 2", ["A", "B", "C"], 1, points=2),
        Question("Pytanie 3", ["A", "B", "C"], 2, points=3),
    ]
    
    # Utworzenie quizu
    quiz = Quiz(questions)
    backend = QuizBackend()
    
    # Rozpoczęcie quizu
    quiz.start()
    assert not quiz.is_finished()
    
    # Odpowiedzi użytkownika
    answers = [0, 1, 1]  # Prawidłowe: 1 i 2, błędne: 3
    for answer in answers:
        if not quiz.is_finished():
            quiz.answer_current(answer)
    
    # Podsumowanie
    assert quiz.is_finished()
    summary = quiz.get_summary()
    assert summary["score"] == 3  # 1 + 2 + 0
    assert summary["max_score"] == 6
    
    # Zapis wyniku
    backend.save_result("test_user", summary)
    saved = backend.get_result("test_user")
    assert saved["score"] == 3


def test_edge_case_single_question():
    """Test quizu z tylko jednym pytaniem"""
    questions = [Question("Tylko jedno?", ["Tak", "Nie"], 0)]
    quiz = Quiz(questions)
    quiz.start()
    
    assert not quiz.is_finished()
    quiz.answer_current(0)
    assert quiz.is_finished()
    assert quiz.score == 1


def test_edge_case_many_options():
    """Test pytania z wieloma opcjami"""
    options = [f"Opcja {i}" for i in range(20)]
    q = Question("Które to?", options, 15, points=10)
    
    assert q.is_correct(15)
    assert not q.is_correct(14)
    assert not q.is_correct(16)


# ===== TESTY WYDAJNOŚCIOWE / SKRAJNE =====

def test_large_quiz():
    """Test quizu z dużą liczbą pytań"""
    questions = [
        Question(f"Q{i}", ["A", "B"], i % 2, points=1)
        for i in range(100)
    ]
    quiz = Quiz(questions)
    quiz.start()
    
    for i in range(100):
        quiz.answer_current(i % 2)
    
    assert quiz.is_finished()
    assert quiz.score == 100
    summary = quiz.get_summary()
    assert len(summary["answers"]) == 100
