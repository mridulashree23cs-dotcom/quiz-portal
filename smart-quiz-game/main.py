# Smart Quiz Game
# Beginner-friendly Python Tkinter project
# Standard library only: tkinter, json, random, os

import tkinter as tk
from tkinter import messagebox
import os
import json
import random


class QuizApp:
    """
    Main application class for the Smart Quiz Game.
    Manages GUI screens, user interactions, timers, and quiz state.
    """

    def __init__(self, root):
        # Store the main Tkinter root window
        self.root = root
        self.root.title("Smart Quiz Game")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Center the window on the user's screen
        self.center_window(800, 600)

        # Application color palette (modern, clean, and accessible)
        self.bg_color = "#f8fafc"          # Light slate background
        self.card_color = "#ffffff"        # Clean white card surface
        self.primary_color = "#2563eb"     # Royal blue for primary actions
        self.primary_hover = "#1d4ed8"     # Darker blue on hover/click
        self.success_color = "#16a34a"     # Green for correct answers
        self.danger_color = "#dc2626"      # Red for wrong answers / timeout
        self.warning_color = "#d97706"     # Amber for timer countdown
        self.text_dark = "#1e293b"         # Dark slate for headings
        self.text_muted = "#64748b"        # Muted gray for subtitles
        self.btn_bg = "#f1f5f9"            # Light gray for option buttons
        self.btn_border = "#cbd5e1"        # Subtle border for options

        self.root.configure(bg=self.bg_color)

        # Quiz state variables
        self.selected_difficulty = tk.StringVar(value="")
        self.all_questions = []
        self.quiz_questions = []
        self.current_question_index = 0
        self.score = 0
        self.time_left = 15
        self.timer_id = None
        self.buttons_locked = False

        # GUI container and widget references
        self.current_frame = None
        self.timer_label = None
        self.score_label = None
        self.feedback_label = None
        self.option_buttons = []

        # Load quiz questions from JSON file
        self.load_questions()

        # Display the initial welcome screen
        self.show_welcome_screen()

    # ---------------------------------------------------------
    # Helper & Data Management Methods
    # ---------------------------------------------------------

    def center_window(self, width, height):
        """Center the Tkinter window on the computer screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def clear_screen(self):
        """Remove existing widgets before rendering a new screen."""
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def cancel_timer(self):
        """Safely cancel any active countdown timer callback."""
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def load_questions(self):
        """
        Load and validate questions from questions.json.
        Handles missing files and malformed JSON safely.
        """
        # Get directory of this script to reliably locate questions.json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "questions.json")

        if not os.path.exists(json_path):
            messagebox.showerror(
                "File Not Found",
                f"Unable to find 'questions.json' in:\n{base_dir}\n\nPlease ensure the file exists."
            )
            self.all_questions = []
            return

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("JSON root must be a list of questions.")

            # Validate each question item
            valid_questions = []
            for item in data:
                if (
                    isinstance(item, dict)
                    and "question" in item
                    and "options" in item
                    and "correct_answer" in item
                    and "difficulty" in item
                    and isinstance(item["options"], list)
                    and len(item["options"]) == 4
                    and item["correct_answer"] in item["options"]
                ):
                    valid_questions.append(item)

            if not valid_questions:
                messagebox.showerror(
                    "Invalid Data",
                    "No valid questions found in 'questions.json'. Please check the file format."
                )

            self.all_questions = valid_questions

        except json.JSONDecodeError:
            messagebox.showerror(
                "JSON Error",
                "Unable to load quiz questions.\n'questions.json' contains invalid JSON syntax."
            )
            self.all_questions = []
        except Exception as err:
            messagebox.showerror(
                "Load Error",
                f"An error occurred while loading questions:\n{str(err)}"
            )
            self.all_questions = []

    # ---------------------------------------------------------
    # Screen 1: Welcome Screen
    # ---------------------------------------------------------

    def show_welcome_screen(self):
        """Display the welcome screen with difficulty selection."""
        self.cancel_timer()
        self.clear_screen()

        # Main container frame
        self.current_frame = tk.Frame(self.root, bg=self.bg_color)
        self.current_frame.pack(expand=True, fill="both", padx=30, pady=30)

        # Centered white card container
        card = tk.Frame(
            self.current_frame,
            bg=self.card_color,
            bd=1,
            relief="solid",
            highlightbackground="#e2e8f0",
            highlightthickness=1,
        )
        card.pack(expand=True, fill="both", padx=20, pady=20)

        # Title Label
        title_label = tk.Label(
            card,
            text="Smart Quiz Game",
            font=("Helvetica", 28, "bold"),
            fg=self.text_dark,
            bg=self.card_color,
        )
        title_label.pack(pady=(45, 10))

        # Description Subtitle
        desc_label = tk.Label(
            card,
            text="Test your knowledge and improve your score!",
            font=("Helvetica", 14),
            fg=self.text_muted,
            bg=self.card_color,
        )
        desc_label.pack(pady=(0, 35))

        # Difficulty Heading
        diff_heading = tk.Label(
            card,
            text="Choose Difficulty Level",
            font=("Helvetica", 16, "bold"),
            fg=self.text_dark,
            bg=self.card_color,
        )
        diff_heading.pack(pady=(5, 15))

        # Difficulty Options Frame
        diff_frame = tk.Frame(card, bg=self.card_color)
        diff_frame.pack(pady=(0, 35))

        difficulties = [
            ("Easy", "Easy", "#16a34a"),
            ("Medium", "Medium", "#d97706"),
            ("Hard", "Hard", "#dc2626"),
        ]

        # Radio Buttons for Easy, Medium, Hard
        for label, value, color in difficulties:
            rb = tk.Radiobutton(
                diff_frame,
                text=label,
                value=value,
                variable=self.selected_difficulty,
                font=("Helvetica", 13, "bold"),
                bg=self.card_color,
                fg=color,
                activebackground=self.card_color,
                selectcolor="#f1f5f9",
                padx=15,
                pady=6,
                cursor="hand2",
            )
            rb.pack(side="left", padx=12)

        # Start Quiz Button
        start_btn = tk.Button(
            card,
            text="Start Quiz",
            font=("Helvetica", 15, "bold"),
            bg=self.primary_color,
            fg="#ffffff",
            activebackground=self.primary_hover,
            activeforeground="#ffffff",
            padx=40,
            pady=12,
            relief="flat",
            cursor="hand2",
            command=self.start_quiz,
        )
        start_btn.pack(pady=(10, 40))

    # ---------------------------------------------------------
    # Quiz Initialization & Progression
    # ---------------------------------------------------------

    def start_quiz(self):
        """
        Validate selection, filter questions by difficulty,
        randomize them, and initiate the first question.
        """
        difficulty = self.selected_difficulty.get()

        # Ensure the user has picked a difficulty
        if not difficulty:
            messagebox.showwarning(
                "Difficulty Required",
                "Please select a difficulty level (Easy, Medium, or Hard) to begin!"
            )
            return

        # Filter questions matching the selected difficulty
        filtered_questions = [
            q for q in self.all_questions if q.get("difficulty") == difficulty
        ]

        if not filtered_questions:
            messagebox.showwarning(
                "No Questions",
                f"No questions are available for '{difficulty}' difficulty."
            )
            return

        # Randomize questions and pick up to 10 questions for this round
        random.shuffle(filtered_questions)
        total_to_pick = min(10, len(filtered_questions))
        self.quiz_questions = filtered_questions[:total_to_pick]

        # Reset quiz state variables
        self.score = 0
        self.current_question_index = 0
        self.buttons_locked = False

        # Display the first question
        self.show_question()

    # ---------------------------------------------------------
    # Screen 2: Quiz Screen
    # ---------------------------------------------------------

    def show_question(self):
        """
        Render the current question, randomized answer options,
        score display, and reset/start the 15-second timer.
        """
        self.cancel_timer()

        # Check if all questions in the quiz have been answered
        if self.current_question_index >= len(self.quiz_questions):
            self.show_result_screen()
            return

        self.clear_screen()
        self.buttons_locked = False
        self.option_buttons.clear()

        # Retrieve current question data
        current_data = self.quiz_questions[self.current_question_index]
        question_text = current_data["question"]
        correct_answer = current_data["correct_answer"]
        difficulty = current_data["difficulty"]

        # Copy options and shuffle them so choices appear in random order
        shuffled_options = list(current_data["options"])
        random.shuffle(shuffled_options)

        # Main Quiz Frame
        self.current_frame = tk.Frame(self.root, bg=self.bg_color)
        self.current_frame.pack(expand=True, fill="both", padx=30, pady=25)

        # Top Bar: Difficulty, Score, and Timer
        top_bar = tk.Frame(self.current_frame, bg=self.card_color, relief="solid", bd=1)
        top_bar.pack(fill="x", padx=10, pady=(0, 15), ipady=8)

        # Difficulty Badge
        diff_label = tk.Label(
            top_bar,
            text=f"Difficulty: {difficulty}",
            font=("Helvetica", 12, "bold"),
            fg=self.text_dark,
            bg=self.card_color,
        )
        diff_label.pack(side="left", padx=20)

        # Score Counter
        self.score_label = tk.Label(
            top_bar,
            text=f"Score: {self.score}",
            font=("Helvetica", 13, "bold"),
            fg=self.primary_color,
            bg=self.card_color,
        )
        self.score_label.pack(side="left", expand=True)

        # Countdown Timer Label
        self.timer_label = tk.Label(
            top_bar,
            text=f"Time: {self.time_left}s",
            font=("Helvetica", 13, "bold"),
            fg=self.warning_color,
            bg=self.card_color,
        )
        self.timer_label.pack(side="right", padx=20)

        # Question Card Container
        q_card = tk.Frame(self.current_frame, bg=self.card_color, relief="solid", bd=1)
        q_card.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        # Question Progress (e.g. "Question 1 of 10")
        total_q = len(self.quiz_questions)
        prog_label = tk.Label(
            q_card,
            text=f"Question {self.current_question_index + 1} of {total_q}",
            font=("Helvetica", 12, "bold"),
            fg=self.text_muted,
            bg=self.card_color,
        )
        prog_label.pack(anchor="w", padx=25, pady=(15, 5))

        # Question Text
        q_label = tk.Label(
            q_card,
            text=question_text,
            font=("Helvetica", 15, "bold"),
            fg=self.text_dark,
            bg=self.card_color,
            wraplength=680,
            justify="left",
        )
        q_label.pack(anchor="w", padx=25, pady=(5, 15))

        # Answer Options Container (Grid layout for clean 2x2 buttons)
        options_container = tk.Frame(q_card, bg=self.card_color)
        options_container.pack(fill="both", expand=True, padx=25, pady=(0, 10))

        # Configure grid columns with equal weight
        options_container.columnconfigure(0, weight=1)
        options_container.columnconfigure(1, weight=1)

        prefixes = ["A", "B", "C", "D"]

        for i, option_text in enumerate(shuffled_options):
            prefix = prefixes[i]
            btn_text = f"{prefix}.  {option_text}"

            # Create button with default styling
            btn = tk.Button(
                options_container,
                text=btn_text,
                font=("Helvetica", 12),
                bg=self.btn_bg,
                fg=self.text_dark,
                activebackground="#e2e8f0",
                activeforeground=self.text_dark,
                relief="flat",
                bd=1,
                padx=15,
                pady=12,
                anchor="w",
                justify="left",
                wraplength=310,
                cursor="hand2",
            )

            # Assign click command using helper method to avoid closure issues
            btn.config(
                command=lambda opt=option_text, b=btn: self.handle_answer(opt, b, correct_answer)
            )

            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
            self.option_buttons.append((btn, option_text))

        # Feedback Label (shows Correct!, Wrong!, or Time's Up!)
        self.feedback_label = tk.Label(
            q_card,
            text="",
            font=("Helvetica", 13, "bold"),
            fg=self.text_dark,
            bg=self.card_color,
        )
        self.feedback_label.pack(pady=(5, 15))

        # Initialize and start the 15-second countdown timer
        self.time_left = 15
        self.update_timer_label()
        self.start_timer()

    # ---------------------------------------------------------
    # Timer Implementation
    # ---------------------------------------------------------

    def update_timer_label(self):
        """Update the timer label display and text color."""
        if self.timer_label is not None:
            self.timer_label.config(text=f"Time: {self.time_left}s")
            if self.time_left <= 5:
                self.timer_label.config(fg=self.danger_color)
            else:
                self.timer_label.config(fg=self.warning_color)

    def start_timer(self):
        """Schedule the next 1-second countdown tick using root.after()."""
        self.cancel_timer()
        if self.time_left > 0:
            self.timer_id = self.root.after(1000, self.countdown_tick)
        else:
            self.handle_timeout()

    def countdown_tick(self):
        """Decrease time remaining by 1 second and schedule the next tick."""
        self.time_left -= 1
        self.update_timer_label()

        if self.time_left > 0:
            self.timer_id = self.root.after(1000, self.countdown_tick)
        else:
            self.handle_timeout()

    # ---------------------------------------------------------
    # Answer Checking & Timeout Handling
    # ---------------------------------------------------------

    def handle_answer(self, selected_option, clicked_button, correct_answer):
        """
        Process user's selected answer, update score,
        provide visual feedback, and transition automatically.
        """
        # Prevent multiple clicks on the same question
        if self.buttons_locked:
            return

        self.buttons_locked = True
        self.cancel_timer()

        # Check if the chosen answer is correct
        if selected_option == correct_answer:
            self.score += 1
            self.feedback_label.config(text="Correct!  +1 Point", fg=self.success_color)
            clicked_button.config(bg=self.success_color, fg="#ffffff", activebackground=self.success_color)
        else:
            self.feedback_label.config(text=f"Wrong! Correct: {correct_answer}", fg=self.danger_color)
            clicked_button.config(bg=self.danger_color, fg="#ffffff", activebackground=self.danger_color)
            # Highlight the correct button in green so user learns the right answer
            for btn, opt_text in self.option_buttons:
                if opt_text == correct_answer:
                    btn.config(bg=self.success_color, fg="#ffffff")

        # Update score counter in top bar
        if self.score_label is not None:
            self.score_label.config(text=f"Score: {self.score}")

        # Automatically advance to next question after 1.2 seconds
        self.root.after(1200, self.advance_to_next_question)

    def handle_timeout(self):
        """Handle question expiration when countdown timer reaches zero."""
        if self.buttons_locked:
            return

        self.buttons_locked = True
        self.cancel_timer()

        current_data = self.quiz_questions[self.current_question_index]
        correct_answer = current_data["correct_answer"]

        # Display timeout feedback
        if self.feedback_label is not None:
            self.feedback_label.config(text=f"Time's Up! Correct: {correct_answer}", fg=self.danger_color)

        # Highlight the correct button in green
        for btn, opt_text in self.option_buttons:
            if opt_text == correct_answer:
                btn.config(bg=self.success_color, fg="#ffffff")

        # Automatically advance to next question after 1.5 seconds
        self.root.after(1500, self.advance_to_next_question)

    def advance_to_next_question(self):
        """Move question pointer forward and display next question."""
        self.current_question_index += 1
        self.show_question()

    # ---------------------------------------------------------
    # Screen 3: Result Screen
    # ---------------------------------------------------------

    def show_result_screen(self):
        """Display final score, percentage, and performance feedback."""
        self.cancel_timer()
        self.clear_screen()

        total_questions = len(self.quiz_questions)
        percentage = int(round((self.score / total_questions) * 100)) if total_questions > 0 else 0

        # Determine performance feedback message based on score percentage
        if percentage >= 90:
            performance_title = "Excellent! Outstanding Job!"
            performance_msg = "You have exceptional knowledge in this subject."
            performance_color = self.success_color
        elif percentage >= 70:
            performance_title = "Very Good! Keep Practicing!"
            performance_msg = "Great effort! You clearly have a strong foundation."
            performance_color = self.primary_color
        elif percentage >= 50:
            performance_title = "Good Effort! You Can Improve!"
            performance_msg = "A decent attempt! Practice a bit more to achieve higher scores."
            performance_color = self.warning_color
        else:
            performance_title = "Keep Practicing and Try Again!"
            performance_msg = "Do not be discouraged! Review the concepts and play again."
            performance_color = self.danger_color

        # Main Container
        self.current_frame = tk.Frame(self.root, bg=self.bg_color)
        self.current_frame.pack(expand=True, fill="both", padx=30, pady=30)

        # White Card Container
        card = tk.Frame(
            self.current_frame,
            bg=self.card_color,
            bd=1,
            relief="solid",
            highlightbackground="#e2e8f0",
            highlightthickness=1,
        )
        card.pack(expand=True, fill="both", padx=20, pady=20)

        # Header Title
        title_label = tk.Label(
            card,
            text="Quiz Completed!",
            font=("Helvetica", 26, "bold"),
            fg=self.text_dark,
            bg=self.card_color,
        )
        title_label.pack(pady=(35, 15))

        # Score Display (e.g. "Your Score: 8 / 10")
        score_display = tk.Label(
            card,
            text=f"Your Score: {self.score} / {total_questions}",
            font=("Helvetica", 20, "bold"),
            fg=self.primary_color,
            bg=self.card_color,
        )
        score_display.pack(pady=5)

        # Percentage Display (e.g. "Percentage: 80%")
        percent_display = tk.Label(
            card,
            text=f"Score Percentage: {percentage}%",
            font=("Helvetica", 15, "bold"),
            fg=self.text_muted,
            bg=self.card_color,
        )
        percent_display.pack(pady=(0, 15))

        # Performance Evaluation Heading
        perf_label = tk.Label(
            card,
            text=performance_title,
            font=("Helvetica", 16, "bold"),
            fg=performance_color,
            bg=self.card_color,
        )
        perf_label.pack(pady=(5, 5))

        # Performance Subtitle
        perf_sub = tk.Label(
            card,
            text=performance_msg,
            font=("Helvetica", 13),
            fg=self.text_muted,
            bg=self.card_color,
        )
        perf_sub.pack(pady=(0, 30))

        # Action Buttons Container (Play Again & Exit)
        btn_frame = tk.Frame(card, bg=self.card_color)
        btn_frame.pack(pady=(10, 35))

        play_again_btn = tk.Button(
            btn_frame,
            text="Play Again",
            font=("Helvetica", 14, "bold"),
            bg=self.primary_color,
            fg="#ffffff",
            activebackground=self.primary_hover,
            activeforeground="#ffffff",
            padx=28,
            pady=10,
            relief="flat",
            cursor="hand2",
            command=self.reset_and_play_again,
        )
        play_again_btn.pack(side="left", padx=15)

        exit_btn = tk.Button(
            btn_frame,
            text="Exit Game",
            font=("Helvetica", 14, "bold"),
            bg="#f1f5f9",
            fg=self.text_dark,
            activebackground="#e2e8f0",
            activeforeground=self.text_dark,
            padx=28,
            pady=10,
            relief="flat",
            cursor="hand2",
            command=self.root.destroy,
        )
        exit_btn.pack(side="left", padx=15)

    # ---------------------------------------------------------
    # Screen Reset & Cleanup
    # ---------------------------------------------------------

    def reset_and_play_again(self):
        """
        Reset quiz state variables and navigate back
        to the difficulty selection welcome screen.
        """
        self.cancel_timer()
        self.score = 0
        self.current_question_index = 0
        self.time_left = 15
        self.buttons_locked = False
        self.quiz_questions = []
        self.selected_difficulty.set("")
        self.show_welcome_screen()


# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    # Create the primary Tkinter window
    root = tk.Tk()
    app = QuizApp(root)
    # Start the event processing loop
    root.mainloop()
