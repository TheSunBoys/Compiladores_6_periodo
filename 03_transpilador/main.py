import re

# Definindo os padrões para tokens
tokens = [
    ('NUMBER', r'\d+(\.\d*)?'),      # Número inteiro ou flutuante
    ('STRING', r'\".*?\"'),           # String entre aspas
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identificadores (variáveis, funções)
    ('ASSIGN', r'='),                 # Operador de atribuição
    ('PLUS', r'\+'),                  # Operador de adição
    ('MINUS', r'-'),                  # Operador de subtração
    ('TIMES', r'\*'),                 # Operador de multiplicação
    ('DIVIDE', r'/'),                 # Operador de divisão
    ('EQUAL', r'=='),                 # Operador de comparação igual
    ('NEQUAL', r'!='),                # Operador de comparação desigual
    ('AND', r'and'),                  # Operador lógico AND
    ('OR', r'or'),                    # Operador lógico OR
    ('IF', r'if'),                    # Palavra-chave if
    ('ELSE', r'else'),                # Palavra-chave else
    ('FOR', r'for'),                  # Palavra-chave for
    ('WHILE', r'while'),              # Palavra-chave while
    ('DEF', r'def'),                  # Palavra-chave def (funções)
    ('RETURN', r'return'),            # Palavra-chave return
    ('LPAREN', r'\('),                # Parênteses de abertura
    ('RPAREN', r'\)'),                # Parênteses de fechamento
    ('LBRACE', r'{'),                 # Chaves de abertura
    ('RBRACE', r'}'),                 # Chaves de fechamento
    ('NEWLINE', r'\n'),               # Nova linha
    ('SKIP', r'[ \t]+'),              # Espaços e tabulação (ignorar)
    ('MISMATCH', r'.'),               # Qualquer coisa que não seja reconhecida (erro)
]

# Função para tokenizar o código Python
def tokenize(code):
    tokens_list = []
    
    while code:
        match = None
        for token in tokens:
            regex, pattern = token
            regex_match = re.match(pattern, code)
            if regex_match:
                if regex != 'SKIP':  # Ignorar espaços em branco e tabulação
                    value = regex_match.group(0)
                    tokens_list.append((regex, value))
                code = code[regex_match.end():]  # Avançar para a próxima parte do código
                match = True
                break  # Encerra o loop quando um token válido é encontrado
        
        if not match:
            print(f"Token não reconhecido: {code[0]}")
            raise SyntaxError(f"Illegal character '{code[0]}' at line 1")
    
    return tokens_list

# Função para analisar expressões
def parse_expression(tokens):
    # Implementando a análise de expressões simples
    if tokens:
        token = tokens.pop(0)
        if token[0] in ['NUMBER', 'ID']:
            return ('EXPRESSION', token[1])
    return None

# Função para analisar atribuições
def parse_assignment(tokens):
    if tokens and tokens[0][0] == 'ID':  # Verifica se há tokens e se é um identificador
        var_name = tokens.pop(0)[1]
        if tokens and tokens[0][0] == 'ASSIGN':
            tokens.pop(0)  # Remove o '='
            expression = parse_expression(tokens)
            return ('ASSIGN', var_name, expression)
    return None

# Função para analisar declarações 'def' (funções)
def parse_function(tokens):
    if tokens and tokens[0][0] == 'DEF':  # Verifica a palavra-chave 'def'
        tokens.pop(0)  # Remove o 'def'
        if tokens and tokens[0][0] == 'ID':  # Nome da função
            func_name = tokens.pop(0)[1]
            if tokens and tokens[0][0] == 'LPAREN':  # Parênteses de abertura
                tokens.pop(0)  # Remove '('
                params = []
                while tokens and tokens[0][0] == 'ID':  # Parâmetros da função
                    params.append(tokens.pop(0)[1])
                if tokens and tokens[0][0] == 'RPAREN':  # Parênteses de fechamento
                    tokens.pop(0)  # Remove ')'
                    return ('FUNC_DEF', func_name, params)
    return None

# Função para analisar o código em busca de expressões e atribuições
def parse(tokens):
    ast = []
    
    while tokens:
        # Ignorar tokens NEWLINE
        if tokens[0][0] == 'NEWLINE':
            tokens.pop(0)
            continue
        
        statement = None
        
        # Verificando a existência de uma atribuição
        statement = parse_assignment(tokens)
        if statement:
            ast.append(statement)
            continue  # Se encontrou uma atribuição, continua com o próximo token
        
        # Verificando a existência de uma definição de função
        statement = parse_function(tokens)
        if statement:
            ast.append(statement)
            continue  # Se encontrou uma função, continua com o próximo token
        
        # Se não encontrou nada válido, lança um erro
        raise SyntaxError(f"Unexpected token: {tokens[0]}")
    
    return ast

def parse_function(tokens):
    if tokens and tokens[0][0] == 'DEF':  # Verifica a palavra-chave 'def'
        tokens.pop(0)  # Remove o 'def'
        if tokens and tokens[0][0] == 'ID':  # Nome da função
            func_name = tokens.pop(0)[1]
            if tokens and tokens[0][0] == 'LPAREN':  # Parênteses de abertura
                tokens.pop(0)  # Remove '('
                params = []
                while tokens and tokens[0][0] != 'RPAREN':  # Até encontrar ')'
                    if tokens[0][0] == 'ID':  # Parâmetros da função
                        params.append(tokens.pop(0)[1])
                    elif tokens[0][0] == 'MISMATCH':  # Ignorar ',' ou ':'
                        tokens.pop(0)
                    else:
                        raise SyntaxError(f"Unexpected token in function parameters: {tokens[0]}")
                if tokens and tokens[0][0] == 'RPAREN':  # Parênteses de fechamento
                    tokens.pop(0)  # Remove ')'
                if tokens and tokens[0][0] == 'MISMATCH':  # Ignorar ':'
                    tokens.pop(0)
                return ('FUNC_DEF', func_name, params)
    return None

def generate_bend_code(ast):
    code = ""
    for node in ast:
        if node[0] == 'ASSIGN':
            var_name = node[1]
            expression = node[2]
            code += f"set {var_name} {expression[1]};\n"
        elif node[0] == 'FUNC_DEF':
            func_name = node[1]
            params = ', '.join(node[2])
            code += f"func {func_name}({params}) {{\n}};\n"
    return code

# Função para transpilação completa
def transpile(python_code):
    tokens = tokenize(python_code)
    print("Tokens:", tokens)  # Adicionando debug para tokens
    ast = parse(tokens)
    print("AST:", ast)  # Adicionando debug para a AST
    bend_code = generate_bend_code(ast)
    return bend_code

# Exemplo de uso
if __name__ == "__main__":
    python_code = """
def my_function(a, b):
    return a + b

x = 10
y = 20
z = x + y
"""
    
    bend_code = transpile(python_code)
    print("Código Bend gerado:\n", bend_code)
