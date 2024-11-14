from flask import Flask, render_template, request

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
questions = [
    {
        "question": "What is the best programming language?",
        "options": ["C++", "Python", "Golang", "C#"],
        "answer": "C++"
    },
    {
        "question": "Which of these is a programming language??",
        "options": ["BloodLast", "Erebus", "Python", "Linux"],
        "answer": "Python"
    },
    {
        "question": "Who created Python programming language?",
        "options": ["Linus Torvalds", "Guido van Rossum", "Mark Zuckerberg", "Chad Meredith Hurley"],
        "answer": "Guido van Rossum"
    },
    {
        "question": "Who is the richest person in the world?",
        "options": ["Mark Zuckerberg", "Elon Mask", "Jacob Rothschild", "Donald Trump"],
        "answer": "Elon Mask"
    },
    {
        "question": "Which of the following programming languages is a markup language?",
        "options": ["HTML", "Java", "Ruby", "C+"],
        "answer": "HTML"
    }
]

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
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

    return render_template('result.html', score=score, total=total, feedback=feedback)


