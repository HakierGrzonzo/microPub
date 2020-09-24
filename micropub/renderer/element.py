from bs4 import BeautifulSoup as Soup
from bs4 import Tag
from micropub.renderer.text import Text

class Element:
    def __init__(self, tag, renderer, parent = None):
        self.renderer = renderer
        self.parent = parent
        self.tag = tag
        self.children = list()
        self.style = self.renderer.resolveStyle(self)
        self.display = self.style.get("display", "inline")
        for child in tag.children:
            if isinstance(child, Tag):
                self.children.append(Element(child, renderer, self))
            else:
                self.children.append(Text(child, self))

    def render(self, force_inline = False):
        if self.display != "inline" and not force_inline:
            # handle block elements
            contents = list()
            lastParagraph = list()
            for child in self.children:
                if isinstance(child, Text):
                    lastParagraph.append(child)
                elif child.display == "inline":
                    childContent = child.render(force_inline)
                    lastParagraph += childContent
                else:
                    childContent = child.render(force_inline)
                    if len(lastParagraph) > 0:
                        contents.append(lastParagraph)
                        lastParagraph = list()
                    contents.append(childContent)
            if len(lastParagraph) > 0:
                contents.append(lastParagraph)
            return contents
        else:
            # handle inline elements
            contents = list()
            for child in self.children:
                if isinstance(child, Text):
                    contents.append(child)
                else:
                    childContent = child.render(force_inline = True)
                    contents += childContent
            return contents

