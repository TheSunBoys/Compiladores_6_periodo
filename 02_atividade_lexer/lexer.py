import re
import inspect
from colorama import Fore

def tokenize(input_string):
    """
    Tokeniza a entrada de forma a tratar números, strings e aspas como um único token.
    """
    token_regex = r'v|\[|\]|"|:|p|n|s'
    return re.findall(token_regex, input_string)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def log(self, message):
        """Loga mensagens com o nome do método atual."""
        current_method = inspect.currentframe().f_back.f_code.co_name
        print(f"{Fore.BLUE}{current_method}{Fore.RESET}: {message}")

    def match(self, expected):
        """Verifica se o token atual é o esperado e avança."""
        if self.current < len(self.tokens) and self.tokens[self.current] == expected:
            self.log(f"Consumiu token: '{expected}'")
            self.current += 1
            return True
        return False

    def S(self):
        """Regra para S -> v [ I ]"""
        if self.match('v'):
            self.log("Reconheceu uma variável (v)")
            if self.match('['):
                if self.I():
                    if self.match(']'):
                        self.log("Reconheceu S -> v [ I ]")
                        return True
        self.log("Falha em S")
        return False

    def I(self):
        """Regra para I -> p | n | s | I : I | v [ I ] | ε"""
        start = self.current  # Salva o estado atual para backtracking

        # Verifica p ou n
        if self.match('p') or self.match('n'):
            self.log("Reconheceu um número")
            return True

        # Verifica s (string)
        elif self.match('s'):
            self.log("Reconheceu uma string")
            return True

        # Verifica v [ I ]
        elif self.match('v'):
            self.log("Reconheceu outra variável (v)")
            if self.match('['):
                if self.I():
                    if self.match(']'):
                        self.log("Reconheceu I -> v [ I ]")
                        return True
            self.current = start  # Backtrack caso falhe

        # Verifica I : I (slice)
        elif self.I():
            if self.match(':'):
                if self.I():
                    self.log("Reconheceu um slice (I : I)")
                    return True
            self.current = start  # Backtrack caso falhe

        # ε (vazio)
        self.log("Reconheceu expressão vazia (ε)")
        return True

    def parse(self):
        """Inicia a análise sintática."""
        if self.S() and self.current == len(self.tokens):
            return f"{Fore.GREEN}Aceito{Fore.RESET}"
        return f"{Fore.RED}Rejeitado{Fore.RESET}"

if __name__ == "__main__":
    # Exemplos de entrada
    tokens_list = [
        'v[v[p:p]]',  # Aninhado
        'v[p:s]',  # Simples
        'v[:]',  # Slice vazio
        'v[v["s"]]',  # Variável aninhada com string
    ]

    for token in tokens_list:
        print(f"Entrada: {token}")
        tokens = tokenize(token)  # Gera a lista de tokens
        print(f"Tokens: {tokens}")

        parser = Parser(tokens)
        print(f"Resultado: {parser.parse()}")
        print("-" * 40)
