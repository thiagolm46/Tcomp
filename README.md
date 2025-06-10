# Trabalho 1 Teoria da Computação 

# Conversão de Gramática para Autômatos (AFN/AFD) e Operações

Este projeto realiza a conversão de uma **gramática regular** para um **AFN**, a determinização do AFN para um **AFD**, e as operações de **reverso** e **complemento** sobre esse AFD.

---

## Estrutura de Arquivos

| Arquivo         | Descrição |
|------------------|-----------|
| `afn.py`         | Converte uma gramática regular em um AFN e salva no arquivo. |
| `afd.py`         | Lê um AFN e o determiniza (AFN → AFD). Salva o AFD. |
| `fechamento.py`  | Aplica operações de **reverso** e **complemento** no AFD determinizado. |
| `output/`        | Diretório de saída com os arquivos `AFN.txt`, `AFD.txt`, etc. |
| `g1.txt`         | Arquivo de entrada contendo a gramática e a cadeia. |
| `main.py`        | Arquivo que executa as principais funções e cria todos os arquivos uma única vez |
| `cadeia.py`      | Arquivo que testa a entrada de uma cadeia |

---

# Execução 

## Execução direta 

Executando o arquivo main.py , é possível carregar o caminho para uma gramática válida e serão criados automaticamente todos os arquivos solicitados para aquela gramática.
A Execução dessa forma pede posteriormente o input de uma cadeia para o AFN 

## Execução específica

No arquivo cadeia.py , é possível indicar qual máquina quer testar
a função : 
afd = ler_afn_do_arquivo("./output/AFD_reverso.txt")

presente neste arquivo nos permite carregar as outras saídas geradas , no caso acima , está indicando o AFD_reverso, mas é possível carregar os outros arquivos. 
