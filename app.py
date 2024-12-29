from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

app.jinja_env.globals.update(enumerate=enumerate)

leaderboard = []

questions = [
    {"question": "What is the best programming language?", "answer": "Python"},
    {"question": "Which of these is a programming language?", "answer": "Python"},
    {"question": "Who created Python programming language?", "answer": "Guido van Rossum"},
    {"question": "Who is the richest person in the world?", "answer": "Elon Musk"},
    {"question": "Which of the following programming languages is a markup language?", "answer": "HTML"},
]


def get_db_connection():
    conn = sqlite3.connect('leaderboard.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html', questions=questions)


@app.route('/result', methods=['POST'])
def result():
    username = request.form.get("username")

    if not username:
        feedback = "Please enter your name."
        return render_template('result.html', score=0, total=len(questions), feedback=feedback, leaderboard=leaderboard)

    score = 0

    for i, question in enumerate(questions):
        user_answer = request.form.get(f"question-{i}")
        if user_answer == question["answer"]:
            score += 1

    total = len(questions)
    percentage = (score / total) * 100

    if percentage >= 80:
        feedback = "Awesome!"
    elif 60 <= percentage < 80:
        feedback = "Well Done!"
    else:
        feedback = "You could have done better"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO leaderboard (username, score) VALUES (?, ?)', (username, score))
    conn.commit()
    conn.close()


    leaderboard.append({"username": username, "score": score})

    return render_template('result.html', score=score, total=total, feedback=feedback, leaderboard=leaderboard)


@app.route('/leaderboard')
def show_leaderboard():
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    return render_template('leaderboard.html', leaderboard=sorted_leaderboard)


if __name__ == '__main__':
    app.run(debug=True)
