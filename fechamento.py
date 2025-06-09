from afd import ler_afn_do_arquivo, salvar_afd_em_arquivo, Automato, determinizar_afn


# Gera o autômato reverso (AFD reverso) de um AFD dado:
#     - Inverte as transições.
#     - Cria um novo estado inicial com transições epsilon para os antigos estados finais.
#     - Define o antigo estado inicial como o novo final.
#     - Determiniza o autômato reverso obtido.
def reverter_afd(afd: Automato) -> Automato:
       # Inverte todas as transições do AFD original
    novas_transicoes = {}
    for (origem, simbolo), destinos in afd.transitions.items():
        for destino in destinos:
            chave = (destino, simbolo)
            if chave not in novas_transicoes:
                novas_transicoes[chave] = []
            novas_transicoes[chave].append(origem)

    # Novo estado inicial fictício com transições ε para os antigos estados finais
    novo_estado_inicial = "QI"
    estados = set(afd.states)
    estados.add(novo_estado_inicial)
    for f in afd.final_states:
        chave = (novo_estado_inicial, "")  # transição ε
        if chave not in novas_transicoes:
            novas_transicoes[chave] = []
        novas_transicoes[chave].append(f)

    # O antigo estado inicial se torna o único novo estado final
    novos_finais = {afd.initial_state}

    # Cria o AFN reverso
    reverso_afn = Automato(
        states=estados,
        alphabet=afd.alphabet,
        transitions=novas_transicoes,
        initial_state=novo_estado_inicial,
        final_states=novos_finais
    )

    # Determiniza o AFN reverso para obter um AFD que reconhece a linguagem reversa
    reverso_afd = determinizar_afn(reverso_afn)
    return reverso_afd

#  Gera o complemento de um AFD:
#     - Garante que o autômato seja completo (todas as transições definidas).
#     - Cria e adiciona o estado morto '∅' para transições ausentes.
#     - Inverte os estados finais: todos os estados que não eram finais passam a ser.

def complemento_afd(afd: Automato) -> Automato:
    # Garante que o AFD é completo (todas as transições existem)
    estados = set(afd.states)
    alfabeto = set(afd.alphabet)
    transicoes = dict(afd.transitions)
    estado_morto = "∅"
    if estado_morto not in estados:
        estados.add(estado_morto)
    # Adiciona transições faltantes para o estado morto
    for estado in estados:
        for simbolo in alfabeto:
            if (estado, simbolo) not in transicoes:
                transicoes[(estado, simbolo)] = [estado_morto]
    # O estado morto faz laço para si mesmo
    for simbolo in alfabeto:
        transicoes[(estado_morto, simbolo)] = [estado_morto]

    # Complementa os estados finais
    novos_finais = set(estados) - set(afd.final_states)
    return Automato(
        states=estados,
        alphabet=alfabeto,
        transitions=transicoes,
        initial_state=afd.initial_state,
        final_states=novos_finais
    )

if __name__ == "__main__":
    # Reverso
    afd = ler_afn_do_arquivo("./output/AFN.txt")
    afd_reverso = reverter_afd(afd)
    salvar_afd_em_arquivo(afd_reverso, "./output/AFD_reverso.txt")
    print("Arquivo 'AFD_reverso.txt' gerado com sucesso!")

    # Complemento
    afd = ler_afn_do_arquivo("./output/AFD.txt")
    afd_complemento = complemento_afd(afd)
    salvar_afd_em_arquivo(afd_complemento, "./output/AFD_complemento.txt")
    print("Arquivo 'AFD_complemento.txt' gerado com sucesso!")