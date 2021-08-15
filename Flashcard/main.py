from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
english_meaning = None
try:
    csv_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    csv_data = pandas.read_csv("data/french_words.csv")

random_index_no = None
french_words_list = csv_data["French"].to_list()
english_meaning_list = csv_data["English"].to_list()


def slide_change():
    english_meaning = english_meaning_list[random_index_no]
    card_canvas.itemconfig(card_image, image=card_back_image)
    card_canvas.itemconfig(language_text, text="English")
    card_canvas.itemconfig(word, text=english_meaning)


def new_word_command():
    global flip_timer, random_index_no
    window.after_cancel(flip_timer)
    card_canvas.itemconfig(card_image, image=card_front_image)
    card_canvas.itemconfig(language_text, text="French")
    random_index_no = random.randint(0, len(french_words_list) - 1)
    french_word = french_words_list[random_index_no]
    card_canvas.itemconfig(word, text=french_word)
    flip_timer = window.after(3000, slide_change)


def tick_command():
    global random_index_no
    french_words_list.remove(french_words_list[random_index_no])
    english_meaning_list.remove(english_meaning_list[random_index_no])
    new_dict = {"French": french_words_list,
                "English": english_meaning_list
                }
    data = pandas.DataFrame(new_dict)
    data.to_csv("data/words_to_learn.csv")
    new_word_command()


# -----------------------------UI SETUP--------------------------------------------------
window = Tk()
window.title("Flashy")
window.configure(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, slide_change)

card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="../Flashcard/images/card_front.png")
card_canvas = Canvas(width=800, height=540, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = card_canvas.create_image(410, 280, image=card_front_image)
language_text = card_canvas.create_text(400, 150, text="", font=("arial", 40, "italic"))
word = card_canvas.create_text(400, 330, text="", font=("arial", 60, "bold"))
card_canvas.grid(row=0, column=0, columnspan=3)

cross_button_image = PhotoImage(file="../Flashcard/images/wrong.png")
cross_button = Button(image=cross_button_image, highlightthickness=0, command=new_word_command)
cross_button.grid(row=1, column=0)

tick_button_image = PhotoImage(file="../Flashcard/images/right.png")
tick_button = Button(image=tick_button_image, command=tick_command)
tick_button.grid(row=1, column=2)

new_word_command()
window.mainloop()
