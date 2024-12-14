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
    printf("[LOG] Ignorando linha de inclusão: %s [na linha %d]\n", yytext, yylineno); 
    /* Ignorar linhas de inclusão e não retornar token */ 
}

"//".* { 
    yylval.str = strdup(yytext + 2); // Ignorar "//" e pegar o texto
    printf("[LOG] Comentário de linha detectado: %s [na linha: %d]\n", yylval.str, yylineno);
    return STR;
}

"/\\*".*"\\*/" {
    yylval.str = strdup(yytext + 2); // Ignorar "/*" no início
    yylval.str[strlen(yylval.str) - 2] = '\0'; // Remover "*/" no final
    printf("[LOG] Comentário de bloco detectado: %s [na linha: %d]\n", yylval.str, yylineno);
    return STR;
}

[ \n]+ { 
    printf("[LOG] Ignorando quebra de linha ou espaço em branco: %s na [linha: %d]\n", yytext, yylineno); 
}

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
