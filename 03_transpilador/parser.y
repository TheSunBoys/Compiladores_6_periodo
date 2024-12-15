%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.h"

extern int yylineno;
extern char *yytext;

extern FILE *yyin;
int yylex(void);
void yyerror(const char *msg) {
    fprintf(stderr, "Erro: %s na linha %d. Caractere problemático: '%s'\n", msg, yylineno, yytext);
}

int indent_level = 4; // Nível de indentação

void increase_indent() {
    indent_level++;
}

void decrease_indent() {
    if (indent_level > 0) indent_level--;
}

char* get_indent() {
    char *spaces = malloc((indent_level * 4) + 1); // 4 espaços por nível
    memset(spaces, ' ', indent_level * 4);
    spaces[indent_level * 4] = '\0';
    return spaces;
}

%}

%union {
    char *str; // Todas as variáveis do tipo `char*` usam essa entrada
}

%token <str> INT FLOAT VOID RETURN PRINTF FOR WHILE IF ELSE
%token <str> ABREP FECHAP ABRECH FECHACH PONTOEVIRG ATRIB MAIS MAISMAIS MENOS VEZES DIVISAO
%token <str> MENOR MAIOR MENORIGUAL MAIORIGUAL IGUAL DIFERENTE ID NUM STR FIM_LINHA MAIN VIRGULA

%type <str> PROGRAM MAIN_FUNC FUNC FUNC_DECL FUNC_CALL PARAM_LIST COMANDO_LIST COMANDO BLOCO DECLARACAO EXPRESSAO PRINT_FUNC LOOP FOR_LOOP CONDICAO INCREMENTO TYPE EXPRESSAO_LIST

%left AND OR
%left MENOR MAIOR MENORIGUAL MAIORIGUAL IGUAL DIFERENTE
%left MAIS MENOS
%left VEZES DIVISAO

%precedence ELSE
%nonassoc IFX

%%

PROGRAM:
    FUNC_DECL MAIN_FUNC
    {
        printf("[LOG] PROGRAM -> FUNC_DECL MAIN_FUNC\n");

        FILE *output = fopen("output.py", "w");
        if (!output) {
            perror("Erro ao abrir o arquivo de saída");
            exit(1);
        }

        fprintf(output, "%s\n%s\n", $1, $2);
        fclose(output);

        printf("Transpilação concluída. Código gerado em 'output.py'.\n");
    }
    ;

FUNC_DECL:
    /* vazio */
    {
        $$ = strdup("");
    }
    | FUNC_DECL FUNC
    {
        printf("[LOG] FUNC_DECL -> FUNC_DECL FUNC\n");
        $$ = malloc(strlen($1) + strlen($2) + 2);
        sprintf($$, "%s\n%s", $1, $2);
    }
    ;

FUNC:
    TYPE ID ABREP PARAM_LIST FECHAP ABRECH COMANDO_LIST FECHACH
    {
        printf("[LOG] FUNC -> TYPE ID (PARAM_LIST) { COMANDO_LIST }\n");
        $$ = malloc(strlen($2) + strlen($4) + strlen($7) + 50);
        sprintf($$, "def %s(%s):\n    %s", $2, $4, $7);
    }
    ;

TYPE:
    INT
    {
        $$ = strdup("int");
    }
    | FLOAT
    {
        $$ = strdup("float");
    }
    | VOID
    {
        $$ = strdup("void");
    }
    ;

PARAM_LIST:
    TYPE ID
    {
        printf("[LOG] PARAM_LIST -> TYPE ID\n");
        char buffer[128];
        snprintf(buffer, sizeof(buffer), "%s %s", $1, $2);
        $$ = strdup(buffer);
    }
    | PARAM_LIST VIRGULA TYPE ID
    {
        printf("[LOG] PARAM_LIST -> PARAM_LIST, TYPE ID\n");
        char buffer[256];
        snprintf(buffer, sizeof(buffer), "%s, %s %s", $1, $3, $4);
        $$ = strdup(buffer);
    }
    ;

MAIN_FUNC:
    INT MAIN ABREP FECHAP ABRECH COMANDO_LIST FECHACH
    {
        printf("[LOG] MAIN_FUNC -> INT MAIN () { COMANDO_LIST }\n");
        $$ = malloc(strlen($6) + 50);
        sprintf($$, "if __name__ == \"__main__\":\n    %s", $6);
    }
    ;

COMANDO_LIST:
    /* vazio */
    {
        $$ = strdup("");
    }
    | COMANDO_LIST COMANDO
    {
        printf("[LOG] COMANDO_LIST -> COMANDO_LIST COMANDO\n");
        char buffer[4096];
        snprintf(buffer, sizeof(buffer), "%s\n        %s", $1, $2);
        $$ = strdup(buffer);
    }
    ;

