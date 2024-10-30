import re

# Definindo a expressão regular no formato regex
regex_pattern = r"\s*(?:(-?\d+|'[^']'|\"[^\"]\")(?::(-?\d+|'[^']'|\"[^\"]\"))?)\s*"

# Compilando a expressão regular
pattern = re.compile(regex_pattern)

# Testando a expressão com exemplos
testes = [
    "[123]",
    "[-456]",
    "['string']",
    '["another string"]',
    "[123:'456']",
    "[ 'text' : \"other text\" ]",
    "[ -789 : 42 ]",
    "[invalido]"
]

for teste in testes:
    if pattern.fullmatch(teste):
        print(f"{teste} é um índice válido.")
    else:
        print(f"{teste} não é um índice válido.")