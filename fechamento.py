from afd import ler_afn_do_arquivo, salvar_afd_em_arquivo, Automato, determinizar_afn

def reverter_afd(afd: Automato) -> Automato:
    # Troca estados inicial e finais, inverte todas as transições
    novos_finais = {afd.initial_state}
    novo_inicial = set(afd.final_states)
    novas_transicoes = {}

    for (origem, simbolo), destinos in afd.transitions.items():
        for destino in destinos:
            chave = (destino, simbolo)
            if chave not in novas_transicoes:
                novas_transicoes[chave] = []
            novas_transicoes[chave].append(origem)

    # Novo autômato pode ser não-determinístico, então determinize
    reverso_afn = Automato(
        states=afd.states,
        alphabet=afd.alphabet,
        transitions=novas_transicoes,
        initial_state=None,  # Será um novo estado inicial fictício
        final_states=novos_finais
    )

    # Novo estado inicial fictício com transições epsilon para todos os antigos finais
    novo_estado_inicial = "QI"
    reverso_afn.states.add(novo_estado_inicial)
    reverso_afn.initial_state = novo_estado_inicial
    for f in novo_inicial:
        chave = (novo_estado_inicial, "")  # "" representa epsilon
        if chave not in reverso_afn.transitions:
            reverso_afn.transitions[chave] = []
        reverso_afn.transitions[chave].append(f)

    # Determinizar o reverso para obter um AFD reverso
    reverso_afd = determinizar_afn(reverso_afn)
    return reverso_afd

def complemento_afd(afd: Automato) -> Automato:
    # Garante que o AFD é completo (todas as transições existem)
    estados = set(afd.states)
    alfabeto = set(afd.alphabet)
    transicoes = dict(afd.transitions)
    estado_morto = "Z"
    if estado_morto not in estados:
        estados.add(estado_morto)
    for estado in estados:
        for simbolo in alfabeto:
            if (estado, simbolo) not in transicoes:
                transicoes[(estado, simbolo)] = [estado_morto]
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
    afd = ler_afn_do_arquivo("AFD.txt")
    afd_reverso = reverter_afd(afd)
    salvar_afd_em_arquivo(afd_reverso, "AFD_reverso.txt")
    print("Arquivo 'AFD_reverso.txt' gerado com sucesso!")

    # Complemento
    afd = ler_afn_do_arquivo("AFD.txt")
    afd_complemento = complemento_afd(afd)
    salvar_afd_em_arquivo(afd_complemento, "AFD_complemento.txt")
    print("Arquivo 'AFD_complemento.txt' gerado com sucesso!")