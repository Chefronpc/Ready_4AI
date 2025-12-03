import os
import sys
from typing import Optional

import httpx
from dotenv import load_dotenv
from PySide6 import QtCore, QtGui, QtWidgets

load_dotenv()


def _build_chat_url() -> str:
    base_url = os.getenv("CHATBOT_BACKEND_URL", "http://127.0.0.1:5000")
    endpoint = os.getenv("CHATBOT_CHAT_ENDPOINT", "/chat")
    return base_url.rstrip("/") + "/" + endpoint.lstrip("/")


CHAT_ENDPOINT_URL = _build_chat_url()


class ChatWorkerSignals(QtCore.QObject):
    success = QtCore.Signal(dict)
    error = QtCore.Signal(str)
    finished = QtCore.Signal()


class ChatWorker(QtCore.QRunnable):
    def __init__(self, message: str, previous_response_id: Optional[str] = None):
        super().__init__()
        self.message = message
        self.previous_response_id = previous_response_id
        self.signals = ChatWorkerSignals()

    def run(self) -> None:
        payload = {"message": self.message}
        if self.previous_response_id:
            payload["previousResponseId"] = self.previous_response_id

        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(CHAT_ENDPOINT_URL, json=payload)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPStatusError as exc:
            detail = self._extract_error_message(exc)
            self.signals.error.emit(detail)
        except Exception as exc:  # pylint: disable=broad-except
            self.signals.error.emit(str(exc))
        else:
            self.signals.success.emit(data)
        finally:
            self.signals.finished.emit()

    @staticmethod
    def _extract_error_message(exc: httpx.HTTPStatusError) -> str:
        try:
            payload = exc.response.json()
            message = payload.get("error") or payload
        except Exception:  # pylint: disable=broad-except
            message = exc.response.text
        return f"{exc.response.status_code}: {message}"


class ChatWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Ready4AI Chatbot")
        self.resize(720, 540)

        self.previous_response_id: Optional[str] = None
        self.thread_pool = QtCore.QThreadPool(self)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)

        self.history_view = QtWidgets.QPlainTextEdit()
        self.history_view.setReadOnly(True)
        layout.addWidget(self.history_view)

        self.input_box = QtWidgets.QTextEdit()
        self.input_box.setPlaceholderText("Wpisz wiadomość do chatbota...")
        self.input_box.setFixedHeight(120)
        layout.addWidget(self.input_box)

        button_row = QtWidgets.QHBoxLayout()
        layout.addLayout(button_row)

        self.status_label = QtWidgets.QLabel("Połączono z: " + CHAT_ENDPOINT_URL)
        self.status_label.setWordWrap(True)
        button_row.addWidget(self.status_label, 1)

        self.send_button = QtWidgets.QPushButton("Wyślij")
        self.send_button.clicked.connect(self._on_send_clicked)
        button_row.addWidget(self.send_button)

        self.clear_button = QtWidgets.QPushButton("Wyczyść")
        self.clear_button.clicked.connect(self._clear_history)
        button_row.addWidget(self.clear_button)

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Return"), self.input_box, self._on_send_clicked)

    def _on_send_clicked(self) -> None:
        message = self.input_box.toPlainText().strip()
        if not message:
            self._set_status("Wiadomość jest pusta.")
            return

        self._append_message("Ty", message)
        self.input_box.clear()
        self._toggle_inputs(False)
        self._set_status("Wysyłanie...")

        worker = ChatWorker(message, self.previous_response_id)
        worker.signals.success.connect(self._handle_success)
        worker.signals.error.connect(self._handle_error)
        worker.signals.finished.connect(lambda: self._toggle_inputs(True))
        self.thread_pool.start(worker)

    def _handle_success(self, payload: dict) -> None:
        response_text = payload.get("response", "")
        response_id = payload.get("responseId")
        self.previous_response_id = response_id or self.previous_response_id

        if response_text:
            self._append_message("Bot", response_text)
            self._set_status("Odpowiedź odebrana.")
        else:
            self._set_status("Brak treści w odpowiedzi.")

    def _handle_error(self, message: str) -> None:
        self._append_message("Błąd", message)
        self._set_status(message)

    def _append_message(self, author: str, message: str) -> None:
        divider = "-" * 30
        self.history_view.appendPlainText(f"{author}:\n{message}\n{divider}")
        self.history_view.verticalScrollBar().setValue(self.history_view.verticalScrollBar().maximum())

    def _clear_history(self) -> None:
        self.history_view.clear()
        self.previous_response_id = None
        self._set_status("Historia wyczyszczona.")

    def _toggle_inputs(self, enabled: bool) -> None:
        self.send_button.setEnabled(enabled)
        self.input_box.setEnabled(enabled)

    def _set_status(self, text: str) -> None:
        self.status_label.setText(text)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
