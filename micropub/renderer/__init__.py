from micropub.renderer.cssParser import Parser
from bs4 import BeautifulSoup as Soup

class Renderer:
    def __init__(self, html, getCallback, cssCache = dict()):
        self.soup = Soup(html.content, features="lxml")
        self.cssCache = cssCache
        
        # Get css from links
        for link in self.soup.find_all("link", rel="stylesheet"):
            if link["href"] not in self.cssCache.keys():
                css = getCallback(link["href"], relative_to=html.filename)
                self.cssCache[link["href"]] = Parser(css)

