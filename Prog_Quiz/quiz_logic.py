from typing import Iterable, List, Tuple, Dict

from ui_text import UITextInterface
from ai_generator import QuizItem

def run_quiz(quiz_item: Iterable[Dict], ui) -> Tuple[int, int, List[Dict]]:
    pass

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