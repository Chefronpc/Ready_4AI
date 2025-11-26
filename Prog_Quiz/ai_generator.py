from typing import List, TypedDict, Literal
import requests
from config import MIN_QUESTIONS, MAX_QUESTIONS, AI_API_URL, AI_API_KEY

EXPECTED_QUESTION_KEYS = ("question", "a", "b", "c", "d", "correct")

class QuizItem(TypedDict):
    question: str
    a: str
    b: str
    c: str
    d: str
    correct: Literal['a', 'b', 'c', 'd']

class AIServiceError(Exception):
    pass

class InvalidModelResponseError(Exception):
    pass

class AIGenerator:
    """
    Klasa do generowania quizów za pomocą modelu AI OpenAI.
    """
    def __init__(self, api_url: str = AI_API_URL, api_key: str = AI_API_KEY):
        self.api_url = api_url
        self.api_key = api_key


    def generate_quiz(self, topic: str, n_questions: int) -> List[QuizItem]:
        """
        Generuje quiz na zadany temat i liczbę pytań przez API OpenAI.
        """
        self._validate_input(topic, n_questions)
        return self._generate_quiz_api(topic, n_questions)


    def _validate_input(self, topic: str, n_questions: int) -> None:
        if not topic or not topic.strip():
            raise ValueError("Temat nie może być pusty.")
        if not (MIN_QUESTIONS <= n_questions <= MAX_QUESTIONS):
            raise ValueError(f"Liczba pytań musi być w zakresie {MIN_QUESTIONS}-{MAX_QUESTIONS}.)")


    def _generate_quiz_api(self, topic: str, n_questions: int) -> List[QuizItem]:
        """
        Generuje pytania quizowe przez API OpenAI (lub inne AI).
        """
        if not self.api_url or not self.api_key:
            raise AIServiceError("Brak konfiguracji API (url/klucz)")
        payload = {
            "topic": topic,
            "n_questions": n_questions,
            "format": "json",
            "expected_keys": EXPECTED_QUESTION_KEYS
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            try:
                data = response.json()
            except ValueError as ve:
                raise InvalidModelResponseError(f"Nieprawidłowy JSON w odpowiedzi API: {ve}")
        except InvalidModelResponseError:
            raise
        except Exception as e:
            raise AIServiceError(f"Błąd komunikacji z API: {e}")

        if not isinstance(data, list):
            raise InvalidModelResponseError("Odpowiedź API nie jest listą pytań.")
        if len(data) != n_questions:
            raise InvalidModelResponseError(f"API zwróciło {len(data)} pytań zamiast oczekiwanych {n_questions}.")
        quiz: List[QuizItem] = []
        for item in data:
            self._validate_quiz_item(item)
            quiz.append(item)
        return quiz


    def _validate_quiz_item(self, item: dict) -> None:
        for key in EXPECTED_QUESTION_KEYS:
            if key not in item:
                raise InvalidModelResponseError(f"Brak klucza '{key}' w pytaniu.")
        if item["correct"] not in {"a", "b", "c", "d"}:
            raise InvalidModelResponseError("Klucz 'correct' musi być jedną z liter: a, b, c, d.")
        for opt in ["a", "b", "c", "d"]:
            if not item[opt]:
                raise InvalidModelResponseError(f"Odpowiedź '{opt}' nie może być pusta.")

# Szybki alias do użycia w innych modułach
generate_quiz = AIGenerator().generate_quiz