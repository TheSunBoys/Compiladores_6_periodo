import re
import inspect
from colorama import Fore
import os

def transform_to_program_format(user_input):
    """
    Transforma a entrada do usuário no formato de programa para verificação.
    Regras:
    - Variáveis são transformadas em 'v'.
    - Strings (entre aspas simples ou duplas) são transformadas em 's'.
    - Números positivos ou zero são transformados em 'p', exceto se seguidos de colchetes, quando são tratados como 'v'.
    - Números negativos são transformados em 'n', exceto se seguidos de colchetes, quando são tratados como 'v'.
    """
    # Regex para identificar os elementos na entrada
    token_regex = r'[a-zA-Z_]\w*|".*?"|\'.*?\'|[-]?\d+|[\[\]:]'
    tokens = re.findall(token_regex, user_input)

    result = []
    first_bracket_found = False  # Para adicionar "v" apenas antes do primeiro '['

    for i, token in enumerate(tokens):
        if token == '[' and not first_bracket_found:
            result.append('v')  # Adiciona 'v' antes do primeiro '['
            first_bracket_found = True

        if re.match(r'[a-zA-Z_]\w*', token):  # Identifica variáveis
            result.append('v')
        elif re.match(r'".*?"|\'.*?\'', token):  # Identifica strings
            result.append('s')
        elif re.match(r'[-]?\d+', token):  # Identifica números
            # Verifica se o número é seguido por colchetes -> trata como variável
            if i + 1 < len(tokens) and tokens[i + 1] == '[':
                result.append('v')
            else:
                result.append('n' if int(token) < 0 else 'p')
        elif token in ['[', ']', ':']:  # Mantém os delimitadores
            result.append(token)
        else:
            raise ValueError(f"Token inválido na entrada: {token}")

    print(f'{Fore.CYAN}{user_input}{Fore.RESET} -> {Fore.GREEN}{''.join(result)}{Fore.RESET}')
    return ''.join(result)

def tokenize(input_string):
    """
    Tokeniza a entrada de forma a tratar números, strings e aspas como um único token.
    """
    token_regex = r'v|\[|\]|"|:|p|n|s'
    return re.findall(token_regex, input_string)

class Parser:
    def __init__(self, tokens, only_results=False):
        self.tokens = tokens
        self.current = 0
        if only_results:
            self.only_results = True

    def log(self, message):
        """Loga mensagens com o nome do método atual."""
        current_method = inspect.currentframe().f_back.f_code.co_name
        if not self.only_results:
            print(f"{Fore.BLUE}{current_method}{Fore.RESET}: {message}")
            file.write(f"{current_method}: {message}\n")

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
                index_type = self.I()
                if index_type and self.match(']'):
                    self.log("Reconheceu S -> v [ I ]")
                    return True
        self.log("Falha em S")
        return False

    def I(self):
        """
        Regra para I:
        I -> I_simple_or_empty ':' I_simple_or_empty
           | I_simple
           | v [ I ]
        Retorna o tipo do índice.
        """
        start = self.current  # Salva o estado atual para backtracking

        # Tenta casar um slice: I_simple_or_empty ':' I_simple_or_empty
        index_type1 = self.I_simple_or_empty()
        if index_type1 is not None or True:
            if self.match(':'):
                index_type2 = self.I_simple_or_empty()
                if index_type2 is not None or True:
                    # Verifica se os tipos dos índices correspondem
                    if (index_type1 == index_type2) or (index_type1 is None) or (index_type2 is None):
                        self.log("Reconheceu um slice (I : I)")
                        return 'slice'
                    else:
                        self.log("Tipos dos índices do slice não correspondem")
                        self.current = start  # Backtrack
                        return None
                else:
                    self.log("Falha ao reconhecer a segunda parte do slice")
                    self.current = start  # Backtrack
                    return None
            else:
                # Se não houver ':', reset e tenta outras opções
                self.current = start

        # Tenta casar um índice simples
        index_type = self.I_simple()
        if index_type:
            return index_type

        # Tenta casar uma variável aninhada
        if self.match('v'):
            if self.match('['):
                index_type = self.I()
                if index_type and self.match(']'):
                    self.log("Reconheceu I -> v [ I ]")
                    return 'variable'
            self.current = start  # Backtrack

        self.log("Falha em I")
        return None

    def I_simple_or_empty(self):
        """
        Regra para I_simple_or_empty:
        I_simple_or_empty -> I_simple | ε
        Retorna o tipo do índice ou None se vazio.
        """
        start = self.current

        index_type = self.I_simple()
        if index_type:
            return index_type

        # Caso vazio (ε)
        self.log("Reconheceu índice vazio (ε)")
        return None

    def I_simple(self):
        """
        Regra para I_simple:
        I_simple -> p | n | s | v [ I ]
        Retorna o tipo do índice.
        """
        start = self.current

        if self.match('p'):
            self.log("Reconheceu índice simples (número positivo)")
            return 'positive'

        if self.match('n'):
            self.log("Reconheceu índice simples (número negativo)")
            return 'negative'

        if self.match('s'):
            self.log("Reconheceu índice simples (string)")
            return 'string'

        if self.match('v'):
            if self.match('['):
                index_type = self.I()
                if index_type and self.match(']'):
                    self.log("Reconheceu I_simple -> v [ I ]")
                    return 'variable'
            self.current = start  # Backtrack

        self.log("Falha em I_simple")
        return None

    def parse(self):
        """Inicia a análise sintática."""
        if self.S() and self.current == len(self.tokens):
            return True
        return False

