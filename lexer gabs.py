import re
from colorama import Fore, Style

# Expressão regular corrigida para validar os casos
regex = r'''\[
    (-?\d+|\'[^\']*\'|"[^"]*"|(-?\d+)
    :(-?\d+)|\'[^\']*:\'[^\']*\'|"[^"]*:"[^"]*")
\]'''

regex = r'\[(\d+):(\d+)]'

# Lista de casos de teste como objetos
test_cases = [
    {"input": 'x[0]', "should_accept": True},
    {"input": 'x[-1]', "should_accept": True},
    {"input": 'x[0:5]', "should_accept": True},
    {"input": 'x["column1"]', "should_accept": True},
    {"input": "x['column2']", "should_accept": True},
    {"input": 'x["val1":"val2"]', "should_accept": False},  # Inválido
    {"input": "x['val3':'val4']", "should_accept": False},  # Inválido
    {"input": 'x[-2:-1]', "should_accept": True},
    {"input": 'x[1:]', "should_accept": False},  # Inválido: falta o limite superior
    {"input": 'x[1:-1]', "should_accept": True},  # Válido
    {"input": 'x["abc":0]', "should_accept": False},  # Inválido: mistura de tipos
    {"input": 'x[0:"abc"]', "should_accept": False},  # Inválido: mistura de tipos
    {"input": 'x["val1":1]', "should_accept": False},  # Inválido: mistura de tipos
    {"input": 'x[1:3]', "should_accept": True},
    {"input": 'x[-1:-3]', "should_accept": True},
    {"input": 'x[-1:0]', "should_accept": True},
    {"input": 'x["string1":"string2"]', "should_accept": False},  # Inválido
    {"input": 'x[0:5.5]', "should_accept": False},  # Inválido: float não aceito
    {"input": 'x[]', "should_accept": False},  # Inválido: índice vazio
    {"input": 'x[:"end"]', "should_accept": False},  # Inválido: índice vazio
    {"input": '''x['end':"start"]''', "should_accept": False},  # Inválido
]

Falses = []
Trues = []

# Função para verificar e imprimir resultados
for test in test_cases:
    match = re.search(regex, test["input"])
    is_valid = match is not None
    should_accept = test["should_accept"]

    # Adicionando verificação para misturar tipos em slices
    if is_valid and (':' in test['input']):
        parts = test['input'][test['input'].index('[') + 1:test['input'].index(']')].split(':')
        if len(parts) == 2:
            left, right = parts
            if (left and right) and (left.isdigit() or right.isdigit()):
                # Verifica se um lado é um número e o outro não
                if (left.isdigit() and not right.isdigit()) or (not left.isdigit() and right.isdigit()):
                    is_valid = False

    if is_valid == should_accept:
        print(f"{Fore.GREEN}Entrada: {test['input']} -> Capturado: {match.group(1) if match else 'Nenhum'} (Válido){Style.RESET_ALL}")
        if should_accept:
            Trues.append(test)
    else:
        print(f"{Fore.RED}Entrada: {test['input']} -> Não capturado (Inválido){Style.RESET_ALL}")
        Falses.append(test)

print(f'Válidos: {Fore.GREEN}{len(Trues)}{Style.RESET_ALL}')
print(f'Não válidos: {Fore.RED}{len(Falses)}{Style.RESET_ALL}')
