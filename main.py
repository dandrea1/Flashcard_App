from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# ---------------------------- Flashcard Setup ------------------------------- #
try:
    word_dataframe = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient='records')
else:
    words_to_learn = word_dataframe.to_dict(orient='records')




def next_card():
    global current_card, flip_timer
    current_card = random.choice(words_to_learn)
    window.after_cancel(flip_timer)
    canvas.itemconfig(canvas_image, image=front_image)
    canvas.itemconfig(language_text, text="French", fill='black')
    canvas.itemconfig(word_text, text=f"{current_card['French']}", fill='black')
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------- Update Word Bank Based on User Knowledge ------------------------------- #
def is_known():
    words_to_learn.remove(current_card)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- Flip Card After 3 seconds ------------------------------- #

def flip_card():
    global current_card
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(language_text, fill="white", text="English")
    canvas.itemconfig(word_text, fill="white", text=f"{current_card['English']}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Create Images
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

# Create Right Button
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=0, row=1)

# Create Wrong Button
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

# Create Flash Card
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_image = canvas.create_image(400, 263, image=front_image)
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, columnspan=2, row=0)

next_card()
window.mainloop()
