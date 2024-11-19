class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def match(self, expected):
        if self.current < len(self.tokens) and self.tokens[self.current] == expected:
            self.current += 1
            return True
        return False

    def S(self):
        if self.match('v'):
            if self.match('['):
                if self.I():
                    if self.match(']'):
                        return True
        return False

    def I(self):
        if self.match('p') or self.match('n') or self.match('s'):
            return True
        elif self.match('v'):
            if self.match('['):
                if self.I():
                    if self.match(']'):
                        return True
        elif self.I_prime():
            return True
        return False

    def I_prime(self):
        if self.I():
            if self.match(':'):
                if self.I():
                    return True
        # epsilon
        return True

    def parse(self):
        if self.S() and self.current == len(self.tokens):
            return "Aceito"
        return "Rejeitado"

if __name__ == "__main__":
    token = 'v["p":"s"]'
    tokens = list(token)
    print(tokens) # ['v', '[', '"', 'p', '"', ':', '"', 's', '"', ']']

    parser = Parser(token)

    # print(parser.parse())  # Aceito