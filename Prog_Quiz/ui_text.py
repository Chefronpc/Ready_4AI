import os
from typing import Dict, Literal


class UITextInterface:
    """
    Interfejs użytkownika tekstowy dla aplikacji Quiz.
    Obsługuje komunikację CLI z czyszczeniem ekranu między etapami.
    """
    
    # Stałe konfiguracyjne
    SCREEN_WIDTH: int = 80
    HEADER_CHAR: str = "="
    SUBHEADER_CHAR: str = "-"
    
    def __init__(self) -> None:
        """Inicjalizuje interfejs użytkownika."""
        self._current_stage: str = "init"
    
    def _clear_screen(self) -> None:
        """Czyści ekran konsoli (Windows lub Unix)."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _print_header(self, title: str, info_text: str = "") -> None:
        """
        Wyświetla nagłówek z tytułem i tekstem informacyjnym.
        
        Args:
            title: Tytuł nagłówka
            info_text: Dodatkowy tekst informacyjny
        """
        self._clear_screen()
        print(self.HEADER_CHAR * self.SCREEN_WIDTH)
        print(f"  {title.upper()}")
        print(self.HEADER_CHAR * self.SCREEN_WIDTH)
        
        if info_text:
            print(f"  ℹ️  {info_text}")
            print(self.SUBHEADER_CHAR * self.SCREEN_WIDTH)
        print()
    
    def _print_footer(self) -> None:
        """Wyświetla stopkę."""
        print()
        print(self.HEADER_CHAR * self.SCREEN_WIDTH)
    
    def _get_valid_input(
        self,
        prompt: str,
        validation_fn=None,
        error_msg: str = "Niepoprawne dane wejściowe. Spróbuj ponownie."
    ) -> str:
        """
        Pobiera od użytkownika wejście z walidacją.
        
        Args:
            prompt: Tekst pytania
            validation_fn: Funkcja walidująca (opcjonalnie)
            error_msg: Komunikat błędu
            
        Returns:
            Zwalidowana wartość wejścia
        """
        while True:
            user_input = input(prompt).strip()
            
            if validation_fn is None:
                if user_input:
                    return user_input
            else:
                if validation_fn(user_input):
                    return user_input
            
            print(f"❌ {error_msg}")
            print()
    
    def display_welcome(self) -> None:
        """Wyświetla ekran powitania."""
        self._current_stage = "welcome"
        self._print_header(
            "Witaj w Quiz AI",
            "Interaktywny system pytań z wykorzystaniem sztucznej inteligencji"
        )
        
        welcome_message = """
        📚 Funkcjonalności:
           • Generowanie pytań z wybranego tematu
           • Test jednokrotnego wyboru
           • Raport z wynikami
           
        🎯 Jak zacząć:
           Naciśnij ENTER aby przejść dalej...
        """
        print(welcome_message)
        self._print_footer()
        
        input("  ➜ ")
    
    def ask_topic(self) -> str:
        """
        Pytany użytkownika o temat quizu.
        
        Returns:
            Temat wybrany przez użytkownika
        """
        self._current_stage = "topic_selection"
        self._print_header(
            "Wybór Tematu",
            "Podaj temat, z którego chcesz odpowiadać na pytania"
        )
        
        print("  Przykłady tematów: Python, Historia, Biologia, Matematyka...\n")
        
        topic = self._get_valid_input(
            "  ➜ Temat: ",
            validation_fn=lambda x: len(x) > 0,
            error_msg="Temat nie może być pusty."
        )
        
        print(f"\n  ✓ Wybrany temat: '{topic}'")
        self._print_footer()
        input("  Naciśnij ENTER aby kontynuować...")
        
        return topic
    
    def ask_number_of_questions(self, min_q: int, max_q: int) -> int:
        """
        Pytany użytkownika o liczbę pytań w quizie.
        
        Args:
            min_q: Minimalna liczba pytań
            max_q: Maksymalna liczba pytań
            
        Returns:
            Liczba pytań wybrana przez użytkownika
        """
        self._current_stage = "question_count"
        self._print_header(
            "Liczba Pytań",
            f"Wybierz liczbę pytań z zakresu {min_q}-{max_q}"
        )
        
        def validate_count(value: str) -> bool:
            try:
                num = int(value)
                return min_q <= num <= max_q
            except ValueError:
                return False
        
        error_msg = f"Wpisz liczbę z zakresu {min_q} do {max_q}."
        
        num_questions = int(self._get_valid_input(
            f"  ➜ Liczba pytań ({min_q}-{max_q}): ",
            validation_fn=validate_count,
            error_msg=error_msg
        ))
        
        print(f"\n  ✓ Liczba pytań: {num_questions}")
        self._print_footer()
        input("  Naciśnij ENTER aby przystąpić do quizu...")
        
        return num_questions
    
    def display_question(
        self,
        index: int,
        question: str,
        choices: Dict[Literal['a', 'b', 'c', 'd'], str]
    ) -> None:
        """
        Wyświetla pytanie z opcjami odpowiedzi.
        
        Args:
            index: Numer pytania (liczony od 1)
            question: Treść pytania
            choices: Słownik opcji (klucze: 'a', 'b', 'c', 'd')
        """
        self._current_stage = f"question_{index}"
        self._print_header(
            f"Pytanie {index}",
            f"Zaznacz poprawną odpowiedź (A, B, C lub D)"
        )
        
        print(f"  {question}\n")
        print("  Opcje:")
        
        option_labels = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}
        for key in ['a', 'b', 'c', 'd']:
            if key in choices:
                print(f"    {option_labels[key]}) {choices[key]}")
        
        print()
    
    def get_user_choice(self) -> str:
        """
        Pobiera od użytkownika wybór odpowiedzi.
        
        Returns:
            Wybrana odpowiedź ('a', 'b', 'c' lub 'd')
        """
        valid_choices = {'a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'}
        
        choice = self._get_valid_input(
            "  ➜ Twoja odpowiedź: ",
            validation_fn=lambda x: x in valid_choices,
            error_msg="Wybierz A, B, C lub D."
        )
        
        return choice.lower()
    
    def show_answer_feedback(
        self,
        is_correct: bool,
        user_choice: str,
        correct_choice: str,
        correct_text: str
    ) -> None:
        """
        Wyświetla informację zwrotną o odpowiedzi.
        
        Args:
            is_correct: Czy odpowiedź była poprawna
            user_choice: Wybór użytkownika
            correct_choice: Poprawna odpowiedź
            correct_text: Tekst poprawnej odpowiedzi
        """
        print()
        if is_correct:
            print(f"  ✅ POPRAWNIE! Twoja odpowiedź '{user_choice.upper()}' jest prawidłowa.")
        else:
            print(f"  ❌ BŁĘDNIE! Wybrałeś '{user_choice.upper()}', prawidłowa to '{correct_choice.upper()}'")
            print(f"     Poprawna odpowiedź: {correct_text}")
        
        print()
        input("  Naciśnij ENTER aby przejść do następnego pytania...")
    
    def display_final_report(self, report_text: str) -> None:
        """
        Wyświetla raport końcowy z wynikami.
        
        Args:
            report_text: Tekst raportu
        """
        self._current_stage = "final_report"
        self._print_header(
            "Raport Wyników",
            "Podsumowanie Twojego quizu"
        )
        
        print(report_text)
        self._print_footer()
        
        input("  Naciśnij ENTER aby zakończyć...")
    
    def show_message(self, message: str, message_type: str = "info") -> None:
        """
        Wyświetla komunikat do użytkownika.
        
        Args:
            message: Treść komunikatu
            message_type: Typ komunikatu ('info', 'success', 'error', 'warning')
        """
        icons = {
            'info': 'ℹ️ ',
            'success': '✅ ',
            'error': '❌ ',
            'warning': '⚠️ '
        }
        
        icon = icons.get(message_type, 'ℹ️ ')
        print(f"\n  {icon}{message}\n")

