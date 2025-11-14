class UITextInterface:

    def display_welcome(self) -> None:
        pass

    def ask_topic(self) -> str:
        pass

    def ask_number_of_questions(self, min_q: int, max_q:int) -> int:
        pass

    def display_question(self, index: int, question: str, choices: dict) -> None:
        pass

    def get_user_choice(self) -> str:
        pass

    def display_final_report(self, report_text: str) -> None:
        pass

