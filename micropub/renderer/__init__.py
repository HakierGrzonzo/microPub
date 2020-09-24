from micropub.renderer.cssParser import Parser, parseInTag
from micropub.renderer.element import Element
from bs4 import BeautifulSoup as Soup
import json, curses
from pprint import pprint as pp

class Renderer:
    def __init__(self, html, getCallback, cssCache = dict(), baseSheets = None):
        self.soup = Soup(html.content, features="lxml")
        self.cssCache = cssCache
        self.styles = list()
        if baseSheets is not None:
            self.styles += baseSheets

        # Get css from links
        for link in self.soup.find_all("link", rel="stylesheet"):
            if link["href"] not in self.cssCache.keys():
                css = getCallback(link["href"], relative_to=html.filename)
                parser = Parser(css)
                self.cssCache[link["href"]] = parser
                self.styles.append(parser)
            else:
                self.styles.append(self.cssCache[link["href"]])

        for style in self.soup.find_all("style"):
            parser = Parser(style.text)
            self.styles.append(parser)

        self.element = Element(self.soup.find("body"), self)
        pp(self.element.render())
        input()
    
    def render(self, window):
        window.addstr(0, 0, "test windowa", curses.A_BOLD)
        window.refresh()

    def resolveStyle(self, element) -> dict:
        rules = list()
        for stylesheet in self.styles:
            rules.append(stylesheet.getStyle(element.tag))
        rules.append(parseInTag(element.tag))
        rules.reverse()

        result = dict()
        for rule in rules:
            for key in rule.keys():
                result[key] = rule[key]
        return result