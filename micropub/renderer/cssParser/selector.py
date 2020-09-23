import re
from micropub.renderer.cssParser.identifier import Identifier
class Selector:
    def __init__(self, selectorText, rule, validRules = None):
        if validRules is not None:
            success = False
            for key in rule.keys():
                if key in validRules:
                    success = True
                    break
            if not success:
                raise Exception("no valid rules")
        self.rule = rule
        if "+" in selectorText:
            self.mode = "previous"
            self.identifiers = list([Identifier(x.strip()) for x in selectorText.split("+")])
            if len(self.identifiers) != 2:
                raise Exception("Css syntax error")
        elif ">" in selectorText:
            self.mode = "parent"
            self.identifiers = list([Identifier(x.strip()) for x in selectorText.split(">")])
            if len(self.identifiers) != 2:
                raise Exception("Css syntax error")
        elif "~" in selectorText:
            self.mode = "after"
            self.identifiers = list([Identifier(x.strip()) for x in selectorText.split("~")])
            if len(self.identifiers) != 2:
                raise Exception("Css syntax error")
        elif " " in selectorText.strip():
            self.mode = "in"
            self.identifiers = list([Identifier(x.strip()) for x in selectorText.split(" ", 1)])
            if len(self.identifiers) != 2:
                raise Exception("Css syntax error")
        else:
            self.mode = "simple"
            self.identifiers = Identifier(selectorText.strip())

    def check(self, tag):
        if self.mode == "simple":
            return self.identifiers.validate(tag)
        elif self.mode == "previous":
            if tag.previous_sibling is not None:
                return self.identifiers[1].validate(tag) and  self.identifiers[0].validate(tag.previous_sibling)
            else:
                return False
        elif self.mode == "parent":
            if tag.parent is not None:
                return self.identifiers[1].validate(tag) and  self.identifiers[0].validate(tag.parent)
            else:
                return False
        elif self.mode == "after":
            if tag.previous_siblings is not None and self.identifiers[1].validate(tag):
                success = False
                for sibling in tag.previous_siblings:
                    if self.identifiers[0].validate(sibling):
                        success = True
                        break
                return success
            else:
                return False
        elif self.mode == "in":
            if tag.parents is not None and self.identifiers[1].validate(tag):
                success = False
                for parent in tag.parents:
                    if self.identifiers[0].validate(parent):
                        success = True
                        break
                return success
            else:
                return False
        raise Exception("weird mode?!?")

