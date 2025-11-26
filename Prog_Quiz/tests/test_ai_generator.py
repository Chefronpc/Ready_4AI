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

# --- Testy walidacji odpowiedzi AI ---
@patch('ai_generator.requests')
def test_generate_quiz_missing_question_key(mock_requests):
    """Test: brak klucza 'question' w odpowiedzi powinien wywołać InvalidModelResponseError"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        "a": "Opcja A",
        "b": "Opcja B",
        "c": "Opcja C",
        "d": "Opcja D",
        "correct": "a"
    }]
    mock_requests.post.return_value = mock_response
    
    with pytest.raises(InvalidModelResponseError):
        generate_quiz("Python", 1)


@patch('ai_generator.requests')
def test_generate_quiz_missing_choices(mock_requests):
    """Test: brak opcji odpowiedzi powinien wywołać InvalidModelResponseError"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        "question": "Test?",
        "a": "Opcja A",
        "b": "Opcja B",
        # brak 'c' i 'd'
        "correct": "a"
    }]
    mock_requests.post.return_value = mock_response
    
    with pytest.raises(InvalidModelResponseError):
        generate_quiz("Python", 1)


@pytest.mark.parametrize("invalid_correct", ["e", "f", "x", "1", "", "ab"])
@patch('ai_generator.requests')
def test_generate_quiz_invalid_correct_value(mock_requests, invalid_correct):
    """Test: nieprawidłowa wartość 'correct' powinna wywołać InvalidModelResponseError"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        "question": "Test?",
        "a": "Opcja A",
        "b": "Opcja B",
        "c": "Opcja C",
        "d": "Opcja D",
        "correct": invalid_correct
    }]
    mock_requests.post.return_value = mock_response
    
    with pytest.raises(InvalidModelResponseError):
        generate_quiz("Python", 1)


@patch('ai_generator.requests')
def test_generate_quiz_wrong_number_of_questions(mock_requests, valid_quiz_item):
    """Test: AI zwraca nieprawidłową liczbę pytań"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Oczekujemy 5 pytań, ale AI zwraca 3
    mock_response.json.return_value = [valid_quiz_item] * 3
    mock_requests.post.return_value = mock_response
    
    with pytest.raises(InvalidModelResponseError):
        generate_quiz("Python", 5)


# --- Testy obsługi błędów komunikacji ---
@patch('ai_generator.requests')
def test_generate_quiz_api_connection_error(mock_requests):
    """Test: błąd połączenia z API powinien wywołać AIServiceError"""
    mock_requests.post.side_effect = ConnectionError("Network error")
    
    with pytest.raises(AIServiceError):
        generate_quiz("Python", 5)


@patch('ai_generator.requests')
def test_generate_quiz_api_timeout(mock_requests):
    """Test: timeout API powinien wywołać AIServiceError"""
    mock_requests.post.side_effect = TimeoutError("Request timeout")
    
    with pytest.raises(AIServiceError):
        generate_quiz("Python", 5)


@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 500, 502, 503])
@patch('ai_generator.requests')
def test_generate_quiz_api_error_status_codes(mock_requests, status_code):
    """Test: błędne kody statusu HTTP powinny wywołać AIServiceError"""
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.raise_for_status.side_effect = Exception(f"HTTP {status_code}")
    mock_requests.post.return_value = mock_response
    
    with pytest.raises(AIServiceError):
        generate_quiz("Python", 5)


@patch('ai_generator.requests')
def test_generate_quiz_invalid_json_response(mock_requests):
    """Test: nieprawidłowy JSON w odpowiedzi powinien wywołać InvalidModelResponseError"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_requests.post.return_value = mock_response
    
    with pytest.raises(InvalidModelResponseError):
        generate_quiz("Python", 5)


@patch('ai_generator.requests')
def test_generate_quiz_non_list_response(mock_requests):
    """Test: odpowiedź nie będąca listą powinna wywołać InvalidModelResponseError"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": "not a list"}
    mock_requests.post.return_value = mock_response
    
    with pytest.raises(InvalidModelResponseError):
        generate_quiz("Python", 5)


# --- Testy walidacji wszystkich kluczy ---
@pytest.mark.parametrize("missing_key", ["a", "b", "c", "d", "correct"])
@patch('ai_generator.requests')
def test_generate_quiz_missing_required_keys(mock_requests, missing_key):
    """Test: brak wymaganego klucza powinien wywołać InvalidModelResponseError"""
    quiz_item = {
        "question": "Test?",
        "a": "Opcja A",
        "b": "Opcja B",
        "c": "Opcja C",
        "d": "Opcja D",
        "correct": "a"
    }
    # Usuń jeden klucz
    del quiz_item[missing_key]
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [quiz_item]
    mock_requests.post.return_value = mock_response
    
    with pytest.raises(InvalidModelResponseError):
        generate_quiz("Python", 1)


# --- Testy poprawności formatowania danych ---
@patch('ai_generator.requests')
def test_generate_quiz_all_correct_values_valid(mock_requests):
    """Test: wszystkie prawidłowe wartości 'correct' (a, b, c, d) powinny być akceptowane"""
    valid_items = [
        {
            "question": f"Pytanie {i}?",
            "a": "Opcja A",
            "b": "Opcja B",
            "c": "Opcja C",
            "d": "Opcja D",
            "correct": correct_value
        }
        for i, correct_value in enumerate(['a', 'b', 'c', 'd'], 1)
    ]
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = valid_items
    mock_requests.post.return_value = mock_response
    
    result = generate_quiz("Python", 4)
    
    assert len(result) == 4
    assert result[0]["correct"] == "a"
    assert result[1]["correct"] == "b"
    assert result[2]["correct"] == "c"
    assert result[3]["correct"] == "d"


# --- Testy integracyjne (jeśli implementacja jest gotowa) ---
@pytest.mark.skip(reason="Wymaga implementacji generate_quiz i prawdziwego API")
def test_generate_quiz_integration_with_real_api():
    """Test integracyjny z prawdziwym API (do odznaczenia po implementacji)"""
    result = generate_quiz("Python basics", 3)
    
    assert len(result) == 3
    assert all(item["correct"] in ["a", "b", "c", "d"] for item in result)
    assert all(len(item["question"]) > 0 for item in result)