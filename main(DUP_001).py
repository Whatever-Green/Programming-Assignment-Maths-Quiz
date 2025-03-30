import random, sqlite3

def get_user_name():
    userName = input("Name: ")
    return userName

def database():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    while True:
        # Prompt user to choose an option
        userInput = input("1. Search Scores\n2. Print All Scores\n3. Add a Score\n4. Delete a Score\n5. Update a Score\n6. Exit\nChoose an option: ").strip()

        if userInput == "1":
            # Ask for a name to search
            name_to_search = input("Enter name to search for: ").strip()

            # Execute the query with the provided name
            results = cur.execute("SELECT * FROM scores WHERE name = ?", (name_to_search,)).fetchall()
            if results:
                for row in results:
                    print(f"Name: {row[0]}, Difficulty: {row[1]}, Score: {row[2]}")
            else:
                print("No scores found for that name.")

        elif userInput == "2":
            # Print all scores
            results = cur.execute("SELECT * FROM scores").fetchall()
            if results:
                for row in results:
                    print(f"Name: {row[0]}, Difficulty: {row[1]}, Score: {row[2]}")
            else:
                print("No scores available.")

        elif userInput == "3":
            # Add a new score
            name = input("Enter name: ").strip()
            difficulty = input("Enter difficulty (easy, medium, hard): ").strip()
            score = input("Enter score: ").strip()

            try:
                score = float(score)
                cur.execute("INSERT INTO scores (name, difficulty, score) VALUES (?, ?, ?)", (name, difficulty, score))
                con.commit()
                print("Score added successfully!")
            except ValueError:
                print("Invalid score. Please enter a valid number.")

        elif userInput == "4":
            # Delete a score
            name_to_delete = input("Enter the name of the score to delete: ").strip()
            cur.execute("DELETE FROM scores WHERE name = ?", (name_to_delete,))
            con.commit()
            print(f"Score(s) for {name_to_delete} deleted.")

        elif userInput == "5":
            # Update a score
            name_to_update = input("Enter the name of the score to update: ").strip()
            new_score = input("Enter the new score: ").strip()

            try:
                new_score = float(new_score)
                cur.execute("UPDATE scores SET score = ? WHERE name = ?", (new_score, name_to_update))
                con.commit()
                print(f"Score for {name_to_update} updated.")
            except ValueError:
                print("Invalid score. Please enter a valid number.")

        elif userInput == "6":
            # Exit the program
            print("Exiting the program...")
            break

        else:
            print("Invalid option. Please choose a valid option.")
def database_save(name, difficulty, score):
    con = sqlite3.connect(
        "data.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS scores
                    (name text, difficulty text, score real)''')
    cur.execute("INSERT INTO scores (name, difficulty, score) VALUES (?, ?, ?)", (name, difficulty, score))
    con.commit()
    for row in cur.execute("SELECT * FROM scores"):
        print(row)

def easy():
    operations = ["+"] * 5 + ["-"] * 3 + ["*"] * 2
    lives = 3
    return question_generator(1, 10, operations, lives)
def medium():
    operations = ["+"] * 4 + ["-"] * 3 + ["*"] * 3
    lives = 2
    return question_generator(2, 15, operations, lives)
def hard():
    operations = ["+"] * 3 + ["-"] * 3 + ["*"] * 4
    lives = 2
    return question_generator(3, 20, operations, lives)

def question_generator(min_val, max_val, operations, lives):
    num1 = random.randint(
        min_val,
        max_val)
    num2 = random.randint(
        min_val,
        max_val)
    operation = random.choice(
        operations)
    if operation == "-":
        num1, num2 = max(num1, num2), min(num1, num2)  # Avoid negative answers

    programAns = eval(f"{num1} {operation} {num2}")
    return num1, num2, operation, programAns, lives
def question_check(num1, num2, operation,programAns, lives):
    attempts = lives
    while attempts > 0:
        try:
            userAns = int(input(f"{num1} {operation} {num2} = "))
            if userAns == programAns:
                print("Correct!")
                return 1
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"Wrong! Try again. {attempts} attempts left.")
                else:
                    print(f"Wrong! The correct answer was {programAns}. Moving to the next question.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            attempts -= 1
    return 0


def main():
    name = get_user_name()
    while True:
        while True:
            admin = input("Start or Admin?").strip().lower()
            if admin == "admin":
                database()
            else:
                break
        score = 0
        difficulty = input(f"Welcome {name}, Choose difficulty (easy, medium, hard): ").strip().lower()
        difficulty_functions = {
            "easy": easy,
            "medium": medium,
            "hard": hard,
        }
        for i in range(10):  # 10 questions
            num1, num2, operation, programAns, lives = difficulty_functions[difficulty]()
            score += question_check(num1, num2, operation, programAns, lives)

        print(f"\nFinal Score: {score}/10")  # Display final score
        database_save(name, difficulty, score)
        play_again = input(
            "Do you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            break
if __name__ == "__main__":
    main()