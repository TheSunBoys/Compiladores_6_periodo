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

Transpilador de Código Fonte Python para Bend

#### O que é Bend?
- Bend é uma linguagem de programação de alto nível brasileira com lançamento em 2024
- Bend tem como maior atrativo o fato de ser executada na placa de vídeo e não na memória RAM
- Bend tem suporte a processos paralelos usando GPUs e pode usar núcleos CUDA para extrair ainda mais performance

veja mais sobre: [https://github.com/HigherOrderCO/Bend](https://github.com/HigherOrderCO/Bend)

#### requirements
- install rust and gcc
    ```bash
    # rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

    #gcc
    sudo apt install gcc # derivados de Debian
    sudo pacman -S # derivados de Arch
    ```

- install hvm2
    ```
    # HVM2 é a ferramente de avaliação de interação combinatória paralela do HOC
    cargo install hvm

    # Verifica que o hvm está instalado e sua versão
    hvm --version
    ``` 

- install Bend lang
    ```bash
    # Instalação da linguagem Bend
    cargo install bend-lang

    # Verifica que está instalado e sua versão
    bend --version
    ```

#### como rodar o Bend?
- É recomendado rodar o bend com C ou com CUDA (se tiver gpu Nvidia) para extrair a maior performance possível
- A maior performance do programa é usando núcleos CUDA
```bash
- bend run    <file.bend> # usa o interpretador C por padrão (em paralelo)
- bend run-rs <file.bend> # usa o interpretador Rust (em sequencial)
- bend run-c  <file.bend> # usa o interpretador C (em paralelo)
- bend run-cu <file.bend> # usa o interpretador CUDA (massivamente em paralelo)
- bend run-rs <file.bend> -s # adicione o "-s" no comando para rodar o código sequencialmente
```

#### Arch linux configuração para usar CUDA
instalação das libs do CUDA
```bash
sudo pacman -S cuda
sudo pacman -S cuda-tools
```

verifique se há uma versão menor ou igual a 13 do gcc (necessário para o CUDA) 
```bash
ls -l /usr/bin/gcc* # mostra todas as opções do gcc (se houver uma versão <=13 use ela senão instale)
```

caso não haja instale algum desses (processo demorado pela compilação do gcc)
```bash
yay -S gcc11
which gcc11 # escolha a versão do gcc e guarde o caminho onde ela está
```

escreva isso no arquivo de inicialização do seu shell: .bashrc, .zshrc, etc... 
```bash
export CUDA_HOME=/opt/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRA>
export CXX=/usr/bin/gcc-13 # aqui você coloca o caminho do gcc instalado >=13 
```

** agora prossiga para as instalações de instalação do HVM e Bend **