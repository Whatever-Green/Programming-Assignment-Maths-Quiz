import random, sqlite3, json

def load_rules(): # Opens or Creates rules.json depending if files exists
    try:
        with open("rules.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "easy": {"min": 1, "max": 10, "add": 5, "sub": 3, "mul": 2, "lives": 3},
            "medium": {"min": 2, "max": 15, "add": 4, "sub": 3, "mul": 3, "lives": 2},
            "hard": {"min": 3, "max": 20, "add": 3, "sub": 3, "mul": 4, "lives": 2}
        }

def save_rules(rules): # if rules are edited save to JSON
    with open("rules.json", "w") as file:
        json.dump(rules, file, indent=4)

def database_setup(): # Creates data.db for scores
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS scores (name TEXT, difficulty TEXT, score INTEGER)""")
    con.commit()
    con.close()

def save_score(name, difficulty, score): # when user finishes quiz save username difficulty and score
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("INSERT INTO scores (name, difficulty, score) VALUES (?, ?, ?)", (name, difficulty, score))
    con.commit()
    con.close()

def view_scores(): # prints the contents of the Database
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    results = cur.execute("SELECT * FROM scores").fetchall()
    con.close()
    return results

def edit_rules(rules): # handles JSON editing
    difficulty = input("Enter difficulty to modify (easy, medium, hard): ").strip().lower()
    if difficulty in rules:
        for key in rules[difficulty]:
            new_value = input(f"Enter new value for {key} (current: {rules[difficulty][key]}): ").strip()
            if new_value.isdigit():
                rules[difficulty][key] = int(new_value)
        save_rules(rules)
        print("Rules updated!")
    else:
        print("Invalid difficulty.")

def question_generator(rules, difficulty): # generates questions depending on Difficulty
    settings = rules[difficulty]
    operations = ["+"] * settings["add"] + ["-"] * settings["sub"] + ["*"] * settings["mul"]
    num1, num2 = random.randint(settings["min"], settings["max"]), random.randint(settings["min"], settings["max"])
    operation = random.choice(operations)
    if operation == "-":
        num1, num2 = max(num1, num2), min(num1, num2)
    return num1, num2, operation, eval(f"{num1} {operation} {num2}"), settings["lives"]

def question_check(num1, num2, operation, correct_ans, lives): # takes in user input and checks it with correct answer
    attempts = lives
    while attempts > 0:
        try:
            user_ans = int(input(f"{num1} {operation} {num2} = "))
            if user_ans == correct_ans:
                print("Correct!")
                return 1
            else:
                attempts -= 1
                print(f"Wrong! {attempts} attempts left.")
        except ValueError:
            print("Invalid input. Enter a number.")
            attempts -= 1
    print(f"Out of attempts! The correct answer was {correct_ans}.")
    return 0

def main():
    database_setup()
    rules = load_rules()
    name = input("Enter your name: ").strip()
    while True:
        mode = input("Start Quiz or Admin Mode? ").strip().lower()
        if mode == "admin":
            admin_choice = input("1. View Scores 2. Edit Rules 3. Exit Admin: ").strip()
            if admin_choice == "1":
                for row in view_scores():
                    print(f"{row[0]} - {row[1]} - Score: {row[2]}")
            elif admin_choice == "2":
                edit_rules(rules)
            elif admin_choice == "3":
                break
            else:
                print("Invalid choice.")
        else:
            break
    score = 0
    difficulty = input("Choose difficulty (easy, medium, hard): ").strip().lower()
    if difficulty not in rules:
        print("Invalid difficulty. Exiting...")
        return
    for _ in range(10):
        num1, num2, operation, correct_ans, lives = question_generator(rules, difficulty)
        score += question_check(num1, num2, operation, correct_ans, lives)
    print(f"Final Score: {score}/10")
    save_score(name, difficulty, score)
    if input("Play again? (yes/no): ").strip().lower() != "yes":
        exit()

if __name__ == "__main__":
    main()
