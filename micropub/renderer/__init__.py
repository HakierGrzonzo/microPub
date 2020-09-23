from micropub.renderer.cssParser import Parser
from micropub.renderer.element import Element
from bs4 import BeautifulSoup as Soup
import json

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
        self.element = Element(self.soup.find("body"), self) 
    
    def render(self, window):
        pass