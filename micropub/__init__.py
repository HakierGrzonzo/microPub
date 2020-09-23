from micropub.epub import Epub
from micropub.renderer import Renderer
from micropub.renderer.cssParser import Parser
import sys, os

def main():
    baseSheet = list()
    try:
        with open(os.path.expanduser("~/.config/micropub/base.css")) as f:
            baseSheet.append(Parser(f.read()))
    except FileNotFoundError:
        print("No base stylesheet found!")

    ebook = Epub(sys.argv[1])
    cache = dict()
    for element in ebook.spine:
        print("\n", element.filename)
        renderer = Renderer(element, ebook.get, cache, baseSheet)
        input()

if __name__ == "__main__":
    main()
