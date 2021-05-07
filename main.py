from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


# -----------------ACCESSING DATA SECTION --------------------------#
# Python attempts to open words_to_learn.csv. At first use this does not exist yet;
# except block deals with this instance and creates a to_learn dictionary

try:
    data = pandas.read_csv("words_to_learn.csv")

except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ------------ FLASH CARD FUNCTIONALITY--------------#

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)                     # this sets the last flip timer to 0
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_img)
    flip_timer = window.after(3000, func=flip_card)     # starts the new flip timer


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=back_img)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()

#----------------------- GUI ------------------------#

window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)  # after 3000 milliseconds we are calling flip_card()
# flip_timer variable allows us to count down for each card being shown


# card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="card_front.png")
back_img = PhotoImage(file="card_back.png")
canvas_image = canvas.create_image(400, 260, image=front_img)
card_title = canvas.create_text(400, 150, text="Language", fill="grey", font=("Courier", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", fill="grey", font=("Courier", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


# right button
right = PhotoImage(file="right.png")
right_button = Button(image=right, highlightthickness=0, command=is_known)
right_button.grid(column=0, row=1)


# wrong button
wrong = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()

window.mainloop()
