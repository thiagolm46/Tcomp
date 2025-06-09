from typing import Dict, List, Tuple, Set


class Grammar:
    # Representa uma gramática livre do lado direito
    def __init__(self, start_symbol: str, productions: Dict[str, List[str]]):
        self.start_symbol = start_symbol
        self.productions = productions


class AFN:
    # Representa um autômato finito não-determinístico
    #Utilizando a definição formal de automato que é um 5-upla (Q, Σ, δ, q0, F)
    def __init__(self):
        self.states: Set[str] = set()
        self.alphabet: Set[str] = set()
        self.transitions: Dict[Tuple[str, str], List[str]] = dict()
        self.initial_state: str = ""
        self.final_states: Set[str] = set()

    def add_transition(self, from_state: str, symbol: str, to_state: str):
        key = (from_state, symbol)
        if key not in self.transitions:
            self.transitions[key] = []
        self.transitions[key].append(to_state)

# Lê uma gramática e uma cadeia a ser testada a partir de um arquivo.
# Retorna a gramática como objeto `Grammar` e a cadeia como string.
def ler_gramatica_do_arquivo(caminho: str) -> Tuple[Grammar, str]:

    with open(caminho, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip() != ""]

    productions: Dict[str, List[str]] = {}
    start_symbol = None
    cadeia = ""

    for linha in linhas:
        if linha.startswith("#"):
            # Tentativa de extrair símbolo inicial da linha do comentário, exemplo:
            # "#Gramatica G = ({S,A}, {a,b}, P, S)"
            if "P," in linha:
                partes = linha.split(",")
                start_candidate = partes[-1].replace(")", "").strip()
                if start_candidate.isalpha():
                    start_symbol = start_candidate
            continue

        if linha.lower().startswith("cadeia"):
            cadeia = linha.split(":")[1].strip()
            continue

        if "->" in linha:
            lado_esq, lado_dir = linha.split("->")
            nao_terminal = lado_esq.strip()

            if start_symbol is None:
                start_symbol = nao_terminal  # Primeira produção define o símbolo inicial

            regras = [regra.strip() for regra in lado_dir.strip().split("|")]

            regras_processadas = []
            for regra in regras:
                regra_limpa = regra.strip()
                if regra_limpa in ['" "', 'ε', "'ε'", '"ε"']:
                    regras_processadas.append("")
                else:
                    regras_processadas.append(regra_limpa)

            if nao_terminal not in productions:
                productions[nao_terminal] = []
            productions[nao_terminal].extend(regras_processadas)

    if start_symbol is None:
        raise ValueError("Símbolo inicial não encontrado.")

    gramatica = Grammar(start_symbol, productions)
    return gramatica, cadeia


# Converte uma gramática regular em um autômato finito não-determinístico (AFN).
# Cria um estado final especial 'QF' e adiciona transições com base nas produções.
def convert_grammar_to_afn(grammar: Grammar) -> AFN:
    afn = AFN()

    afn.states = set(grammar.productions.keys())
    final_state = "QF"
    afn.states.add(final_state)
    afn.final_states = {final_state}
    afn.initial_state = grammar.start_symbol

    # Descobrir o alfabeto completo
    for rules in grammar.productions.values():
        for production in rules:
            if production == "" or production == "ε":
                continue
            symbol = production[0]
            afn.alphabet.add(symbol)

    # Adicionar transições da gramática
    for non_terminal, rules in grammar.productions.items():
        for production in rules:
            if production == "" or production == "ε":
                # Adiciona transição epsilon para o estado final especial
                afn.add_transition(non_terminal, "", final_state)
            elif len(production) == 1:
                symbol = production
                afn.add_transition(non_terminal, symbol, final_state)
            elif len(production) == 2:
                symbol, next_state = production[0], production[1]
                afn.add_transition(non_terminal, symbol, next_state)
            else:
                raise ValueError(f"Produção inválida: {production}")

    return afn

#Formatação do arquivo de saída do AFN
def salvar_afn_em_arquivo(afn: AFN, caminho: str):
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write("AFN Original\n")

        # Estados
        f.write("Q: " + ', '.join(sorted(afn.states)) + "\n")

        # Alfabeto
        f.write("Σ: " + ', '.join(sorted(afn.alphabet)) + "\n")

        # Transições
        f.write("δ:\n")
        for (from_state, symbol), to_states in sorted(afn.transitions.items()):
            for to_state in to_states:
                f.write(f"{from_state}, {symbol} -> {to_state}\n")

        # Estado inicial
        f.write(f"{afn.initial_state}: inicial\n")

        # Estados finais
        f.write("F: " + ', '.join(sorted(afn.final_states)) + "\n")


def print_afn(afn: AFN):
    print("Estados:", afn.states)
    print("Alfabeto:", afn.alphabet)
    print("Estado inicial:", afn.initial_state)
    print("Estados finais:", afn.final_states)
    print("Transições:")
    for (from_state, symbol), to_states in afn.transitions.items():
        for to_state in to_states:
            print(f"  {from_state} --{symbol}--> {to_state}")


if __name__ == "__main__":
    caminho_entrada = "g1.txt"

    # Ler gramática
    gramatica, cadeia = ler_gramatica_do_arquivo(caminho_entrada)

    # Mostrar a cadeia lida
    print(f"Cadeia a ser testada: {cadeia}")

    # Converter para AFN
    afn = convert_grammar_to_afn(gramatica)

    # Imprimir no console
    print_afn(afn)

    # Salvar no arquivo
    salvar_afn_em_arquivo(afn, "./output/AFN.txt")
    print("Arquivo 'AFN.txt' gerado com sucesso!")
