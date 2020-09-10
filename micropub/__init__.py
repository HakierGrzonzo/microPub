from micropub.epub import Epub
from micropub.renderer import Renderer
import sys

def main():
    ebook = Epub(sys.argv[1])

if __name__ == "__main__":
    main()