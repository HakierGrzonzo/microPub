from micropub.epub import Epub
from micropub.renderer import Renderer
from micropub.renderer.cssParser import Parser
import sys, os, curses, time, json

def main():
    baseSheet = list()
    try:
        with open(os.path.expanduser("~/.config/micropub/base.css")) as f:
            baseSheet.append(Parser(f.read()))
    except FileNotFoundError:
        print("No base stylesheet found!")

    ebook = Epub(sys.argv[1])
    cache = dict()
    chapters = list()
    for element in ebook.spine:
        chapter = Renderer(element, ebook.get, cache, baseSheet)
        chapters.append(chapter)
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.clear()
        stdscr.refresh()
        rows, cols = stdscr.getmaxyx()

        tooltip = curses.newwin(1, cols, rows -1, 0)
        tooltip.addstr(0, 0, "µPub v.0".center(cols - 1), curses.A_REVERSE)
        tooltip.refresh()

        readerWindow = curses.newwin(rows - 1, cols, 0, 0)
        chapters[0].render(readerWindow)

        time.sleep(5)
    finally:
        curses.endwin()


if __name__ == "__main__":
    main()
