#!/usr/bin/env python3
"""
Główny plik aplikacji Quiz AI
Integruje wszystkie moduły i zapewnia przepływ aplikacji
"""

from typing import List, Dict, Literal
import sys

from config import MIN_QUESTIONS, MAX_QUESTIONS
from ui_text import UITextInterface
from ai_generator import AIGenerator, AIServiceError, InvalidModelResponseError, QuizItem
from quiz_logic import Question, Quiz, QuizException, InvalidQuestionError, InvalidAnswerError
from result_procesor import build_report


class QuizApplication:
    """Główna klasa aplikacji Quiz"""
    
    def __init__(self):
        self.ui = UITextInterface()
        self.ai_generator = AIGenerator()
        self.quiz = None
        self.quiz_data: List[QuizItem] = []
        self.results = {
            'correct': 0,
            'wrong': 0,
            'wrong_items': []
        }
    
    def run(self):
        """Główna pętla aplikacji"""
        try:
            # 1. Ekran powitalny
            self.ui.display_welcome()
            
            # 2. Wybór tematu
            topic = self.ui.ask_topic()
            
            # 3. Wybór liczby pytań
            num_questions = self.ui.ask_number_of_questions(MIN_QUESTIONS, MAX_QUESTIONS)
            
            # 4. Generowanie pytań przez AI
            self.ui.show_message("Generowanie pytań... Proszę czekać.", "info")
            try:
                self.quiz_data = self.ai_generator.generate_quiz(topic, num_questions)
            except (AIServiceError, InvalidModelResponseError) as e:
                self.ui.show_message(f"Błąd generowania pytań: {e}", "error")
                return
            except Exception as e:
                self.ui.show_message(f"Nieoczekiwany błąd: {e}", "error")
                return
            
            # 5. Konwersja do formatu quiz_logic
            questions = self._convert_to_questions(self.quiz_data)
            
            # 6. Utworzenie i uruchomienie quizu
            try:
                self.quiz = Quiz(questions)
                self.quiz.start()
            except QuizException as e:
                self.ui.show_message(f"Błąd inicjalizacji quizu: {e}", "error")
                return
            
            # 7. Przeprowadzenie quizu
            self._run_quiz()
            
            # 8. Wyświetlenie raportu końcowego
            self._show_final_report()
            
        except KeyboardInterrupt:
            self.ui.show_message("\nAplikacja przerwana przez użytkownika.", "warning")
            sys.exit(0)
        except Exception as e:
            self.ui.show_message(f"Krytyczny błąd aplikacji: {e}", "error")
            sys.exit(1)
    
    def _convert_to_questions(self, quiz_data: List[QuizItem]) -> List[Question]:
        """
        Konwertuje dane z AI (QuizItem) do obiektów Question
        
        Args:
            quiz_data: Lista pytań z AI w formacie QuizItem
            
        Returns:
            Lista obiektów Question
        """
        questions = []
        letter_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        
        for item in quiz_data:
            try:
                options = [item['a'], item['b'], item['c'], item['d']]
                correct_index = letter_to_index[item['correct']]
                
                question = Question(
                    text=item['question'],
                    options=options,
                    correct_index=correct_index,
                    points=1
                )
                questions.append(question)
            except (KeyError, InvalidQuestionError) as e:
                self.ui.show_message(f"Błąd przetwarzania pytania: {e}", "error")
                continue
        
        return questions
    
    def _run_quiz(self):
        """Przeprowadza quiz, zadając kolejne pytania"""
        question_num = 1
        
        while not self.quiz.is_finished():
            current_question = self.quiz.get_current_question()
            if current_question is None:
                break
            
            # Pobierz oryginalne dane pytania (dla feedbacku)
            original_item = self.quiz_data[self.quiz.current]
            
            # Przygotuj opcje dla UI
            choices = {
                'a': current_question.options[0],
                'b': current_question.options[1],
                'c': current_question.options[2],
                'd': current_question.options[3]
            }
            
            # Wyświetl pytanie
            self.ui.display_question(question_num, current_question.text, choices)
            
            # Pobierz odpowiedź użytkownika
            user_choice = self.ui.get_user_choice()
            
            # Konwertuj literę na indeks
            letter_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
            user_index = letter_to_index[user_choice]
            
            # Sprawdź poprawność przed zapisaniem odpowiedzi
            is_correct = current_question.is_correct(user_index)
            
            # Zapisz odpowiedź w quizie
            try:
                self.quiz.answer_current(user_index)
            except (InvalidAnswerError, QuizException) as e:
                self.ui.show_message(f"Błąd zapisu odpowiedzi: {e}", "error")
                continue
            
            # Pokaż feedback
            correct_choice = original_item['correct']
            correct_text = original_item[correct_choice]
            
            self.ui.show_answer_feedback(
                is_correct=is_correct,
                user_choice=user_choice,
                correct_choice=correct_choice,
                correct_text=correct_text
            )
            
            # Zapisz wynik
            if is_correct:
                self.results['correct'] += 1
            else:
                self.results['wrong'] += 1
                self.results['wrong_items'].append({
                    'index': question_num,
                    'user': user_choice,
                    'correct': correct_choice,
                    'question': current_question.text,
                    'correct_text': correct_text
                })
            
            question_num += 1
    
    def _show_final_report(self):
        """Generuje i wyświetla raport końcowy"""
        total_questions = len(self.quiz.questions)
        
        # Użyj result_procesor do wygenerowania raportu
        report_text = self._build_custom_report(
            total=total_questions,
            correct=self.results['correct'],
            wrong_items=self.results['wrong_items']
        )
        
        self.ui.display_final_report(report_text)
    
    def _build_custom_report(self, total: int, correct: int, wrong_items: List[Dict]) -> str:
        """
        Tworzy raport tekstowy z wynikami quizu
        
        Args:
            total: Liczba wszystkich pytań
            correct: Liczba poprawnych odpowiedzi
            wrong_items: Lista błędnych odpowiedzi
            
        Returns:
            Sformatowany raport tekstowy
        """
        wrong = len(wrong_items)
        percentage = (correct / total * 100) if total > 0 else 0
        
        # Nagłówek
        report = f"""
  📊 Statystyki:
     • Wszystkie pytania: {total}
     • Poprawne odpowiedzi: {correct}
     • Błędne odpowiedzi: {wrong}
     • Wynik procentowy: {percentage:.1f}%
"""
        
        # Ocena
        if percentage >= 90:
            grade = "🏆 DOSKONALE!"
        elif percentage >= 75:
            grade = "🎉 BARDZO DOBRZE!"
        elif percentage >= 60:
            grade = "👍 DOBRZE!"
        elif percentage >= 50:
            grade = "📚 ŚREDNIO - POTRZEBA WIĘCEJ NAUKI"
        else:
            grade = "💪 NIE PODDAWAJ SIĘ - ĆWICZ DALEJ!"
        
        report += f"\n  🎯 Ocena: {grade}\n"
        
        # Lista błędów
        if wrong_items:
            report += f"\n  ❌ Błędne odpowiedzi:\n"
            for item in wrong_items:
                report += f"\n     Pytanie {item['index']}: {item['question']}\n"
                report += f"     • Twoja odpowiedź: {item['user'].upper()}\n"
                report += f"     • Poprawna odpowiedź: {item['correct'].upper()} - {item['correct_text']}\n"
        else:
            report += f"\n  🌟 Gratulacje! Wszystkie odpowiedzi były poprawne!\n"
        
        return report


def main():
    """Punkt wejścia aplikacji"""
    app = QuizApplication()
    app.run()


if __name__ == "__main__":
    main()
