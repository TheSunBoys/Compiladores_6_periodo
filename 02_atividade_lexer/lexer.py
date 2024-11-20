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
        """
        Regra para I:
        I -> p | n | s | I : I | v [ I ] | ε
        """
        start = self.current  # Salva o estado atual para backtracking

        # Casos básicos: p, n ou s
        if self.match('p') or self.match('n') or self.match('s'):
            self.log("Reconheceu p, n ou s")
            return True

        # Slice (I : I)
        if self.I_simple_or_empty():
            if self.match(':'):
                if self.I_simple_or_empty():
                    self.log("Reconheceu um slice (I : I)")
                    return True
            self.current = start  # Backtrack caso falhe

        # Variável aninhada (v [ I ])
        if self.match('v'):
            if self.match('['):
                if self.I():
                    if self.match(']'):
                        self.log("Reconheceu I -> v [ I ]")
                        return True
            self.current = start  # Backtrack caso falhe

        # ε (vazio)
        self.log("Reconheceu expressão vazia (ε)")
        return True

    def I_simple_or_empty(self):
        """
        Regra auxiliar para tratar índices opcionais:
        I_simple_or_empty -> p | n | s | ε
        """
        start = self.current
        if self.match('p') or self.match('n') or self.match('s'):
            self.log("Reconheceu um índice simples (p, n ou s)")
            return True
        self.current = start  # Backtrack
        self.log("Reconheceu índice vazio (ε)")
        return True

    def parse(self):
        """Inicia a análise sintática."""
        if self.S() and self.current == len(self.tokens):
            return f"{Fore.GREEN}Aceito{Fore.RESET}"
        return f"{Fore.RED}Rejeitado{Fore.RESET}"

if __name__ == "__main__":
    # Exemplos de entrada
    tokens_list = [
        'v[p]',          # Acesso simples com número positivo
        'v[n]',          # Acesso simples com número negativo
        'v[s]',          # Acesso simples com string
        'v[p:p]',        # Slice numérico
        'v[s:s]',        # Slice string
        'v[:]',          # Slice vazio
        'v[p:]',         # Slice parcial
        'v[:p]',         # Slice parcial
        'v[v[p:n]]',     # Variável aninhada com slice
        'v[v[s:s]]',     # Variável aninhada com string
        'v[v[:]]',       # Variável aninhada com slice vazio
        'v[:s]',         # Slice parcial com string
        'v[s:]',         # Slice parcial com string
        'v[p:s]',        # Slice misto
        'v[v["s"]]',     # Variável aninhada com string
    ]

    for token in tokens_list:
        print(f"{Fore.GREEN}Entrada{Fore.RESET}: {Fore.YELLOW}{token}{Fore.RESET}")
        tokens = tokenize(token)  # Gera a lista de tokens
        print(f"Tokens: {tokens}")

        parser = Parser(tokens)
        print(f"Resultado: {parser.parse()}")
        print("-" * 40)
