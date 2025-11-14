from typing import List,TypedDict


class QuizItem(TypedDict):
    question: str
    a: str
    b: str
    c: str
    d: str
    correct: str    # 'a'|'b'|'c'|'d'


class AIServiceError(Exception):
    pass

class InvalidModelResponseError(Exception):
    pass


def generate_quiz(topic: str, n_questions: int) -> List[QuizItem]:
    pass

    """
    Wywołuje model AI i zwraca listę pytań.

    Walidacja:
    - topic nie może być pusty
    - n_questions w MIN_QUESTIONS..MAX_QUESTIONS
    - każdy QuizItem ma wszystkie klucze EXPECTED_QUESTION_KEYS
    - 'correct' ∈ {'a','b','c','d'}

    Wyjątki:
    - AIServiceError dla błędów komunikacji
    - InvalidModelResponseError dla niepoprawnego formatu odpowiedzi
    """