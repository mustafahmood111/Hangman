# **********************************************************
# *    Program: Hangman                                    *
# *    Date: August 14 , 2022                              *
# *    Name: Mustafa Hmood                                 *
# *    Description: Hangman made with Tkinter.             *
# **********************************************************

from tkinter import *
from tkinter import messagebox as mb, ttk
from PIL import Image, ImageTk
import random
import sys

# Set the default difficulty to easy
DIFFICULTY = 0

# Create a window
hangwin = Tk()                         # Define the window as "hangwin"
hangwin.title("Hangman")               # Give the window the title "Hangman"
hangwin.geometry("730x610+450+150")    # Resize the window to fit a picture and some other widgets
hangwin.resizable(False, False)        # The window size should not be adjustable by the user
hangwin.configure(bg="light gray")     # The color of the window will be light gray
hangwin.iconbitmap("icon2.ico")        # Change the window icon

word_lists = {}

# Create the application icon
if sys.platform.startswith('hangwindow'):
    hangwin.iconbitmap('hanger.gif')
else:
    logo = PhotoImage(file='hanger.gif')
    hangwin.call('wm', 'iconphoto', hangwin._w, logo)

# Load the word lists from files
for i in range(0, 3):
    words = open(f"hangwords{i}.txt", 'r')
    word_lists[i] = [x.upper() for x in words.read().split("\n") if 3<len(x)<14 and x.isalpha()]

# Load the pictures from files
pics = []
for i in range(0, 10):
    pic = Image.open(f"hangpics/hang{i}.png")
    pic_resize = pic.resize((195, 250), Image.ANTIALIAS)
    pics.append(ImageTk.PhotoImage(pic_resize))

# Create the heading and input it into the window
head = Label(hangwin, text="HANGMAN")

# The font veradana is great for a huge title that has a size of 36.
head_fnt = ("Calibri", 40, "bold")

# Use 'head_fnt' as a header with dark red colour and a light gray background
# for design. The gray contrasts well with the red.
head.configure(font=head_fnt, fg="dark red", bg="light gray")

# Place it in the middle but above the frame with the word and canvas
head.place(x=230, y=30)

# Input the canvas in the window, wide enough to fit the image, word, and the letters.
can = Canvas(hangwin, highlightbackground="black", bg="blue", width=600, height=280, bd=5)
can.place(x=50, y=100)      # Place the canvas in the middle of the window.

# Create image border
picframe = Frame(hangwin, bg="black", width=203, height=258)
picframe.place(x=448, y=118)

# Create the image
piclabel = Label(hangwin, image=pics[0])
piclabel.place(x=450, y=120)

# Initialize word display and fail count
current_word = random.choice(word_lists[DIFFICULTY])
word_display = Label(hangwin, text="_  " * len(current_word))

# Use Comic Sans for the font so the letters stick out a bit more, with a larger font of 20.
# Place it to the left of the pictures. It also must be placed above the letters.
word_display_fnt = ("Comic Sans MS", 20)
word_display.configure(font=word_display_fnt, fg="red", bg="black")   # cCnfigure the font.
word_display.place(x=80, y=180)                                         # Place the word within the frame

# When the user guesses the incorrect letter they will have
# more mistakes. But we must start with 0 mistakes.
fail = 0

# Give the letters attributes for when they are displayed.
letter_width = 5
letter_height = 1
letter_bg = "green"
letter_fg = "red"

# Initialize dictionary of buttons
buttons = {}


# Define the function that will allow the user to pick letters.
# Word will be a string.
def find_char(word, letter):
    count = word.count(letter)
    t = word.find(letter)

    loc_arr = [t]
    while len(loc_arr) < count:
        loc_arr.append(word.find(letter, t + 1))

    return loc_arr


