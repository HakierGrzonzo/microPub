from micropub.epub import Epub
from micropub.renderer import Renderer
import sys

def main():
    ebook = Epub(sys.argv[1])
    for element in ebook.spine:
        renderer = Renderer(element, ebook.get)

if __name__ == "__main__":
    main()