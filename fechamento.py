from afd import ler_afn_do_arquivo, salvar_afd_em_arquivo, Automato, determinizar_afn

def reverter_afd(afd: Automato) -> Automato:
    # Inverte todas as transições
    novas_transicoes = {}
    for (origem, simbolo), destinos in afd.transitions.items():
        for destino in destinos:
            chave = (destino, simbolo)
            if chave not in novas_transicoes:
                novas_transicoes[chave] = []
            novas_transicoes[chave].append(origem)

    # Novo estado inicial fictício com transições vazias para todos os antigos finais
    novo_estado_inicial = "QI"
    estados = set(afd.states)
    estados.add(novo_estado_inicial)
    for f in afd.final_states:
        chave = (novo_estado_inicial, "")  # "" representa vazio
        if chave not in novas_transicoes:
            novas_transicoes[chave] = []
        novas_transicoes[chave].append(f)

    # O antigo inicial vira final
    novos_finais = {afd.initial_state}

    reverso_afn = Automato(
        states=estados,
        alphabet=afd.alphabet,
        transitions=novas_transicoes,
        initial_state=novo_estado_inicial,
        final_states=novos_finais
    )

    # Determiniza o reverso para obter um AFD reverso
    reverso_afd = determinizar_afn(reverso_afn)
    return reverso_afd

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
    afd = ler_afn_do_arquivo("./output/AFD.txt")
    afd_reverso = reverter_afd(afd)
    salvar_afd_em_arquivo(afd_reverso, "./output/AFD_reverso.txt")
    print("Arquivo 'AFD_reverso.txt' gerado com sucesso!")

    # Complemento
    afd = ler_afn_do_arquivo("./output/AFD.txt")
    afd_complemento = complemento_afd(afd)
    salvar_afd_em_arquivo(afd_complemento, "./output/AFD_complemento.txt")
    print("Arquivo 'AFD_complemento.txt' gerado com sucesso!")