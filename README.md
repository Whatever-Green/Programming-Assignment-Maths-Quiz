
# Maths Quiz

A Python application that allows pupils to practice arithmetic questions and enables teachers to monitor performance and adjust difficulty levels. The quiz supports addition, subtraction, and multiplication questions across adjustable difficulty settings.

## Features

✅ Pupils can enter their name and select a difficulty level (Easy, Medium, Hard)  
✅ Random arithmetic questions generated based on chosen difficulty  
✅ Tracks scores and saves results with pupil names and dates  
✅ Teachers (admins) can:

-   View all stored scores
-   Adjust quiz settings (number ranges, operations, attempts)  
    ✅ Graphical interface (Tkinter) for ease of use


## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/maths-quiz.git
cd maths-quiz

```

Ensure Python 3 is installed.


**Note**: Tkinter comes pre-installed with most Python distributions.

## Usage

Run the application:

```bash
python main.py

```

## File Structure

```
maths-quiz/
├── lib_mathsquiz.py   # Core logic and data handling
├── main.py            # Tkinter GUI interface
├── rules.json         # Settings for quiz rules
├── scores.db          # SQLite database storing pupil scores (auto-generated)
└── README.md

```

## How It Works

-   Pupils start the quiz, answer randomly generated questions, and get immediate feedback.
-   Scores and attempts are saved automatically.
-   Teachers can log into an admin menu to view past scores and modify quiz settings.

## Technologies Used

-   Python 3
-   Tkinter (for GUI)
-   SQLite3 (for score storage)
-   JSON (for settings/rules)



## Contributing

why?

## License

This project is licensed under the "Unlicense License"
