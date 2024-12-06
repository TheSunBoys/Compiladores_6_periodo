import ast

class PythonToBendTranspiler:
    def __init__(self):
        self.output = []

    def transpile(self, python_code):
        """
        Transpila o código Python para Bend.

        Args:
        python_code (str): O código Python a ser transpilado.

        Returns:
        str: O código gerado em Bend.
        """
        # Parse o código Python para a árvore AST
        tree = ast.parse(python_code)
        self.output.clear()  # Limpa o buffer de saída
        self.visit(tree)
        return ''.join(self.output)  # Junta as partes do código final

    def visit(self, node):
        """
        Visita os nós da árvore AST, chamando o método específico para cada tipo de nó.

        Args:
        node (ast.AST): O nó da árvore a ser visitado.
        
        Returns:
        str: O código gerado correspondente ao nó.
        """
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Método para nós não específicos"""
        for child_node in ast.iter_child_nodes(node):
            self.visit(child_node)

    def visit_Assign(self, node):
        """Converte uma atribuição de variável"""
        target = node.targets[0]
        value = self.visit_expr(node.value)
        self.output.append(f"{target.id} = {value}\n")

    def visit_Expr(self, node):
        """Converte expressões simples"""
        self.output.append(f"{self.visit_expr(node.value)}\n")

    def visit_If(self, node):
        """Converte estruturas if/else"""
        self.output.append(f"if {self.visit_expr(node.test)}:\n")
        self.visit(node.body)
        if node.orelse:
            self.output.append("else:\n")
            self.visit(node.orelse)

    def visit_While(self, node):
        """Converte loops while"""
        self.output.append(f"while {self.visit_expr(node.test)}:\n")
        self.visit(node.body)

    def visit_For(self, node):
        """Converte loops for"""
        target = node.target
        iter_expr = self.visit_expr(node.iter)
        self.output.append(f"for {target.id} in {iter_expr}:\n")
        self.visit(node.body)

    def visit_FunctionDef(self, node):
        """Converte funções"""
        args = ', '.join([arg.arg for arg in node.args.args])
        self.output.append(f"def {node.name}({args}):\n")
        self.visit(node.body)

    def visit_Return(self, node):
        """Converte a declaração de retorno"""
        self.output.append(f"return {self.visit_expr(node.value)}\n")

    def visit_Constant(self, node):
        """Converte constantes (inteiros, strings, etc.)"""
        if isinstance(node.value, str):
            return f'"{node.value}"'  # Aspas para strings
        elif isinstance(node.value, bool):
            return "true" if node.value else "false"
        elif node.value is None:
            return "null"  # Para tipos nulos em Bend
        else:
            return str(node.value)

    def visit_Name(self, node):
        """Converte nomes de variáveis"""
        return node.id

    def visit_BinOp(self, node):
        """Converte operações binárias (como +, -, *, etc.)"""
        left = self.visit_expr(node.left)
        right = self.visit_expr(node.right)
        op = self.visit(node.op)
        return f"({left} {op} {right})"

    def visit_Add(self, node):
        """Converte operador de adição"""
        return "+"

    def visit_Sub(self, node):
        """Converte operador de subtração"""
        return "-"

    def visit_Mult(self, node):
        """Converte operador de multiplicação"""
        return "*"

    def visit_Div(self, node):
        """Converte operador de divisão"""
        return "/"

    def visit_Mod(self, node):
        """Converte operador de módulo"""
        return "%"

    def visit_FloorDiv(self, node):
        """Converte operador de divisão inteira"""
        return "//"

    def visit_Eq(self, node):
        """Converte operador de igualdade"""
        return "=="

    def visit_NotEq(self, node):
        """Converte operador de desigualdade"""
        return "!="

    def visit_Lt(self, node):
        """Converte operador de menor que"""
        return "<"

    def visit_LtE(self, node):
        """Converte operador de menor ou igual"""
        return "<="

    def visit_Gt(self, node):
        """Converte operador de maior que"""
        return ">"

    def visit_GtE(self, node):
        """Converte operador de maior ou igual"""
        return ">="

    def visit_And(self, node):
        """Converte operador lógico AND"""
        return "and"

    def visit_Or(self, node):
        """Converte operador lógico OR"""
        return "or"

    def visit_Not(self, node):
        """Converte operador lógico NOT"""
        return "not"

    def visit_List(self, node):
        """Converte listas"""
        elements = [self.visit_expr(e) for e in node.elts]
        return f"[{', '.join(elements)}]"

    def visit_Dict(self, node):
        """Converte dicionários"""
        items = [f"{self.visit_expr(k)}: {self.visit_expr(v)}" for k, v in zip(node.keys, node.values)]
        return f"{{{', '.join(items)}}}"

    def visit_Tuple(self, node):
        """Converte tuplas"""
        elements = [self.visit_expr(e) for e in node.elts]
        return f"({', '.join(elements)})"

    def visit_Set(self, node):
        """Converte conjuntos"""
        elements = [self.visit_expr(e) for e in node.elts]
        return f"{{{', '.join(elements)}}}"

    def visit_ClassDef(self, node):
        """Converte definições de classe"""
        self.output.append(f"class {node.name}:\n")
        for stmt in node.body:
            self.visit(stmt)

    def visit_Attribute(self, node):
        """Converte atributos de classe/objeto"""
        return f"{self.visit_expr(node.value)}.{node.attr}"

    def visit_expr(self, expr):
        """Método auxiliar para avaliar expressões"""
        if isinstance(expr, ast.Constant):
            return self.visit_Constant(expr)
        elif isinstance(expr, ast.Name):
            return self.visit_Name(expr)
        elif isinstance(expr, ast.BinOp):
            return self.visit_BinOp(expr)
        elif isinstance(expr, ast.Call):
            return self.visit_Call(expr)
        elif isinstance(expr, ast.List):
            return self.visit_List(expr)
        elif isinstance(expr, ast.Dict):
            return self.visit_Dict(expr)
        elif isinstance(expr, ast.Tuple):
            return self.visit_Tuple(expr)
        elif isinstance(expr, ast.Set):
            return self.visit_Set(expr)
        elif isinstance(expr, ast.Attribute):
            return self.visit_Attribute(expr)
        else:
            return ""

# Exemplo de uso do transpilador com desempenho melhorado
python_code = """
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def saudacao(self):
        return f"Olá, meu nome é {self.nome} e tenho {self.idade} anos."

p1 = Pessoa("João", 30)
p2 = Pessoa("Maria", 25)

tupla = (1, 2, 3)
conjunto = {1, 2, 3}
"""

transpiler = PythonToBendTranspiler()
bend_code = transpiler.transpile(python_code)
print("Código Bend gerado:\n", bend_code)