# Define the function that will affect the game based on the result of the
# letter picked. If the letter picked is not within the randomized word
# then the 'hangman' photo is changed.
def letter_clk(letter):
    buttons[letter].config(bg="#ff0000", state=DISABLED)
    current_display = word_display["text"].split("  ")
    locs = find_char(current_word, letter)

    global fail
    # If the letter is correct, ten we place the letter into the word.
    if locs[0] != -1:
        for loc in locs:
            current_display[loc] = letter
    # If the letter is incorrect, then the mistake count is increased by 1
    else:
        fail += 1
        if fail < 7:
            # Everytime the user makes a mistake the photo is updated as they have
            # the same name, but it is dependent on the number of mistakes.
            piclabel['image'] = pics[fail]

        # If there are more than 7 mistakes the final picture of the dead
        # hangman stick figure will appear.
        else:
            piclabel['image'] = pics[8]
            mb.showinfo("Defeat", f"You have lost. The word was {current_word}.")

            # A message box will also open up and tell the user
            # that they have lost with the correct word.
            for button in buttons.values():
                button.config(state=DISABLED)

    word_display["text"] = '  '.join(current_display)

    # If there are no more underscores in the word, the user has
    # won and the final picture of the victory will appear.
    if "_" not in current_display:
        piclabel['image'] = pics[9]
        mb.showinfo("Victory", "You have found the word!")
        for button in buttons.values():
            button.config(state=DISABLED)


# Define the reset function. We will have to re-run some
# previous functions mentioned to restart everything.
def reset():
    # Make the variables global, so they can be accessed throughout the entire project.
    global current_word, word_display, fail

    # Pull a new random word from the list of words
    current_word = random.choice(word_lists[DIFFICULTY])
    word_display["text"] = "_  " * len(current_word)

    # Place the image in the same place it was originally been
    piclabel['image'] = pics[0]

    # Reset mistakes counter
    fail = 0

    # Put the letters that can be clicked on back in the frame as something new.
    for button in buttons.values():
        button.config(state=NORMAL, bg=letter_bg)


# Define the instruction function. This will create a permanent messagebox
# that will print a message, as long as the label button is created.
def instr():
    mb.showinfo("Instructions", "Find the hidden word to save the Dude from gallows. Mistakes lead to Death!")

# Label for game difficulty drop down
difflabel = Label(text = "Which difficulty would you preffer?")
difflabel.place(x=200, y=530)
# Define the difficulty changing function.
def difficulty_change(event):
    global DIFFICULTY
    diff = difficulty.get()
    if diff == 'Easy':
        DIFFICULTY = 0
    elif diff == 'Medium':
        DIFFICULTY = 1
    elif diff == 'Hard':
        DIFFICULTY = 2


# Create the button that resets the game. Create a command for it to be clicked.
res = Button(hangwin, text="New Game", width=20, height=2, bd=3, bg="brown", fg="red", command=reset)

# Place the button in the bottom right. This will be below the picture of the hangman.
# This is the optimal location as the user will see the state of the hangman and be able to reset the game.
res.place(x=490, y=530)

# Create the instructions button, that helps the user understand the game rules
# and how many attempts they get until they lose.
inst = Button(hangwin, text="Instructions", width=12, height=2, bd=3, command=instr)
inst.place(x=30, y=530)

# Create a combo box that allows the user to choose which difficulty of the hangman game they would prefer.
# The harder the difficulty the tougher and longer the words are.
difficulty = ttk.Combobox(hangwin, values=('Easy', 'Medium', 'Hard'))
difficulty.bind("<<ComboboxSelected>>", difficulty_change)
difficulty.current(0)
difficulty.place(x=200, y=550)

# Create the buttons for letters in the correct range. Each iteration
# of the loop places a letter in each row.
for i, j, k in zip(range(65, 78), range(78, 91), range(30, 631, 50)):
    letter1 = chr(i)
    letter2 = chr(j)

    # Create a button. The text should be the letter. We use a 'lambda' so
    # we can pass an argument when we call 'letter_clk'.
    buttons[letter1] = Button(hangwin, text=letter1, width=letter_width, height=letter_height, bg=letter_bg, fg=letter_fg)
    buttons[letter1].bind("<Button-1>", lambda event: letter_clk(event.widget['text']))
    buttons[letter1].place(x=k, y=420)

    buttons[letter2] = Button(hangwin, text=letter2, width=letter_width, height=letter_height, bg=letter_bg, fg=letter_fg)
    buttons[letter2].bind("<Button-1>", lambda event: letter_clk(event.widget['text']))
    buttons[letter2].place(x=k, y=450)

mb.showinfo('Hangman introduction', (
    "Welcome to Hangman. \n"
    "Click on 'Start new game' to begin a new game. \n"
    "Then choose letters to attempt to fully guess the word. \n"
    "If you make more than 7 errors your stick figure will get hanged. \n"
    "Save HIM!"))

# Finish the code by using mainloop to keep the screen active.
hangwin.mainloop()
