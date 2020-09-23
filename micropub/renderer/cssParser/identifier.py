import re
class Identifier:
    def __init__(self, identifier):
        if identifier == "*":
            self.all = True
        else:
            self.all = False
            self.classes = list([x.strip(".") for x in re.findall(r"\.[^.\[\]\s\:]+", identifier)])
            self.element = re.findall(r"(?<!.)[^\s\.\[\]\:]+", identifier)

    def validate(self, tag):
        if self.all:
            return True
        return (tag.get("class") in self.classes or len(self.classes) == 0) and (tag.name in self.element or len(self.element) == 0)


