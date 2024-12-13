%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.h"

extern FILE *yyin;
int yylex(void);
void yyerror(const char *msg) {
    fprintf(stderr, "Erro: %s\n", msg);
}
%}

%union {
    char *str;
}

%token <str> INT FLOAT VOID RETURN PRINTF FOR WHILE IF ELSE
%token <str> ABREP FECHAP ABRECH FECHACH PONTOEVIRG ATRIB MAIS MAISMAIS MENOS VEZES DIVISAO
%token <str> MENOR MAIOR MENORIGUAL MAIORIGUAL IGUAL DIFERENTE ID NUM STR FIM_LINHA MAIN

%type <str> PROGRAM MAIN_FUNC COMANDO_LIST COMANDO BLOCO DECLARACAO EXPRESSAO PRINT_FUNC LOOP FOR_LOOP CONDICAO INCREMENTO

%left MENOR MAIOR MENORIGUAL MAIORIGUAL IGUAL DIFERENTE
%left MAIS MENOS
%left VEZES DIVISAO

%%

PROGRAM:
    MAIN_FUNC
    {
        printf("[LOG] PROGRAM -> MAIN_FUNC\n");
        printf("[LOG] Código principal:\n%s\n", $1);
        $$ = strdup($1);
    }
    ;

MAIN_FUNC:
    INT MAIN ABREP FECHAP ABRECH COMANDO_LIST FECHACH
    {
        printf("[LOG] MAIN_FUNC -> INT MAIN () { COMANDO_LIST }\n");
        $$ = malloc(strlen($6) + 40);
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
        $$ = malloc(strlen($1) + strlen($2) + 2);
        sprintf($$, "%s\n%s", $1, $2);
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
        $$ = malloc(strlen($2) + 10);
        sprintf($$, "return %s", $2);
    }
    ;

DECLARACAO:
    INT ID ATRIB EXPRESSAO PONTOEVIRG
    {
        $$ = malloc(strlen($2) + strlen($4) + 4);
        sprintf($$, "%s = %s", $2, $4);
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
    PRINTF ABREP STR FECHAP PONTOEVIRG
    {
        $$ = malloc(strlen($3) + 10);
        sprintf($$, "print(%s)", $3);
    }
    ;

LOOP:
    FOR_LOOP
    {
        $$ = strdup($1);
    }
    | WHILE ABREP CONDICAO FECHAP BLOCO
    {
        $$ = malloc(strlen($3) + strlen($5) + 10);
        sprintf($$, "while %s:\n%s", $3, $5);
    }
    ;

FOR_LOOP:
    FOR ABREP DECLARACAO CONDICAO PONTOEVIRG INCREMENTO FECHAP BLOCO
    {
        printf("[LOG] FOR_LOOP -> FOR (DECLARACAO; CONDICAO; INCREMENTO) BLOCO\n");
        $$ = malloc(strlen($3) + strlen($4) + strlen($6) + strlen($8) + 50);
        sprintf($$, "for %s in range(%s):\n%s", $3, $4, $8);
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
    EXPRESSAO MENOR EXPRESSAO
    {
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s < %s", $1, $3);
    }
    ;

EXPRESSAO:
    ID
    {
        $$ = strdup($1);
    }
    | NUM
    {
        $$ = strdup($1);
    }
    | ID MAIS NUM
    {
        $$ = malloc(strlen($1) + strlen($3) + 4);
        sprintf($$, "%s + %s", $1, $3);
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