COMANDO:
    DECLARACAO
    | BLOCO
    | PRINT_FUNC
    | LOOP
    | RETURN EXPRESSAO PONTOEVIRG
    {
        printf("[LOG] COMANDO -> return EXPRESSAO;\n");
        $$ = malloc(strlen($2) + 20);
        sprintf($$, "return %s", $2);
    }
    | FUNC_CALL PONTOEVIRG
    {
        printf("[LOG] COMANDO -> FUNC_CALL;\n");
        $$ = strdup($1);
    }
    | IF ABREP CONDICAO FECHAP BLOCO
    {
        printf("[LOG] COMANDO -> if (CONDICAO) BLOCO\n");
        char buffer[4096];
        snprintf(buffer, sizeof(buffer), "if %s:\n        %s", $3, $5);
        $$ = strdup(buffer);
    }
    | IF ABREP CONDICAO FECHAP BLOCO ELSE BLOCO
    {
        printf("[LOG] COMANDO -> if (CONDICAO) BLOCO else BLOCO\n");
        char buffer[4096];
        snprintf(buffer, sizeof(buffer), "if %s:\n        %s\n    else:\n        %s", $3, $5, $7);
        $$ = strdup(buffer);
    }
    | ELSE BLOCO
    {
        printf("[LOG] COMANDO -> else BLOCO\n");
        char buffer[4096];
        snprintf(buffer, sizeof(buffer), "else:\n        %s", $2);
        $$ = strdup(buffer);
    }
    | IF ABREP CONDICAO FECHAP BLOCO ELSE COMANDO
    {
        printf("[LOG] COMANDO -> if (CONDICAO) BLOCO else COMANDO\n");
        char buffer[4096];
        snprintf(buffer, sizeof(buffer), "if %s:\n        %s\n    else:\n        %s", $3, $5, $7);
        $$ = strdup(buffer);
    }
    ;

FUNC_CALL:
    ID ABREP FECHAP
    {
        printf("[LOG] FUNC_CALL -> ID()\n");
        char buffer[128];
        snprintf(buffer, sizeof(buffer), "%s()", $1);
        $$ = strdup(buffer);
    }
    | ID ABREP EXPRESSAO_LIST FECHAP
    {
        printf("[LOG] FUNC_CALL -> ID(EXPRESSAO_LIST)\n");
        char buffer[256];
        snprintf(buffer, sizeof(buffer), "%s(%s)", $1, $3);
        $$ = strdup(buffer);
    }
    ;

DECLARACAO:
    INT ID ATRIB EXPRESSAO PONTOEVIRG
    {
        printf("[LOG] DECLARACAO -> INT ID = EXPRESSAO;\n");
        char buffer[256];
        snprintf(buffer, sizeof(buffer), "%s = %s", $2, $4);
        $$ = strdup(buffer);
    }
    ;

BLOCO:
    ABRECH COMANDO_LIST FECHACH
    {
        printf("[LOG] BLOCO -> { COMANDO_LIST }\n");
        $$ = malloc(strlen($2) + 10);
        sprintf($$, "    %s", $2);
    }
    ;

PRINT_FUNC:
    PRINTF ABREP STR VIRGULA EXPRESSAO FECHAP PONTOEVIRG
    {
        printf("[LOG] PRINT_FUNC -> printf(STR, EXPRESSAO);\n");
        char buffer[256];
        snprintf(buffer, sizeof(buffer), "print(%s, %s)", $3, $5);
        $$ = strdup(buffer);
    }
    | PRINTF ABREP STR FECHAP PONTOEVIRG
    {
        printf("[LOG] PRINT_FUNC -> printf(STR);\n");
        $$ = malloc(strlen($3) + 10);
        sprintf($$, "print(%s)", $3);
    }
    ;

