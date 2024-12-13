all: transpiler

transpiler: lexer.o parser.o
	gcc -o transpiler lexer.o parser.o -lfl

lexer.o: lexer.c
	gcc -c lexer.c -o lexer.o

parser.o: parser.c
	gcc -c parser.c -o parser.o

lexer.c: lexer.l parser.h
	flex -o lexer.c lexer.l

parser.c parser.h: parser.y
	bison -d -o parser.c parser.y

clean:
	rm -f transpiler lexer.c parser.c parser.h lexer.o parser.o
