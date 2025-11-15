import pytest
import builtins
import os
from ui_text import UITextInterface

class DummyScreen:
    def __init__(self):
        self.cleared = False
    def clear(self):
        self.cleared = True

@pytest.fixture
def ui():
    return UITextInterface()

# --- Testy czyszczenia ekranu ---
def test_clear_screen(monkeypatch, ui):
    called = {}
    monkeypatch.setattr(os, "system", lambda cmd: called.setdefault("system", cmd))
    ui._clear_screen()
    assert called["system"] in ["cls", "clear"]

# --- Testy nagłówka ---
def test_print_header(capsys, ui):
    ui._print_header("Test", "Info")
    out = capsys.readouterr().out
    assert "TEST" in out
    assert "Info" in out
    assert ui.HEADER_CHAR * ui.SCREEN_WIDTH in out

# --- Testy walidacji wejścia ---
def test_get_valid_input_valid(monkeypatch, ui):
    monkeypatch.setattr(builtins, "input", lambda _: "abc")
    result = ui._get_valid_input("Prompt: ")
    assert result == "abc"

def test_get_valid_input_invalid(monkeypatch, capsys, ui):
    responses = iter(["", "ok"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))
    result = ui._get_valid_input("Prompt: ")
    assert result == "ok"
    out = capsys.readouterr().out
    assert "Niepoprawne dane" in out

# --- Testy wyboru tematu ---
def test_ask_topic(monkeypatch, capsys, ui):
    monkeypatch.setattr(builtins, "input", lambda _: "Python")
    result = ui.ask_topic()
    assert result == "Python"
    out = capsys.readouterr().out
    assert "WYBÓR TEMATU" in out
    assert "Python" in out

def test_ask_topic_empty_then_valid(monkeypatch, capsys, ui):
    responses = iter(["", "  ", "Python", ""])  # Cztery wejścia: dwa błędy + prawidłowe + ENTER
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))
    result = ui.ask_topic()
    assert result == "Python"
    out = capsys.readouterr().out
    assert "Temat nie może być pusty" in out

# --- Testy wyboru liczby pytań ---
@pytest.mark.parametrize("user_input", ["1", "10"])
def test_ask_number_of_questions_edges(monkeypatch, capsys, ui, user_input):
    monkeypatch.setattr(builtins, "input", lambda _: user_input)
    result = ui.ask_number_of_questions(1, 10)
    assert result == int(user_input)

def test_ask_number_of_questions_invalid(monkeypatch, capsys, ui):
    responses = iter(["0", "-1", "abc", "5", ""])  # Cztery błędy + prawidłowe + ENTER
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))
    result = ui.ask_number_of_questions(1, 10)
    assert result == 5
    out = capsys.readouterr().out
    assert "Wpisz liczbę z zakresu" in out

# --- Testy wyświetlania pytania ---
def test_display_question(capsys, ui):
    choices = {"a": "Opcja A", "b": "Opcja B", "c": "Opcja C", "d": "Opcja D"}
    ui.display_question(1, "Jaki to język?", choices)
    out = capsys.readouterr().out
    assert "PYTANIE 1" in out
    assert "Jaki to język?" in out
    for v in choices.values():
        assert v in out

# --- Testy wyboru odpowiedzi ---
def test_get_user_choice_invalid(monkeypatch, capsys, ui):  # Wartości błędne
    responses = iter(["X", "?", "A"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))
    result = ui.get_user_choice()
    assert result == "a"
    out = capsys.readouterr().out
    assert "Wybierz A, B, C lub D" in out

def test_display_question_missing_choices(capsys, ui):  # Brak niektórych wartości
    choices = {"a": "Opcja A", "c": "Opcja C"}
    ui.display_question(1, "Test?", choices)
    out = capsys.readouterr().out

    assert "Opcja A" in out
    assert "Opcja C" in out
    # brak B i D
    assert "Opcja B" not in out
    assert "Opcja D" not in out

def test_get_user_choice(monkeypatch, ui):  # Poprawna wartość
    monkeypatch.setattr(builtins, "input", lambda _: "B")
    result = ui.get_user_choice()
    assert result == "b"

# --- Testy feedbacku odpowiedzi ---
def test_show_answer_feedback_correct(monkeypatch, capsys, ui):
    monkeypatch.setattr(builtins, "input", lambda _: "")
    ui.show_answer_feedback(True, "a", "a", "Opcja A")
    out = capsys.readouterr().out
    assert "POPRAWNIE" in out
    assert "a" in out

def test_show_answer_feedback_wrong(monkeypatch, capsys, ui):
    monkeypatch.setattr(builtins, "input", lambda _: "")
    ui.show_answer_feedback(False, "b", "c", "Opcja C")
    out = capsys.readouterr().out
    assert "BŁĘDNIE" in out
    assert "c" in out
    assert "Opcja C" in out

# --- Testy raportu końcowego ---
def test_display_final_report(monkeypatch, capsys, ui):
    monkeypatch.setattr(builtins, "input", lambda _: "")
    ui.display_final_report("Wynik: 5/5")
    out = capsys.readouterr().out
    assert "RAPORT WYNIKÓW" in out
    assert "Wynik: 5/5" in out

# --- Testy komunikatów ---
def test_show_message_info(capsys, ui):
    ui.show_message("To jest info", "info")
    out = capsys.readouterr().out
    assert "ℹ️" in out
    assert "To jest info" in out

def test_show_message_error(capsys, ui):
    ui.show_message("Błąd!", "error")
    out = capsys.readouterr().out
    assert "❌" in out
    assert "Błąd!" in out
