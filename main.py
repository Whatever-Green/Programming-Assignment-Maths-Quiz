import tkinter as tk
from tkinter import messagebox
import lib_mathsquiz as mq

class MathsQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")

        self.user_name = tk.StringVar()
        self.difficulty = tk.StringVar(value="easy")
        self.score = 0
        self.current_question = None

        self.create_main_menu()

    def create_main_menu(self):
        """Creates the main menu with name entry and difficulty selection."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Your Name:", font=("Arial", 14)).pack(pady=10)
        tk.Entry(self.root, textvariable=self.user_name, font=("Arial", 14)).pack(pady=5)

        tk.Label(self.root, text="Choose Difficulty:", font=("Arial", 14)).pack(pady=10)
        tk.OptionMenu(self.root, self.difficulty, "easy", "medium", "hard").pack(pady=5)

        tk.Button(self.root, text="Start Quiz", command=self.start_quiz, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="View Scores", command=self.view_scores, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.root, text="Admin Panel", command=self.admin_panel, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 12)).pack(pady=10)

    def start_quiz(self):
        """Starts the quiz and asks the first question."""
        if not self.user_name.get():
            messagebox.showerror("Error", "Please enter your name!")
            return

        self.score = 0
        self.ask_question()

    def ask_question(self):
        """Generates and displays a new question."""
        difficulty_func = {"easy": mq.easy, "medium": mq.medium, "hard": mq.hard}
        self.current_question = difficulty_func[self.difficulty.get()]()

        num1, num2, operation, answer, lives = self.current_question

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"{num1} {operation} {num2} =", font=("Arial", 24)).pack(pady=20)
        self.user_answer = tk.Entry(self.root, font=("Arial", 20))
        self.user_answer.pack(pady=10)

        tk.Button(self.root, text="Submit Answer", command=self.check_answer, font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Quit Quiz", command=self.create_main_menu, font=("Arial", 12)).pack(pady=5)

    def check_answer(self):
        """Validates the user's answer and moves to the next question."""
        try:
            user_input = int(self.user_answer.get())
            num1, num2, operation, answer, lives = self.current_question

            if user_input == answer:
                self.score += 1
                messagebox.showinfo("Correct!", "Well done!")
            else:
                messagebox.showerror("Wrong!", f"The correct answer was {answer}.")

            if self.score < 10:
                self.ask_question()
            else:
                self.end_quiz()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    def end_quiz(self):
        """Ends the quiz and saves the score."""
        messagebox.showinfo("Quiz Completed", f"Final Score: {self.score}/10")
        mq.database_save(self.user_name.get(), self.difficulty.get(), self.score)
        self.create_main_menu()

    def view_scores(self):
        """Displays stored scores from the database."""
        scores_window = tk.Toplevel(self.root)
        scores_window.title("Scores")

        con = mq.sqlite3.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM scores")
        scores = cur.fetchall()
        con.close()

        tk.Label(scores_window, text="High Scores", font=("Arial", 16)).pack(pady=10)
        if scores:
            for score in scores:
                tk.Label(scores_window, text=f"{score[0]} - {score[1]} - {score[2]}", font=("Arial", 12)).pack()
        else:
            tk.Label(scores_window, text="No scores available.", font=("Arial", 12)).pack()

    def admin_panel(self):
        """Opens the admin panel."""
        mq.database()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuizApp(root)
    root.mainloop()
