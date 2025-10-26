import math
import pygame
from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
MUSIC_MODE = "loop"
MUSIC_FILE = "music.mp3"
# ---------------------------- PYGAME AUDIO SETUP ------------------------------- #
try:
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)  # volume 0.0 - 1.0
except Exception as e:
    print("Warning: pygame mixer failed to initialize:", e)

def play_music():
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(MUSIC_FILE)
            if MUSIC_MODE == "loop":
                pygame.mixer.music.play(loops=-1)
            else:
                pygame.mixer.music.play(loops=0)
    except Exception as e:
        print("Could not play music:", e)

def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print("Could not stop music:", e)

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text,text="00:00")
    label.config(text="Timer")
    global reps
    reps = 0
    stop_music()
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 6
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 2 != 0:
        play_music()
        count_down(work_sec)
        label.config(text="Work",fg=GREEN)
    elif reps == 8:
        stop_music()
        count_down(long_break_sec)
        label.config(text="Long break",fg=RED)
    else:
        stop_music()
        count_down(short_break_sec)
        label.config(text="Short break",fg=PINK)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text , text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000,count_down , count-1)
    else:
        start_timer()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("All Roads Lead to Rome")
window.config(padx=100 , pady=50,bg=YELLOW)

canvas = Canvas(width= 200 ,height=224, bg=YELLOW, highlightthickness=0)
image = PhotoImage(file="AllRoadsLeadtoRome.png")
canvas.create_image(100, 112, image=image)
timer_text = canvas.create_text(103,130,text="00:00", fill="white",font=(FONT_NAME,35,"bold"))
canvas.grid(column=1,row=1)

label = Label(text="Timer",fg=GREEN,bg=YELLOW, font=(FONT_NAME,50))
label.grid(column=1,row=0)

start_button = Button(text="Start",command=start_timer)
start_button.grid(column=0,row=2)
reset_button = Button(text="Reset",command=reset_timer)
reset_button.grid(column=2,row=2)

window.mainloop()