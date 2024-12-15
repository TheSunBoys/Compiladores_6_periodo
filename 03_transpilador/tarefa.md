Nome da Tarefa:
Trabalho final - Transpilador - 3ª Unidade
Descrição:

Implementar um transpilador, que converte um programa fonte em uma linguagem de programação para outra linguagem de programação.

O transpilador pode ser feito usando uma abordagem descendente, com um analisador descendente recursivo, ou ascendente usando geradores de analisadores léxico/sintático, como o Flex/Bison e similares

Entregar um documento com a descrição do trabalho, o link para o repositório com o código fonte e as instruções para executá-lo. Na descrição do trabalho deve haver:

    A linguagem de origem (ex: Python);
    A linguagem de destino (ex: Javascript);
    Justificativa - por que o trabalho é preciso/importante (ex: converter programas para uma linguagem suportada por navegadores para web apps);
    Tokens suportados pela análise léxica, incluindo os literais dos tipos de dados suportados e palavras reservadas (ex: tipos inteiros decimais positivos e negativos, strings com aspas duplas, if, for, parênteses...);
    Gramática utilizada no reconhecimento dos comandos.

O transpilador deve suportar os seguintes comandos, pelo menos:

    Declaração/atribuição de valores a variáveis;
    Expressões aritméticas com os 4 operações;
    Um comando condicional (if/else, switch/case);
    Um comando de repetição (for, while, do while, repeat until);
    Expressões lógicas com E e OU;
    Declaração e chamada de função com parâmetros posicionais.

A divisão dos pontos será feita da seguinte maneira:

    Documentação (com justificativa, tokens e gramática definida): 2,0
    Análise léxica: 3,0
    Análise sintática: 4,0
    Geração de código para linguagem alvo: 3,0