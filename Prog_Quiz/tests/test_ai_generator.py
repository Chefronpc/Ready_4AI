from unittest.mock import MagicMock, patch
import pytest

from ai_generator import AIServiceError, InvalidModelResponseError, QuizItem, generate_quiz
from config import MAX_QUESTIONS, MIN_QUESTIONS


# --- Fixtures ---
@pytest.fixture
def valid_quiz_item() -> QuizItem:
    """Zwraca przykładowy poprawny obiekt QuizItem."""
    return QuizItem(
        question="What is the capital of France?",
        a="Berlin",
        b="Madrid",
        c="Paris",
        d="Rome",
        correct="b"
    )
    

@pytest.fixture
def valid_quiz_response(valid_quiz_item: QuizItem) -> list:
    """Zwraca przykładową poprawną odpowiedź z AI jako lista słowników."""
    return [
        valid_quiz_item,
        {
            "question": "What is 2 + 2?",
            "a": "3",
            "b": "4",
            "c": "5",
            "d": "6",
            "correct": "b"
        },
        {
            "question": "What is the largest planet in our solar system?",
            "a": "Earth",
            "b": "Mars",
            "c": "Jupiter",
            "d": "Saturn",
            "correct": "c"
        }
    ]


# --- Testy walidacji wejścia ----
def test_generate_quiz_empty_topic():
    """Test: pusty temat powinien wywołać wyjątek"""
    with pytest.raises((ValueError, AIServiceError, InvalidModelResponseError)):
        generate_quiz("",5)


def test_generate_quiz_whitespace_topic():
    """Test: temat z samymi spacjami powinien wywołać wyjątek"""
    with pytest.raises((ValueError, AIServiceError, InvalidModelResponseError)):
        generate_quiz("   ",5)


@pytest.mark.parametrize("n_questions", [MIN_QUESTIONS - 1, 0, -1, -10])
def test_generate_quiz_below_min_question(n_questions: int):
    """Test: liczba pytań poniżej MIN_QUESTIONS powinna wywołać wyjątek"""
    with pytest.raises((ValueError, AIServiceError, InvalidModelResponseError)):
        generate_quiz("Python", n_questions)


@pytest.mark.parametrize("n_questions", [MAX_QUESTIONS + 1, MAX_QUESTIONS + 10, 100])
def test_generate_quiz_above_max_questions(n_questions: int):
    """Test: liczba pytań powyżej MAX_QUESTIONS powinna wywołać wyjątek"""
    with pytest.raises((ValueError, AIServiceError, InvalidModelResponseError)):
        generate_quiz("Python", n_questions)


# --- Testy prawidłowego działania ---
@patch('ai_generator.requests')  # Użycie requst do komunikacji z API
def test_generate_quiz_valid_input(mock_requests, valid_quiz_response: list):
    """Test: prawidłowe wejście powinno zwrócić poprawną listę QuizItem"""
    # Mockowanie odpowiedzi z AI
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = valid_quiz_response
    mock_requests.post.return_value = mock_response

    result = generate_quiz("Python", 3)
        
    assert isinstance(result, list)
    assert len(result) == 3
    for item in result:
        assert isinstance(item, dict)
        assert all(key in item for key in ["question", "a", "b", "c", "d", "correct"])
        assert item["correct"] in ["a", "b", "c", "d"]

    # Wersja "dyskretna" - Do zweryfikowania
    """
        assert isinstance(item, dict)
        assert "question" in item
        assert "a" in item
        assert "b" in item
        assert "c" in item
        assert "d" in item
        assert "correct" in item
    """


@pytest.mark.parametrize("n_questions", [MIN_QUESTIONS, MIN_QUESTIONS + 5, MAX_QUESTIONS - 5, MAX_QUESTIONS])
@patch('ai_generator.requests')
def test_generate_quiz_boundary_questions(mock_requests, valid_quiz_item: QuizItem, n_questions: int):
    """Test: Liczba pytań na granicach zakresu powinna działać poprawnie"""
    # Mock odpowiedzi z odpowiednią liczbą pytań
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [valid_quiz_item] * n_questions
    mock_requests.post.return_value = mock_response

    result = generate_quiz("Python", n_questions)

    assert len(result) == n_questions

