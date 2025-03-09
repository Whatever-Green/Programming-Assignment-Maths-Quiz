import random

def get_user_name():
    userName = input("Name: ")
    return userName

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
"""
def easy():
    return random.randint(1, 10), random.randint(1, 10)
def medium():
    return random.randint(2, 15), random.randint(2, 15)
def hard():
    return random.randint(3, 20), random.randint(3, 20)
"""

"""
def question_generator():
    arr = [1,10]
    num1 = random.randint(arr)
    num2 = random.randint(arr)
    programAns = num1 + num2
    return num1, num2, programAns
"""

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
    while True:
        score = 0
        difficulty = input("Choose difficulty (easy, medium, hard): ").strip().lower()
        difficulty_functions = {
            "easy": easy,
            "medium": medium,
            "hard": hard
        }
        for i in range(10):  # 10 questions
            num1, num2, operation, programAns, lives = difficulty_functions[difficulty]()
            score += question_check(num1, num2, operation, programAns, lives)

        print(f"\nFinal Score: {score}/10")  # Display final score
        play_again = input(
            "Do you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            break


if __name__ == "__main__":
    main()


