import re

# Função para traduzir expressões aritméticas
def traduzir_expressao(expr):
    # Substitui a exponenciação em Python (**) por `^` em Shell Script
    expr = expr.replace("**", "^")
    # Outras operações podem ser diretamente passadas, já que são compatíveis com Bash
    return expr

# Função para traduzir o código Python para Shell Script (Bash)
def transpilar(codigo_python):
    codigo_shell = []
    linhas = codigo_python.splitlines()

    for linha in linhas:
        linha = linha.strip()

        # Tradução de declaração de variáveis
        if re.match(r'^\w+ = .+', linha):  # Detecta atribuições como 'variavel = valor'
            var, valor = linha.split("=", 1)
            var = var.strip()
            valor = traduzir_expressao(valor.strip())
            codigo_shell.append(f"{var}={valor}")

        # Condicional 'if' e 'else'
        elif linha.startswith("if"):
            condicao = re.match(r'if (.*):', linha)
            if condicao:
                codigo_shell.append(f"if [ {condicao.group(1)} ]; then")
        
        elif linha.startswith("elif"):
            condicao = re.match(r'elif (.*):', linha)
            if condicao:
                codigo_shell.append(f"elif [ {condicao.group(1)} ]; then")
        
        elif linha.startswith("else"):
            codigo_shell.append("else")
        
        elif linha == "end":
            codigo_shell.append("fi")

        # Comandos 'for' e 'while' para laços de repetição
        elif linha.startswith("for"):
            match = re.match(r'for (\w+) in (.*):', linha)
            if match:
                variavel = match.group(1)
                iteravel = match.group(2)
                codigo_shell.append(f"for {variavel} in {iteravel}; do")

        elif linha.startswith("while"):
            match = re.match(r'while (.*):', linha)
            if match:
                condicao = match.group(1)
                codigo_shell.append(f"while [ {condicao} ]; do")
        
        # Fechamento dos loops 'for' e 'while'
        elif linha == "end":
            codigo_shell.append("done")

        # Função 'def' em Python
        elif linha.startswith("def"):
            match = re.match(r'def (\w+)\((.*)\):', linha)
            if match:
                nome_funcao = match.group(1)
                parametros = match.group(2).split(",")
                parametros = [p.strip() for p in parametros]
                codigo_shell.append(f"{nome_funcao}() {{")
        
        # Comando de retorno 'return' em Python
        elif linha.startswith("return"):
            comando = linha.replace("return", "").strip()
            codigo_shell.append(f"return {comando}")

        # Função chamada (exemplo: 'funcao(3, 4)')
        elif re.match(r'\w+\(.*\)', linha):
            codigo_shell.append(f"{linha}")

        # Expansões para `and`, `or`, `not` e expressões lógicas
        linha = linha.replace("and", "-a")
        linha = linha.replace("or", "-o")
        linha = linha.replace("not", "!")
        codigo_shell.append(linha)

    return "\n".join(codigo_shell)

# Função principal para ler o arquivo Python e gerar o arquivo Shell Script
def gerar_shell(codigo_python, arquivo_saida):
    codigo_shell = transpilar(codigo_python)
    with open(arquivo_saida, 'w') as f:
        f.write(codigo_shell)

# Exemplo de uso
if __name__ == "__main__":
    # Leitura do arquivo Python
    with open("ex.py", "r") as f:
        codigo_python = f.read()

    # Gera o código Shell Script
    gerar_shell(codigo_python, "out.sh")
