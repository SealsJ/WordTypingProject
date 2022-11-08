import curses
from curses import wrapper
import time
import random


#Start game loop and prompt user if they want to play the game
def startScreen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress Enter to begin the game!")
    stdscr.refresh()
    #Used to wait for user to input something and program doesn't close automatically
    stdscr.getkey()

#Creating display for the overlay of text typing
def displayText(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    #we can specify the row and column we want this text through coordinate system
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    #This will overlay what user is typing over target text, incremented by 1
    for i, character in enumerate(current):
        correctCharacter = target[i]
        color = curses.color_pair(1)
        #if not the correct character we will change color of text for user
        if character != correctCharacter:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, character, color)

#Randomize the text user has to write out from text file
def loadText():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


#Establishing the text / amount of time that has elapsed
def wpmTest(stdscr):
    targetText = loadText()
    currentText = []
    wpm = 0
    startTime = time.time()
    #do not delay based on user input so WPM can decrease while nothing happens
    stdscr.nodelay(True)

    while True:
        timeElapsed = max(time.time() - startTime, 1)
        #equation for calculating wpm; assuming a word has 5 characters
        wpm = round((len(currentText) / (timeElapsed / 60)) / 5)

        #Use clear so we don't keep adding to line of text and can write out sentence
        stdscr.clear()
        displayText(stdscr, targetText, currentText, wpm)
        stdscr.refresh()

        #When user gets to end of text we can end the game / prompt to replay
        #got to compare current and target text but current text is index so got to convert to string
        if "".join(currentText) == targetText:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        #allows user to hit escape to break out of the game using ASCII
        if ord(key) == 27:
            break
        #handle special characters like backspace across different operating systems
        if key in ("KEY_BACKSPACE", '\b', "\x7f", "^?"):
            if len(currentText) > 0:
                currentText.pop()
        elif len(currentText) < len(targetText):
            currentText.append(key)

#function to write directly to terminal and add a string
def main(stdscr):
    #add color to text in terminal
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    startScreen(stdscr)

    #prompt user to play again
    while True:
        wpmTest(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press Enter for next challenge or Escape to leave!")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)