import re
from colorama import Fore, Style

# positive_numbers = 0123456789
# negative_numbers = 123456789

# Nova expressão regular
regex = r'''\[
    (
        # (-?\d+|(-\d+):(-\d+)|(\d):())  # Grupo para números
        (-([1-9]\d+):-([1-9]\d+)|([0-9]]\d+):([0-9]\d+))|(-?\d+)

    )
    |
    (
        (\'[^\']*\'|"[^"]*") #|     # Grupo para strings
        # (\'[^\']*:\'[^\']*\')|     # Slice de strings entre aspas simples
        # ("[^"]*:"[^"]*")          # Slice de strings entre aspas duplas
    )
\]'''

# Lista de casos de teste como objetos
test_cases = [
    {"input": 'x[0]', "should_accept": True},
    {"input": 'x[-1]', "should_accept": True},
    {"input": 'x[0:5]', "should_accept": True},
    {"input": 'x["column1"]', "should_accept": True},
    {"input": "x['column2']", "should_accept": True},
    {"input": 'x["val1":"val2"]', "should_accept": False},
    {"input": "x['val3':'val4']", "should_accept": False},
    {"input": 'x[-2:-1]', "should_accept": True},
    {"input": 'x[1:]', "should_accept": False},
    {"input": 'x[1:-1]', "should_accept": True},
    {"input": 'x["abc":0]', "should_accept": False},
    {"input": 'x[0:"abc"]', "should_accept": False},
    {"input": 'x["val1":1]', "should_accept": False},
    {"input": 'x[1:3]', "should_accept": True},
    {"input": 'x[-1:-3]', "should_accept": True},
    {"input": 'x[-1:0]', "should_accept": True},
    {"input": 'x["string1":"string2"]', "should_accept": False},
    {"input": 'x[0:5.5]', "should_accept": False},
    {"input": 'x[]', "should_accept": False},
    {"input": 'x[:"end"]', "should_accept": False},
    {"input": "x['end':'start']", "should_accept": False},
]

Trues = []
Falses = []
# Função para verificar e imprimir resultados
for test in test_cases:
    match = re.search(regex, test["input"], re.VERBOSE)
    is_valid = match is not None
    should_accept = test["should_accept"]

    if is_valid == should_accept:
        print(f"{Fore.GREEN}Entrada: {test['input']} -> Capturado: {match.group(0) if match else 'Nenhum'} (Válido){Style.RESET_ALL}")
        Trues.append(test["input"])
    else:
        print(f"{Fore.RED}Entrada: {test['input']} -> Não capturado (Inválido){Style.RESET_ALL}")
        Falses.append(test['input'])

print(f'Válidos: {Fore.GREEN}{len(Trues)}{Style.RESET_ALL}')
print(f'Não válidos: {Fore.RED}{len(Falses)}{Style.RESET_ALL}')