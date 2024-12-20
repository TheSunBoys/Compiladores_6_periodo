# Compiladores_6_periodo

### Bibliotecas utilizadas
```shell
pip install -r requirements.txt
```

- re
- colorama (precisa baixar)
- inspect
- os

### /01_atividade_regex
implementação da atividade do regex descrita no arquivo PDF
- regex.py (arquivo da atividade)
- Trabalho teórico-prático - Análise léxica - 2ª avaliação-3.pdf (Descrição da atividade)
```shell
01_atividade_regex
├── regex.py
└── Trabalho teórico-prático - Análise léxica - 2ª avaliação-3.pdf
```

### /02_analisador_sintatico_recursivo
implementação da atividade do Analisador Sintático Descendente descrita no arquivo PDF
- sebas_recursiva.py (código que o professor utilizou em aula, usado principalmente para referência do trabalho)
- syntax_parser.py (código implementado da atividade do Analisador Sintático Descendente)
- Trabalho teórico-prático - Análise sintática ascendente - 2ª avaliação.pdf (Descrição da atividade)

! Quando rodar o código vai mostrar os resultados no terminal e no arquivo log.txt que vai ser gerado

! Para mostrar apenas os resultados sem ter os logs do código mude o parâmetro "only_results" na atribuição do parser:

```python

parser = Parser(tokens, only_results=False) # mostrar todo o log de tokens no parser
parser = Parser(tokens, only_results=True) # mostrar apenas o resultado se foi aceita ou não
```

```shell
02_analisador_sintatico_recursivo
├── sebas_recursiva.py
├── syntax_parser.py
└── Trabalho teórico-prático - Análise sintática ascendente - 2ª avaliação.pdf
```

### /03_transpilador
Linguagens: C para Python

!Enfrentamos um grande problema com formatar as tabulações do código python gerado, tirando isso está quase tudo perfeito

#### Como rodar:
depêndencias para rodar:
- bison
- flex
- make

```shell
git clone https://github.com/TheSunBoys/Compiladores_6_periodo.git
cd Compiladores_6_periodo && cd 03_transpilador
make clean && make
./transpiler ex.c
```

Arquivos da tarefa:
- o tarefa é para se orientar sobre a tarefa pedida
- lexer e parser para o transpilador
- makefile e main.c para auxiliar no uso dos lexer e parser integrando com debugs
- ex.c é um código de exemplo pra testar o transpilador, ele contém a sintaxe suportada pelo transpilador

```shell
├── ex.c
├── lexer.l
├── main.c
├── Makefile
├── parser.y
└── tarefa.md
```