EXPRESSAO_LIST:
    EXPRESSAO
    {
        printf("[LOG] EXPRESSAO_LIST -> EXPRESSAO\n");
        $$ = strdup($1);
    }
    | EXPRESSAO_LIST VIRGULA EXPRESSAO
    {
        printf("[LOG] EXPRESSAO_LIST -> EXPRESSAO_LIST, EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 5);
        sprintf($$, "%s, %s", $1, $3);
    }
    ;

LOOP:
    FOR_LOOP
    {
        $$ = strdup($1);
    }
    | WHILE ABREP CONDICAO FECHAP BLOCO
    {
        printf("[LOG] LOOP -> WHILE (CONDICAO) BLOCO\n");
        $$ = malloc(strlen($3) + strlen($5) + 10);
        sprintf($$, "while %s:\n%s", $3, $5);
    }
    ;

FOR_LOOP:
    FOR ABREP DECLARACAO CONDICAO PONTOEVIRG INCREMENTO FECHAP BLOCO
    {
        printf("[LOG] FOR_LOOP -> FOR (DECLARACAO; CONDICAO; INCREMENTO) BLOCO\n");
        char buffer[4096];
        snprintf(buffer, sizeof(buffer), "for %s in range(%s):\n        %s", $3, $4, $8);
        $$ = strdup(buffer);
    }
    ;


INCREMENTO:
    ID MAISMAIS
    {
        printf("[LOG] INCREMENTO -> ID++\n");
        $$ = malloc(strlen($1) + 10);
        sprintf($$, "%s + 1", $1);
    }
    ;

CONDICAO:
    EXPRESSAO
    {
        printf("[LOG] CONDICAO -> EXPRESSAO\n");
        $$ = strdup($1);
    }
    | CONDICAO AND CONDICAO
    {
        printf("[LOG] CONDICAO -> CONDICAO AND CONDICAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 6);
        sprintf($$, "%s and %s", $1, $3);
    }
    | CONDICAO OR CONDICAO
    {
        printf("[LOG] CONDICAO -> CONDICAO OR CONDICAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 5);
        sprintf($$, "%s or %s", $1, $3);
    }
    | EXPRESSAO IGUAL EXPRESSAO
    {
        printf("[LOG] CONDICAO -> EXPRESSAO == EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 5);
        sprintf($$, "%s == %s", $1, $3);
    }
    | EXPRESSAO DIFERENTE EXPRESSAO
    {
        printf("[LOG] CONDICAO -> EXPRESSAO != EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 5);
        sprintf($$, "%s != %s", $1, $3);
    }
    | EXPRESSAO MENOR EXPRESSAO
    {
        printf("[LOG] CONDICAO -> EXPRESSAO < EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s < %s", $1, $3);
    }
    | EXPRESSAO MAIOR EXPRESSAO
    {
        printf("[LOG] CONDICAO -> EXPRESSAO > EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s > %s", $1, $3);
    }
    ;

EXPRESSAO:
    ID
    {
        printf("[LOG] EXPRESSAO -> ID\n");
        $$ = strdup($1);
    }
    | NUM
    {
        printf("[LOG] EXPRESSAO -> NUM\n");
        $$ = strdup($1);
    }
    | FUNC_CALL
    {
        printf("[LOG] EXPRESSAO -> FUNC_CALL\n");
        $$ = strdup($1); // FUNC_CALL retorna uma string
    }
    | EXPRESSAO MAIS EXPRESSAO
    {
        printf("[LOG] EXPRESSAO -> EXPRESSAO + EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s + %s", $1, $3);
    }
    | EXPRESSAO MENOS EXPRESSAO
    {
        printf("[LOG] EXPRESSAO -> EXPRESSAO - EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s - %s", $1, $3);
    }
    | EXPRESSAO VEZES EXPRESSAO
    {
        printf("[LOG] EXPRESSAO -> EXPRESSAO * EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s * %s", $1, $3);
    }
    | EXPRESSAO DIVISAO EXPRESSAO
    {
        printf("[LOG] EXPRESSAO -> EXPRESSAO / EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s / %s", $1, $3);
    }
    | EXPRESSAO IGUAL EXPRESSAO
    {
        printf("[LOG] EXPRESSAO -> EXPRESSAO == EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 5);
        sprintf($$, "%s == %s", $1, $3);
    }
    | EXPRESSAO DIFERENTE EXPRESSAO
    {
        printf("[LOG] EXPRESSAO -> EXPRESSAO != EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 5);
        sprintf($$, "%s != %s", $1, $3);
    }
    | EXPRESSAO MENOR EXPRESSAO
    {
        printf("[LOG] CONDICAO -> EXPRESSAO < EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s < %s", $1, $3);
    }
    | EXPRESSAO MAIOR EXPRESSAO
    {
        printf("[LOG] EXPRESSAO -> EXPRESSAO > EXPRESSAO\n");
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s > %s", $1, $3);
    }
    ;


%%

int main(int argc, char **argv) {
    if (argc != 2) {
        printf("Modo de uso: ./transpiler codigo.c\n");
        return -1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file) {
        perror("Erro ao abrir o arquivo");
        return -1;
    }

    yyin = file;
    yyparse();
    fclose(file);

    return 0;
}
