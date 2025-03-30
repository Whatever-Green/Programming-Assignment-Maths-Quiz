import \
    tkinter as tk
from tkinter import \
    messagebox, \
    ttk, \
    simpledialog
import \
    lib_mathsquiz as mq


class MathsQuizApp:
    def __init__(
            self,
            root):
        self.root = root
        self.root.title(
            "Maths Quiz")
        self.name = ""
        self.difficulty = ""
        self.score = 0

        self.create_main_menu()

    def create_main_menu(
            self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Welcome to Maths Quiz",
            font=(
            "Arial",
            16)).pack(
            pady=10)
        tk.Button(
            self.root,
            text="Start Quiz",
            command=self.start_quiz_menu).pack(
            pady=5)
        tk.Button(
            self.root,
            text="Admin Mode",
            command=self.admin_mode).pack(
            pady=5)
        tk.Button(
            self.root,
            text="Exit",
            command=self.root.quit).pack(
            pady=5)

    def start_quiz_menu(
            self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Enter Your Name:",
            font=(
            "Arial",
            12)).pack(
            pady=5)
        name_entry = tk.Entry(
            self.root)
        name_entry.pack(
            pady=5)

        tk.Label(
            self.root,
            text="Choose Difficulty:",
            font=(
            "Arial",
            12)).pack(
            pady=5)
        difficulty_combo = ttk.Combobox(
            self.root,
            values=[
                "easy",
                "medium",
                "hard"],
            state="readonly")
        difficulty_combo.pack(
            pady=5)
        difficulty_combo.current(
            0)

        def start_quiz():
            self.name = name_entry.get().strip()
            self.difficulty = difficulty_combo.get()
            if self.name:
                self.start_quiz()
            else:
                messagebox.showwarning(
                    "Warning",
                    "Please enter your name!")

        tk.Button(
            self.root,
            text="Start",
            command=start_quiz).pack(
            pady=5)
        tk.Button(
            self.root,
            text="Back",
            command=self.create_main_menu).pack(
            pady=5)

    def start_quiz(
            self):
        self.score = 0
        rules = mq.load_rules()
        if self.difficulty not in rules:
            messagebox.showerror(
                "Error",
                "Invalid difficulty!")
            return

        for _ in range(
                10):
            num1, num2, operation, correct_ans, lives = mq.question_generator(
                rules,
                self.difficulty)
            self.ask_question(
                num1,
                num2,
                operation,
                correct_ans,
                lives)

        messagebox.showinfo(
            "Quiz Complete",
            f"Final Score: {self.score}/10")
        mq.save_score(
            self.name,
            self.difficulty,
            self.score)
        self.create_main_menu()

    def ask_question(
            self,
            num1,
            num2,
            operation,
            correct_ans,
            lives):
        attempts = lives

        while attempts > 0:
            user_ans = simpledialog.askinteger(
                "Question",
                f"{num1} {operation} {num2} = ? ({attempts} attempts left)")
            if user_ans is None:
                return
            if user_ans == correct_ans:
                messagebox.showinfo(
                    "Correct!",
                    "Well done!")
                self.score += 1
                return
            else:
                attempts -= 1
                messagebox.showwarning(
                    "Incorrect",
                    f"Try again! {attempts} attempts left.")

        messagebox.showinfo(
            "Answer Revealed",
            f"The correct answer was {correct_ans}.")

    def admin_mode(
            self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Admin Mode",
            font=(
            "Arial",
            16)).pack(
            pady=10)
        tk.Button(
            self.root,
            text="View Scores",
            command=self.view_scores).pack(
            pady=5)
        tk.Button(
            self.root,
            text="Edit Rules",
            command=self.edit_rules).pack(
            pady=5)
        tk.Button(
            self.root,
            text="Back",
            command=self.create_main_menu).pack(
            pady=5)

    def view_scores(
            self):
        scores = mq.view_scores()
        if not scores:
            messagebox.showinfo(
                "Scores",
                "No scores recorded yet.")
            return

        score_text = "\n".join(
            [
                f"{row[0]} - {row[1]} - Score: {row[2]}"
                for
                row
                in
                scores])
        messagebox.showinfo(
            "Scores",
            score_text)

    def edit_rules(
            self):
        rules = mq.load_rules()
        difficulty = simpledialog.askstring(
            "Edit Rules",
            "Enter difficulty to modify (easy, medium, hard):").strip().lower()

        if difficulty in rules:
            for key in \
            rules[
                difficulty]:
                new_value = simpledialog.askinteger(
                    "Edit Value",
                    f"Enter new value for {key} (current: {rules[difficulty][key]}):")
                if new_value is not None:
                    rules[
                        difficulty][
                        key] = new_value
            mq.save_rules(
                rules)
            messagebox.showinfo(
                "Success",
                "Rules updated successfully!")
        else:
            messagebox.showerror(
                "Error",
                "Invalid difficulty!")


if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuizApp(
        root)
    root.mainloop()
