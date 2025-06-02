from typing import Dict, List, Tuple, Set


class Automato:
    def __init__(self, states: Set[str], alphabet: Set[str],
                 transitions: Dict[Tuple[str, str], List[str]],
                 initial_state: str, final_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states


def ler_afn_do_arquivo(caminho: str) -> Automato:
    with open(caminho, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip() != ""]

    states = set()
    alphabet = set()
    transitions = dict()
    initial_state = ""
    final_states = set()

    for linha in linhas:
        if linha.startswith("Q:"):
            states = set(item.strip() for item in linha[2:].split(","))
        elif linha.startswith("Σ:") or linha.startswith("I:"):
            alphabet = set(item.strip() for item in linha[2:].split(","))
        elif linha.startswith("δ:") or linha.startswith("6:"):
            continue  # A linha apenas indica início das transições
        elif "->" in linha:
            partes = linha.split("->")
            esquerda = partes[0].strip()
            direita = partes[1].strip()

            origem, simbolo = [x.strip() for x in esquerda.split(",")]

            chave = (origem, simbolo)
            if chave not in transitions:
                transitions[chave] = []

            transitions[chave].append(direita)
        elif ": inicial" in linha:
            initial_state = linha.split(":")[0].strip()
        elif linha.startswith("F:"):
            finais = linha[2:].split(",")
            final_states = set(item.strip() for item in finais)

    return Automato(states, alphabet, transitions, initial_state, final_states)


def determinizar_afn(afn: Automato) -> Automato:
    afd_states: Set[str] = set()
    afd_transitions: Dict[Tuple[str, str], List[str]] = {}
    afd_final_states: Set[str] = set()

    initial_set = frozenset([afn.initial_state])
    estados_mapeados = {initial_set: nome_estado(initial_set)}
    fila = [initial_set]

    afd_states.add(nome_estado(initial_set))

    if any(state in afn.final_states for state in initial_set):
        afd_final_states.add(nome_estado(initial_set))

    while fila:
        atual = fila.pop(0)
        nome_atual = nome_estado(atual)

        for simbolo in afn.alphabet:
            destino = set()

            for estado in atual:
                chave = (estado, simbolo)
                if chave in afn.transitions:
                    destino.update(afn.transitions[chave])

            if destino:
                nome_destino = nome_estado(frozenset(destino))
                afd_transitions[(nome_atual, simbolo)] = [nome_destino]

                if nome_destino not in afd_states:
                    afd_states.add(nome_destino)
                    fila.append(frozenset(destino))

                    if any(state in afn.final_states for state in destino):
                        afd_final_states.add(nome_destino)
            # Se não há destino, não adiciona transição (não há estado morto)

    return Automato(
        states=afd_states,
        alphabet=afn.alphabet,
        transitions=afd_transitions,
        initial_state=nome_estado(initial_set),
        final_states=afd_final_states
    )

def nome_estado(estado_conjunto: frozenset) -> str:
    elementos = sorted(estado_conjunto)
    return "{" + ", ".join(elementos) + "}"


def salvar_afd_em_arquivo(afd: Automato, caminho: str):
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write("AFD Determinizado\n")

        f.write("Q: " + ', '.join(sorted(afd.states)) + "\n")
        f.write("Σ: " + ', '.join(sorted(afd.alphabet)) + "\n")
        f.write("δ:\n")
        for (from_state, symbol), to_states in sorted(afd.transitions.items()):
            for to_state in to_states:
                f.write(f"{from_state}, {symbol} -> {to_state}\n")
        f.write(f"{afd.initial_state}: inicial\n")
        f.write("F: " + ', '.join(sorted(afd.final_states)) + "\n")


# Execução principal
if __name__ == "__main__":
    caminho_afn = "AFN.txt"
    caminho_afd = "AFD.txt"

    # Ler o AFN do arquivo
    afn = ler_afn_do_arquivo(caminho_afn)

    # Determinizar
    afd = determinizar_afn(afn)

    # Salvar no arquivo
    salvar_afd_em_arquivo(afd, caminho_afd)

    print(f"Arquivo '{caminho_afd}' gerado com sucesso!")
