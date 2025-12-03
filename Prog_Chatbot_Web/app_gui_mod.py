import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QTextEdit, QPushButton, QLabel, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QTextCursor
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class ChatWorker(QThread):
    """Wątek do wykonywania zapytań do API w tle"""
    response_ready = Signal(str, str)  # response_text, response_id
    error_occurred = Signal(str)

    def __init__(self, client, message, previous_response_id=None):
        super().__init__()
        self.client = client
        self.message = message
        self.previous_response_id = previous_response_id

    def run(self):
        try:
            response = self.client.responses.create(
                model="gpt-4.1-mini",
                input=self.message,
                previous_response_id=self.previous_response_id
            )
            self.response_ready.emit(response.output_text, response.id)
        except Exception as e:
            self.error_occurred.emit(str(e))


class ChatbotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()
        self.previous_response_id = None
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("Chatbot AI")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
        """)

        # Widget centralny
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout główny
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Tytuł
        title_label = QLabel("🤖 Chatbot AI")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Obszar historii czatu
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setPlaceholderText("Historia konwersacji pojawi się tutaj...")
        main_layout.addWidget(self.chat_history, stretch=3)

        # Pole tekstowe dla wiadomości użytkownika
        input_label = QLabel("Twoja wiadomość:")
        main_layout.addWidget(input_label)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Wpisz swoją wiadomość tutaj...")
        self.message_input.setMaximumHeight(100)
        main_layout.addWidget(self.message_input)

        # Layout przycisków
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Przycisk wyślij
        self.send_button = QPushButton("📤 Wyślij")
        self.send_button.clicked.connect(self.send_message)
        button_layout.addWidget(self.send_button, stretch=2)

        # Przycisk wyczyść
        self.clear_button = QPushButton("🗑️ Wyczyść historię")
        self.clear_button.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_button, stretch=1)

        main_layout.addLayout(button_layout)

        # Status bar
        self.statusBar().showMessage("Gotowy do rozmowy")
        self.statusBar().setStyleSheet("color: #00ff00; font-size: 12px;")

    def send_message(self):
        """Wysyłanie wiadomości do API"""
        message = self.message_input.toPlainText().strip()
        
        if not message:
            self.statusBar().showMessage("⚠️ Proszę wpisać wiadomość", 3000)
            return

        # Dodaj wiadomość użytkownika do historii
        self.append_to_chat("Ty", message, "#0078d4")
        
        # Wyczyść pole input
        self.message_input.clear()
        
        # Wyłącz przyciski podczas oczekiwania
        self.send_button.setEnabled(False)
        self.send_button.setText("⏳ Wysyłanie...")
        self.statusBar().showMessage("⏳ Oczekiwanie na odpowiedź...")

        # Uruchom wątek do wykonania zapytania API
        self.worker = ChatWorker(self.client, message, self.previous_response_id)
        self.worker.response_ready.connect(self.handle_response)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.start()

    def handle_response(self, response_text, response_id):
        """Obsługa odpowiedzi z API"""
        self.previous_response_id = response_id
        self.append_to_chat("AI", response_text, "#00ff00")
        
        # Włącz przyciski ponownie
        self.send_button.setEnabled(True)
        self.send_button.setText("📤 Wyślij")
        self.statusBar().showMessage("✅ Odpowiedź otrzymana", 3000)
        
        # Ustaw fokus na pole input
        self.message_input.setFocus()

    def handle_error(self, error_message):
        """Obsługa błędów"""
        self.append_to_chat("System", f"Błąd: {error_message}", "#ff0000")
        
        # Włącz przyciski ponownie
        self.send_button.setEnabled(True)
        self.send_button.setText("📤 Wyślij")
        self.statusBar().showMessage("❌ Wystąpił błąd", 3000)

    def append_to_chat(self, sender, message, color):
        """Dodawanie wiadomości do historii czatu"""
        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertBlock()  # ensure each entry starts on its own line
        
        # Formatowanie wiadomości
        html = (
            f'<div style="margin: 10px 0; padding: 10px; background-color: #2d2d2d; '
            f'border-left: 3px solid {color}; border-radius: 3px;">'
            f'<strong style="color: {color};">{sender}:</strong> '
            f'<span style="color: #ffffff; white-space: pre-wrap;">{message}</span>'
            f'</div>'
        )
        
        cursor.insertHtml(html)
        self.chat_history.setTextCursor(cursor)
        self.chat_history.ensureCursorVisible()

    def clear_history(self):
        """Czyszczenie historii konwersacji"""
        self.chat_history.clear()
        self.previous_response_id = None
        self.statusBar().showMessage("🗑️ Historia wyczyszczona", 3000)

    def keyPressEvent(self, event):
        """Obsługa skrótów klawiszowych"""
        # Ctrl+Enter lub Cmd+Enter do wysyłania wiadomości
        if (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter) and \
           event.modifiers() == Qt.ControlModifier:
            if self.send_button.isEnabled():
                self.send_message()
        else:
            super().keyPressEvent(event)


def main():
    """Funkcja główna aplikacji"""
    app = QApplication(sys.argv)
    
    # Sprawdź czy klucz API jest ustawiony
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('OPEN_API_KEY'):
        print("BŁĄD: Brak klucza API. Ustaw OPENAI_API_KEY w pliku .env")
        sys.exit(1)
    
    window = ChatbotGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
