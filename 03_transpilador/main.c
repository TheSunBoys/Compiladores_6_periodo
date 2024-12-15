#include <stdio.h>
#include <stdlib.h>

extern int yyparse();
extern FILE *yyin;

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}

int main(int argc, char **argv) {
    printf("[INFO] Iniciando o transpilador...\n");

    if (argc != 2) {
        fprintf(stderr, "[ERRO] Uso: %s <arquivo>\n", argv[0]);
        return 1;
    }

    printf("[INFO] Abrindo arquivo: %s\n", argv[1]);
    FILE *file = fopen(argv[1], "r");
    if (!file) {
        perror("[ERRO] Erro ao abrir o arquivo");
        return 1;
    }

    printf("[INFO] Definindo yyin e chamando yyparse...\n");
    yyin = file; // Define o arquivo de entrada para o analisador
    yyparse();
    if (yyparse() == 0) {
        printf("[INFO] Transpilação concluída com sucesso.\n");
    } else {
        printf("[ERRO] Falha durante a transpilação.\n");
    }

    fclose(file);
    printf("[INFO] Arquivo fechado e programa concluído.\n");
    return 0;
}
