
A beginner-friendly, interactive desktop quiz application built using **Python** and **Tkinter**. 

The application allows users to select a difficulty level, answer randomized multiple-choice questions, race against a 15-second countdown timer, and view instant scoring and performance feedback.

---

## Features

- **Tkinter Desktop GUI**: Clean, modern card-based desktop interface.
- **Difficulty Selection**: Three difficulty tiers (**Easy**, **Medium**, **Hard**).
- **JSON Data Storage**: Questions and answers stored in human-readable `questions.json`.
- **Randomization Engine**: Shuffles question selection and answer order on every attempt.
- **Non-Blocking Timer**: 15-second per-question countdown implemented via Tkinter `.after()` (no UI freezing).
- **Instant Answer Feedback**: Visual feedback for correct answers, wrong answers, and timeouts.
- **Score & Percentage Calculation**: Accurate score tracking and percentage-based evaluations.
- **Performance Evaluation**: Custom feedback messages based on performance tiers:
  - $\ge 90\%$: Excellent! Outstanding Job!
  - $70\% - 89\%$: Very Good! Keep Practicing!
  - $50\% - 69\%$: Good Effort! You Can Improve!
  - $< 50\%$: Keep Practicing and Try Again!
- **Play Again & Exit Flow**: Reset quiz state without restarting the program.
- **Zero Third-Party Dependencies**: Runs strictly on the Python Standard Library.

---

## Technologies Used

- **Python 3**: Core programming language.
- **Tkinter**: GUI library (standard library).
- **JSON**: Question database format.
- **Standard Library Modules**: `tkinter`, `json`, `random`, `os`, `sys`.

---

## Project Structure

```
smart-quiz-game/
├── main.py             # Main GUI application logic and screen management
├── questions.json      # JSON question database (Easy, Medium, Hard)
├── requirements.txt    # Standard library dependency declaration
├── .gitignore          # Git exclusion rules for compiled Python bytecode
└── README.md           # Documentation, testing table, and interview guide
```

---

## Installation & How to Run

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Step 1: Clone or Download the Project
```bash
git clone <repository-url>
cd smart-quiz-game
```

### Step 2: Run the Application
On Windows:
```bash
py main.py
```
*or*
```bash
python main.py
```

On macOS / Linux:
```bash
python3 main.py
```

> **Note**: No `pip install` commands are needed because all modules belong to Python's standard library.

---

## How It Works

1. **Application Launch**:
   - The application creates an $800 \times 600$ window centered on the screen.
   - Loads and validates questions from `questions.json`.
   - Displays the Welcome Screen with difficulty choices (**Easy**, **Medium**, **Hard**).

2. **Starting the Quiz**:
   - The user selects a difficulty and clicks **Start Quiz**.
   - Filters questions matching the chosen difficulty.
   - Randomly selects up to 10 questions and shuffles answer choices ($A, B, C, D$).

3. **Answering & Timer**:
   - Each question has a 15-second countdown timer.
   - Clicking an answer immediately locks buttons, awards points if correct, highlights the right choice, and advances after a 1.2-second pause.
   - If the timer hits zero, the question is marked unanswered/incorrect and automatically advances.

4. **Results & Replay**:
   - Displays final score, percentage, and performance message.
   - **Play Again** safely resets the score and state, returning to the difficulty menu.

---

## Adding Custom Questions to `questions.json`

You can easily expand the quiz by adding new question objects to `questions.json`:

```json
{
  "question": "What is the capital of Japan?",
  "options": [
    "Tokyo",
    "Kyoto",
    "Osaka",
    "Hiroshima"
  ],
  "correct_answer": "Tokyo",
  "difficulty": "Easy"
}
```

### Rules for Adding Questions:
1. `question`: A clear, unambiguous question string.
2. `options`: A list of exactly 4 choices.
3. `correct_answer`: Must exactly match one of the 4 items in `options`.
4. `difficulty`: Must be `"Easy"`, `"Medium"`, or `"Hard"`.

---

## QA Test Cases & Results

| # | Test Case | Expected Result | Status |
|---|---|---|---|
| 1 | Application Startup | 800x600 window opens centered with title "Smart Quiz Game" | **Pass** |
| 2 | Start without Difficulty | Displays warning message box prompting user to select difficulty | **Pass** |
| 3 | Difficulty Filtering | Selecting "Easy" loads only questions with `"difficulty": "Easy"` | **Pass** |
| 4 | Question Randomization | Question order and option button positions shuffle on each run | **Pass** |
| 5 | Correct Answer | Score increases by 1, button turns green, moves to next question | **Pass** |
| 6 | Wrong Answer | Score remains unchanged, shows correct answer in green, button in red | **Pass** |
| 7 | Multi-Click Prevention | Clicking an option locks buttons so multiple clicks are ignored | **Pass** |
| 8 | Timer Countdown | Countdown decreases from 15 to 0 without freezing UI | **Pass** |
| 9 | Question Timeout | At 0s, question is marked wrong, reveals correct answer, auto-advances | **Pass** |
| 10 | Score Calculation | Final score and percentage calculated accurately ($X/10$, $Y\%$) | **Pass** |
| 11 | Performance Feedback | Displays correct evaluation message based on percentage score | **Pass** |
| 12 | Play Again Reset | Clears score, timer, and current question; returns to Welcome Screen | **Pass** |
| 13 | Exit Button | Closes window and terminates cleanly without background threads | **Pass** |
| 14 | Missing `questions.json` | Shows user-friendly error popup instead of crashing | **Pass** |
| 15 | Malformed JSON | Shows JSON error message popup instead of traceback | **Pass** |

---

## Screenshots

> *(Placeholders for project portfolio screenshots)*
- `screenshots/welcome.png` — Welcome screen with difficulty selection
- `screenshots/quiz.png` — Active question with countdown timer and options
- `screenshots/result.png` — Result screen with final score and performance message

---

## Interview Questions & Answers

### 1. What is Tkinter and why was it chosen for this project?
> **Answer**: Tkinter is the standard Python interface to the Tk GUI toolkit. It comes built-in with standard Python installations, making it ideal for desktop applications without requiring third-party package installations.

### 2. How did you implement the countdown timer without freezing the GUI?
> **Answer**: In GUI applications, `time.sleep()` blocks the main thread and freezes event processing. Instead, we used Tkinter's non-blocking `root.after(1000, callback)` method, which schedules the countdown tick on the event loop while keeping the GUI responsive.

### 3. How do you prevent multiple answer clicks on the same question?
> **Answer**: We maintain a boolean flag `self.buttons_locked = True` when an answer is selected or when timeout occurs. If clicked again, the handler immediately returns, ignoring further input.

### 4. How does the application handle data persistence and validation?
> **Answer**: Questions are decoupled into `questions.json`. On launch, the program validates that the file exists, has valid JSON syntax, and ensures each question contains 4 options with the correct answer included in the option list.

---

## Future Improvements

- [ ] High Score & Persistent Leaderboard (local file storage)
- [ ] Sound effects and audio cues on correct/wrong answers
- [ ] Subject categories (Python, General Science, History, Math)
- [ ] Dark Mode toggle
- [ ] User profiles and quiz performance history tracking

---

## Author

Developed as a beginner-friendly Python portfolio project demonstrating desktop GUI development, event-driven programming, and clean data architecture.
