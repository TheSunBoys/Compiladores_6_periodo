#include <stdio.h>
#include <string.h>

// declaração de função com pârametros posicionais
int sum_foo(int num, int num2) {
    return num + num2;
}

// declaração de função com pârametros posicionais
int two_values(int num, int num2) {
    // Expressões lógicas com E e OU;
    if (num && num2) {
        printf("Os dois valores foram dados.\n");
        return 0;
    } // Expressões lógicas com E e OU; 
    else if (num || num2) {
        printf("Apenas um valor dos dois foi dado.\n");
        return 1;
    }
    return 0;
}

int main() {
    // declaração de váriaveis
    int x = 5;
    int y = 10;

    // comando de repetição
    for (int i = 1; i < 10; i++) {
        printf("Valor de i: %d\n", i);
    }

    // expressões lógicas
    printf("Y é menor que X: %d", y<x);
    printf("Y é maior que X: %d", y>x);
    printf("Y é igual a X: %d", x==y);
    printf("Y é diferente de X: %d", x!=y);

    // chamada de função com pârametros posicionais
    int soma = sum_foo(2, y);

    // expressões aritmeticas
    int z = x - 10 * soma / 4;

    // comando condicional
    if (z == 5) {
        printf("Valor de z é 5: %d\n", x);
    } else if (z == 10) {
        printf("Valor de z é 10: %d\n", x);
    } else {
        printf("Valor de z não é 5 nem 10: %d\n", x);
    }

    // chamada de função com pârametros posicionais
    int response = two_values(x, y);
    
    // comando condicional
    if (response == 0) {
        printf("Ambos os valores foram dados.\n");
    } else if (response == 1) {
        printf("Apenas um valor dos dois foi dado.\n");
    }

    return 0;
}