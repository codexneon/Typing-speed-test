import curses # built in module for styling our terminal
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear() 
    stdscr.addstr("Welcome to Speed Typing Test !")
    stdscr.addstr("\nPress any key to begin") 
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr , target , current, wpm=0):
        stdscr.addstr(target)
        stdscr.addstr(1,0 ,f"WPM: {wpm}")

        for i, char in enumerate(current): # for looping through every char in list i.e current text
            correct_char = target[i]
            color = curses.color_pair(1)
            if char != correct_char:
                color = curses.color_pair(2) 

            stdscr.addstr(0 , i , char , color) # enumerate gives element from our current text as well as the index

def load_text():
    with open ("text.txt" , "r") as f: # with is a context manager 
        lines = f.readlines()
        return random.choice(lines).strip() 


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True) # nodelay : do not wait for user to input key , keep calculating wpm

    while True:
        time_elapsed = max(time.time() - start_time , 1) # time between new time and current time
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5) # gives us character per minute and when / 5 gives words per minute 
            # round gives us a round off number and not a decimal
        stdscr.clear()
        display_text(stdscr , target_text , current_text , wpm)   
        stdscr.refresh()

        if "".join(current_text) == target_text: #takes current text and joins it with the string i.e "" 
            stdscr.nodelay(False)
            break

        try:    
            key = stdscr.getkey() # block
        except:
            continue

        if ord(key) == 27: # 27 key - esc key
            break

        if key in ("KEY_BACKSPACE", '\b' , "\x7f"):
            if len(current_text) > 0:
                current_text.pop() # pop will remove the last character from the list when we use backspace
        elif len(current_text) < len(target_text):
            current_text.append(key)    

def main(stdscr): # stdscr : standard output screen
    curses.init_pair(1, curses.COLOR_GREEN , curses.COLOR_BLACK) #To add background and foreground to the text
    curses.init_pair(2, curses.COLOR_RED , curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE , curses.COLOR_BLACK)
    
    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0 ,"You completed the text !! Press any key to continue .....")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main) #passing main func to wrapper func