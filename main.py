import tkinter as tk
import random
from tkinter import messagebox

# Choose a random word
words = ["Entertairment", "Engineering", "Adventure", "Psycology", "Brotherhood","Situationship","Boating","Racing","Scrolling","Omnipotentd"]
word_to_guess = random.choice(words).upper()
guess_character = ["_"] * len(word_to_guess)
attempts = 6

# Setup the main window
window = tk.Tk()
window.title("Hangman Game")
window_width = 400
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
window.config(bg="lightblue")
window.resizable(False, False)

# Canvas for drawing
canvas = tk.Canvas(window, width=300, height=300, bg="beige")
canvas.pack(pady=20)

# Hangman body parts coordinates
hangman_parts = {
    "head": (185, 60, 225, 100),
    "body": (205, 100, 205, 170),
    "left_arm": (205, 110, 175, 140),
    "right_arm": (205, 110, 235, 140),
    "left_leg": (205, 170, 175, 210),
    "right_leg": (205, 170, 235, 210),
}


attempts_label = tk.Label(window, text=f"You have {attempts} attempts to guess",
                          font=("Arial", 14, "bold"), bg="yellow", fg="darkred",relief= 'sunken')
attempts_label.place(x=50, y=350, width=300, height=30)
# Display guessed letters
showing_screen = tk.Label(window, text=" ".join(guess_character), font=("Arial", 20, "bold"), fg="black", bg="white")
showing_screen.place(x=50, y=400, width=300, height=35)

# Entry box for guessing letters
guess_entry = tk.Entry(window, font=("Arial", 18))
guess_entry.place(x=100, y=450, width=200)

# Draw the gallows
def draw_gallows():
    canvas.create_line(65, 250, 145, 250, width=10)
    canvas.create_line(105, 250, 105, 20, width=5)
    canvas.create_line(105, 20, 205, 20, width=5)
    canvas.create_line(205, 20, 205, 60, width=5)

# Draw hangman depending on remaining attempts
def draw_hangman(attempts_left):
    parts_order = ["head", "body", "left_arm", "right_arm", "left_leg", "right_leg"]
    part_index = 6 - attempts_left
    if part_index < len(parts_order):
        part = parts_order[part_index]
        canvas.create_line(hangman_parts[part], width=5)

# Check if player has won
def check_win():
    
    return "_" not in guess_character

# Reset game
def reset():
    canvas.config(bg="beige")
    global word_to_guess, guess_character, attempts
    word_to_guess = random.choice(words).upper()
    guess_character = ["_"] * len(word_to_guess)
    attempts = 6
    showing_screen.config(text=" ".join(guess_character))
    canvas.delete("all")
    draw_gallows()
    guess_entry.delete(0, tk.END)

# Handle guessing logic
def guess_word():
    global attempts
    letter = guess_entry.get().upper()
    guess_entry.delete(0, tk.END)

    if not letter.isalpha() or len(letter) != 1:
        messagebox.showwarning("Invalid Input", "Please enter a single alphabet letter.")
        return

    if letter in guess_character:
        messagebox.showinfo("Already Guessed", f"You already guessed '{letter}'")
        return

    if letter in word_to_guess:
        for i, l in enumerate(word_to_guess):
            if l == letter:
                guess_character[i] = letter
        showing_screen.config(text=" ".join(guess_character))

        if check_win():
            canvas.config(bg="green")
            messagebox.showinfo("Congratulations!", f"You've guessed the word: {word_to_guess}")
            reset()
    else:
        attempts -= 1
        draw_hangman(attempts)
        if attempts == 0:
            canvas.config(bg="red")
            canvas.create_oval(hangman_parts["head"], width=5)
            messagebox.showinfo("Game Over", f"You lost! The word was: {word_to_guess}")
            reset()

# Button to submit guess
guess_btn = tk.Button(window, text="Guess", command=guess_word, font=("Arial", 20, 'bold'),
                      bg="black", fg="white", relief="raised", bd=5, padx=20, pady=10,
                      activebackground="green", activeforeground="white", borderwidth=4)
guess_btn.place(x=100, y=500, width=200, height=40)

#this is use to bind the enter key with the guess button if i wanna bind some other key like A so use <a>
window.bind('<Return>', lambda event: guess_btn.invoke()) 
window.focus()

# Initial draw
draw_gallows()

# Start the main event loop
window.mainloop()
