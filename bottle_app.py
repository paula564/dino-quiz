from html import escape
from pathlib import Path
from bottle import get, post, request, run, static_file, template
from quiz_generator import dinos, generate_quiz

@get("/quiz")
def quiz_form():
    questions = generate_quiz(dinos, num_questions=5)
    return template("quiz", questions=questions)

@post("/quiz")
def quiz_submit():
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)