%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.h"
%}

%option noyywrap
%option nodefault
%option yylineno

BRANCO [ \t]
ESPACO {BRANCO}+
DIGITO [0-9]
NUMERO {DIGITO}+
LETRA [A-Za-z_]

IDENTIFICADOR [A-Za-z_][A-Za-z0-9_]*

%%
[ \n]+ {
    /* Ignora linhas em branco ou espaços */
}

"#include".* {
    /* Ignora linhas de importação de bibliotecas */
}

"//".* {
    /* Ignora comentários de linha */
}

"/\\*".*"\\*/" {
    /* Ignora comentários de bloco */
}

\"([^"\\]|\\.)*\" {
    yylval.str = strdup(yytext); // Copiar a string completa
    return STR; // Retornar token STR
}

"main"          { return MAIN; }
"int"           { return INT; }
"float"         { return FLOAT; }
"void"          { return VOID; }
"return"        { return RETURN; }
"printf"        { return PRINTF; }
"for"           { return FOR; }
"if"            { return IF; }
"else"          { return ELSE; }
"("             { return ABREP; }
")"             { return FECHAP; }
"{"             { return ABRECH; }
"}"             { return FECHACH; }
";"             { return PONTOEVIRG; }
","             { return VIRGULA; }
"="             { return ATRIB; }
"+"             { return MAIS; }
"++"            { return MAISMAIS; }
"-"             { return MENOS; }
"*"             { return VEZES; }
"/"             { return DIVISAO; }
"<"             { return MENOR; }
">"             { return MAIOR; }
"<="            { return MENORIGUAL; }
">="            { return MAIORIGUAL; }
"=="            { return IGUAL; }
"!="            { return DIFERENTE; }
"&&"            { return AND; }
"||"            { return OR; }

{IDENTIFICADOR} {
    printf("[LOG] Identificador detectado: %s [na linha %d]\n", yytext, yylineno);
    yylval.str = strdup(yytext);
    return ID;
}

{NUMERO} {
    printf("[LOG] Número detectado: %s [na linha %d]\n", yytext, yylineno);
    yylval.str = strdup(yytext);
    return NUM;
}

\n {
    printf("[LOG] Quebra de linha detectada [na linha %d]\n", yylineno);
}

.               { printf("[ERRO] Caractere desconhecido [na linha %d]: %s\n", yylineno, yytext); }
%%