if __name__ == "__main__":
    # Exemplos de entrada
    tokens_list = [
        'v[p]',                   # Aceitar
        'v[n]',                   # Aceitar
        'v[s]',                   # Aceitar
        'v[p:p]',                 # Aceitar
        'v[s:s]',                 # Aceitar
        'v[n:n]',                 # Aceitar
        'v[:]',                   # Aceitar
        'v[p:]',                  # Aceitar
        'v[:p]',                  # Aceitar
        'v[v[p:n]]',              # Rejeitar (tipos diferentes)
        'v[v[p:p]]',              # Aceitar
        'v[v[n:n]]',              # Aceitar
        'v[v[v[v[v[n:n]]]]]',     # Aceitar
        'v[v[v[v[v[p:p]]]]]',     # Aceitar
        'v[v[v[v[v[s:s]]]]]',     # Aceitar
        'v[v[v[v[v[n:p]]]]]',     # Rejeitar (tipos diferentes)
        'v[v[v[v[v[s:n]]]]]',     # Rejeitar (tipos diferentes)
        'v[v[s:s]]',              # Aceitar
        'v[v[:]]',                # Aceitar
        'v[:s]',                  # Aceitar
        'v[s:]',                  # Aceitar
        'v[p:s]',                 # Rejeitar (tipos diferentes)
        'v[:]',                   # Aceitar
        transform_to_program_format('[8:9]'),
        transform_to_program_format('[a["a":"b"]]'),
        transform_to_program_format('[8:]'),
        transform_to_program_format('[:]'),
        transform_to_program_format('["a":9]'),
        transform_to_program_format('[-1:9]'),
        transform_to_program_format('[vba[8:9]]'),
    ]

    # criando novamente o arquivo de log e usando 'a+' pra poder escrever no arquivo novas linhas
    if os.path.exists('./log.txt'):
        os.remove('./log.txt')
    file = open('./log.txt', 'a+')

    for token in tokens_list:
        print(f"{Fore.GREEN}Entrada{Fore.RESET}: \033[1m{Fore.YELLOW}{token}{Fore.RESET}\033[0m")
        file.write(f"Entrada: {token}\n")
        tokens = tokenize(token)  # Gera a lista de tokens
        print(f'Quantidade de caracteres: {Fore.LIGHTMAGENTA_EX}{len(tokens)}{Fore.RESET}')
        file.write(f'Quantidade de caracteres: {len(tokens)}\n')
        formatted_tokens = ', '.join([f"\033[1m{Fore.MAGENTA}{t}{Fore.RESET}\033[0m" for t in tokens])
        print(f"Tokens: {formatted_tokens}")
        file.write(f"Tokens: {tokens}\n")

        parser = Parser(tokens, only_results=True)
        result = parser.parse()
        if result is True:
            print(f"Resultado: {Fore.GREEN}Aceito{Fore.RESET}")
            file.write(f"{token} - Aceito\n")
        else:
            print(f"Resultado: {Fore.RED}Rejeitado{Fore.RESET}")
            file.write(f"{token} - Rejeitado\n")

        print("-" * 40)
        file.write('\n\n')
    file.close()