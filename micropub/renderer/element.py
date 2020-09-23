from bs4 import BeautifulSoup as Soup
from bs4 import Tag
from micropub.renderer.text import Text

class Element:
    def __init__(self, tag, renderer, parent = None):
        self.renderer = renderer
        self.parent = parent
        self.tag = tag
        self.children = list()
        for child in tag.children:
            if isinstance(child, Tag):
                self.children.append(Element(child, renderer, self))
            else:
                self.children.append(Text(child, self))

    def debug(self):
        res = {
            "name" : "{}.{}".format(self.tag.name, self.tag.get("class", str())),
            "styles" : list(),
            "children" : list()
        }
        for stylesheet in self.renderer.styles:
            rules = stylesheet.getStyle(self.tag) 
            if len(rules.keys()) > 1:
                res["styles"].append(list(["{}: {}".format(x, rules[x]) for x in rules.keys()]))
        res["children"] = list()
        for child in self.children:
            if isinstance(child, Element):
                res["children"].append(child.debug())
            else:
                res["children"].append(child.textNode)
        return res
