import cssutils
from micropub.renderer.cssParser.selector import Selector

class Parser:
    def __init__(self, raw, href = None):
        self.stylesheet = cssutils.parseString(raw, validate=False, href=href)
        self.sheet = list()
        for rule in self.stylesheet.cssRules:
            if isinstance(rule, cssutils.css.CSSStyleRule):
                for selector in rule.selectorList:
                    try:
                        self.sheet.append(Selector(selector.selectorText, rule.style))
                    except Exception:
                        pass

    def getStyle(self, tag):
        """Return dict of styles for a given tag"""
        res = dict()
        for selector in self.sheet:
            if selector.check(tag):
                for k in selector.rule.keys():
                    res[k] = selector.rule[k]
        return res

def unitDecoder(text):
    """changes css length unit to rough approximation in char cells"""
    scale = 1
    unit_to_char_dict = {
            'em': 2,
            'ex': 1,
            'ch': 1,
            'rem': 2,
            'cm': 5,
            'mm': 0.5,
            'in': 12.7,
            'px': 0.13,
            'pt': 0.18,
            'pc': 0.014
        }
    number = ""
    unit = ""
    nums = list([str(x) for x in range(0, 10)])
    for char in text:
        if char in nums + ["."]:
            number += char
        else:
            unit += char
    number = float(number)
    try:
        return int(number * scale * unit_to_char_dict[unit])
    except KeyError:
        return 1




