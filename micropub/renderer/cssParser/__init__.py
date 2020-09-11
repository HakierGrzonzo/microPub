import cssutils 
class Parser:
    def __init__(self, raw, href = None):
        self.stylesheet = cssutils.parseString(raw, validate=False, href=href)
        for rule in self.stylesheet.cssRules:
            if isinstance(rule, cssutils.css.CSSStyleRule):
                for selector in rule.selectorList:
                    print(selector.selectorText)
        print("\n-----\n")

