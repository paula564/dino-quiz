from html import escape
from pathlib import Path
from bottle import get, post, request, run, static_file, template, html_escape
from quiz_generator import dinos, generate_quiz
import os

STATIC_DIR = Path(__file__).resolve().parent / "static"

@get("/quiz")
def quiz_form():
    questions = generate_quiz(dinos, num_questions=5)
    return template("quiz", questions=questions)

@post("/quiz")
def quiz_submit():
    selected = [request.forms.get("q" + str(i)) for i in range(5)]
    correct = [request.forms.get(f"ans{i}") for i in range(5)]

    score = 0
    for i in range(5):
        if selected[i] == correct[i]:
            score += 1

    return template('results', correct=correct, selected=selected, score=score)

@get("/static/<filename>")
def serve_css(filename):
    return static_file(filename, root=str(STATIC_DIR))





if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)