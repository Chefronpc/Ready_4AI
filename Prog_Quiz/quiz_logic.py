# Moduł logiki quizu zgodny z założeniami agentów
# Autor: Ready_4AI

from typing import List, Dict, Optional


# Własne wyjątki dla lepszej obsługi błędów
class QuizException(Exception):
    """Bazowy wyjątek dla błędów quizu"""
    pass


class InvalidQuestionError(QuizException):
    """Błąd nieprawidłowego pytania (puste opcje, zły indeks)"""
    pass


class InvalidAnswerError(QuizException):
    """Błąd nieprawidłowej odpowiedzi (indeks poza zakresem)"""
    pass


class QuizStateError(QuizException):
    """Błąd stanu quizu (np. próba odpowiedzi po zakończeniu)"""
    pass


class EmptyQuizError(QuizException):
    """Błąd pustego quizu (brak pytań)"""
    pass


class Question:
    def __init__(self, text: str, options: List[str], correct_index: int, points: int = 1):
        # Walidacja danych wejściowych
        if not isinstance(text, str) or not text.strip():
            raise InvalidQuestionError("Tekst pytania nie może być pusty")
        
        if not isinstance(options, list) or len(options) < 2:
            raise InvalidQuestionError("Pytanie musi mieć co najmniej 2 opcje odpowiedzi")
        
        if not all(isinstance(opt, str) and opt.strip() for opt in options):
            raise InvalidQuestionError("Wszystkie opcje muszą być niepustymi stringami")
        
        if not isinstance(correct_index, int) or correct_index < 0 or correct_index >= len(options):
            raise InvalidQuestionError(
                f"Indeks prawidłowej odpowiedzi ({correct_index}) musi być w zakresie 0-{len(options)-1}"
            )
        
        if not isinstance(points, (int, float)) or points <= 0:
            raise InvalidQuestionError("Punkty muszą być liczbą dodatnią")
        
        self.text = text.strip()
        self.options = [opt.strip() for opt in options]
        self.correct_index = correct_index
        self.points = points

    def is_correct(self, answer_index: int) -> bool:
        if not isinstance(answer_index, int):
            raise InvalidAnswerError("Indeks odpowiedzi musi być liczbą całkowitą")
        
        if answer_index < 0 or answer_index >= len(self.options):
            raise InvalidAnswerError(
                f"Indeks odpowiedzi ({answer_index}) musi być w zakresie 0-{len(self.options)-1}"
            )
        
        return answer_index == self.correct_index

class Quiz:
    def __init__(self, questions: List[Question]):
        # Walidacja listy pytań
        if not isinstance(questions, list):
            raise EmptyQuizError("Pytania muszą być przekazane jako lista")
        
        if len(questions) == 0:
            raise EmptyQuizError("Quiz musi zawierać co najmniej jedno pytanie")
        
        if not all(isinstance(q, Question) for q in questions):
            raise InvalidQuestionError("Wszystkie elementy muszą być obiektami Question")
        
        self.questions = questions
        self.current = 0
        self.score = 0
        self.answers: List[Optional[int]] = [None] * len(questions)

    def start(self):
        self.current = 0
        self.score = 0
        self.answers = [None] * len(self.questions)

    def get_current_question(self) -> Optional[Question]:
        if self.current < len(self.questions):
            return self.questions[self.current]
        return None

    def answer_current(self, answer_index: int):
        if self.is_finished():
            raise QuizStateError("Quiz został już zakończony, nie można już odpowiadać")
        
        question = self.get_current_question()
        if question is None:
            raise QuizStateError("Brak bieżącego pytania")
        
        # Walidacja odpowiedzi delegowana do Question.is_correct()
        try:
            is_correct = question.is_correct(answer_index)
            self.answers[self.current] = answer_index
            if is_correct:
                self.score += question.points
            self.current += 1
            return True
        except InvalidAnswerError:
            raise  # Przepuszczamy wyjątek walidacji odpowiedzi

    def is_finished(self) -> bool:
        return self.current >= len(self.questions)

    def get_summary(self) -> Dict[str, any]:
        return {
            "score": self.score,
            "max_score": sum(q.points for q in self.questions),
            "answers": self.answers,
            "questions": [q.text for q in self.questions]
        }

# Interfejs do backendu/bazy danych (stub)
class QuizBackend:
    def __init__(self):
        self._db = {}

    def save_result(self, user_id: str, result: Dict):
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("ID użytkownika musi być niepustym stringiem")
        
        if not isinstance(result, dict):
            raise ValueError("Wynik musi być słownikiem")
        
        self._db[user_id.strip()] = result

    def get_result(self, user_id: str) -> Optional[Dict]:
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("ID użytkownika musi być niepustym stringiem")
        
        return self._db.get(user_id.strip())

# Przykładowe użycie i testy
def example_quiz():
    questions = [
        Question("2+2=", ["3", "4", "5"], 1),
        Question("Stolica Polski?", ["Kraków", "Warszawa", "Gdańsk"], 1),
    ]
    quiz = Quiz(questions)
    quiz.start()
    while not quiz.is_finished():
        q = quiz.get_current_question()
        # Symulacja odpowiedzi: zawsze wybieramy pierwszą opcję
        quiz.answer_current(0)
    return quiz.get_summary()

if __name__ == "__main__":
    print("Test quizu:", example_quiz())

"""
Przeprowadza quiz.

ui: obiekt UI_Text implementujący:
    - display_question(index:int, question:str, choices:dict)
    - get_user_choice() -> str
    - show_message(msg: str)

Zwraca:
- liczba_poprawnych: int
- liczba_blednych: int
- lista_blednych: [{"index": idx, "user": 'a'..'d', "correct": 'a'..'d', "question_item": QuizItem}]
"""