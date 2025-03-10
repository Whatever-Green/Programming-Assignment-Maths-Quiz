from flask import Flask, render_template, request, redirect, url_for, session
import lib_mathsquiz as mq  # Import your existing library (replace with actual name)

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session storage

@app.route("/", methods=["GET", "POST"])
def index():
    """Homepage where users enter their name and select difficulty."""
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["difficulty"] = request.form["difficulty"]
        session["score"] = 0
        session["question_number"] = 0
        return redirect(url_for("quiz"))
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Handles quiz questions and answer submissions."""
    if "name" not in session:
        return redirect(url_for("index"))

    if session["question_number"] >= 10:  # End after 10 questions
        return redirect(url_for("result"))

    # Get difficulty function dynamically from your library
    difficulty_func = {
        "easy": mq.easy,
        "medium": mq.medium,
        "hard": mq.hard
    }[session["difficulty"]]

    # Get a new question
    num1, num2, operation, correct_answer, lives = difficulty_func()

    if request.method == "POST":
        user_answer = request.form.get("answer")
        if user_answer and int(user_answer) == correct_answer:
            session["score"] += 1

        session["question_number"] += 1
        return redirect(url_for("quiz"))

    return render_template("quiz.html", num1=num1, num2=num2, operation=operation, q_num=session["question_number"] + 1)

@app.route("/results")
def result():
    """Show final score and save it using your library's function."""
    mq.database_save(session["name"], session["difficulty"], session["score"])
    return render_template("results.html", name=session["name"], score=session["score"])

@app.route("/scores")
def scores():
    """Retrieve scores using the database() function from your library."""
    scores_list = mq.database
    return render_template("results.html", scores=scores_list)    # This prints scores in the console. Adjust if needed.

if __name__ == "__main__":
    app.run(debug=True)
