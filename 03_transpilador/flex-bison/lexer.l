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
LETRA [A-Za-z]
IDENTIFICADOR {LETRA}({LETRA}|{DIGITO})*

%%
"#include".* { 
    printf("[LOG] Ignorando linha de inclusão: %s\n", yytext); 
    // Ignora a linha inteira que começa com #include e não retorna tokens
}

[ \n]+        ;  // Ignora espaços em branco e quebras de linha
"main"          { return MAIN; }
"int"           { return INT; }
"float"         { return FLOAT; }
"void"          { return VOID; }
"return"        { return RETURN; }
"printf"        { return PRINTF; }
"for"           { return FOR; }
"while"         { return WHILE; }
"if"            { return IF; }
"else"          { return ELSE; }
"("             { return ABREP; }
")"             { return FECHAP; }
"{"             { return ABRECH; }
"}"             { return FECHACH; }
";"             { return PONTOEVIRG; }
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

{IDENTIFICADOR} { yylval.str = strdup(yytext); return ID; }
{NUMERO}        { yylval.str = strdup(yytext); return NUM; }

[ \t]+          ;  // Ignorar espaços em branco
\n              ;  // Ignorar quebras de linha
.               { printf("[ERRO] Caractere desconhecido na linha %d: %s\n", yylineno, yytext); }
%%
