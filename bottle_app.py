from html import escape
from pathlib import Path
from bottle import get, post, request, run, static_file, template, html_escape 
from quiz_generator import dinos, generate_quiz

@get("/quiz")
def quiz_form():
    questions = generate_quiz(dinos, num_questions=5)
    return template("quiz", questions=questions)

@post("/quiz")
def quiz_submit():
    selected_options = []
    for i in range(5):
        selected_options.append(request.forms.get("q" + str(i)))

    return f"<h1>Options: {html_escape(str(selected_options))}</h1>"


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)