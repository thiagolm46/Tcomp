from afd import ler_afn_do_arquivo

def simular_cadeia(afd, cadeia):
    estado_atual = afd.initial_state
    for simbolo in cadeia:
        chave = (estado_atual, simbolo)
        if chave in afd.transitions:
            estado_atual = afd.transitions[chave][0]  # determinístico: só um destino
        else:
            return False
    return estado_atual in afd.final_states

if __name__ == "__main__":
    # Entrada da cadeia
    cadeia = input("Entrada fornecida: w = ").strip()

    # Carrega o AFD determinizado
    afd = ler_afn_do_arquivo("./output/AFD_complemento.txt")

    # Simula a cadeia
    aceita = simular_cadeia(afd, cadeia)

    print(f"Cadeia: {cadeia}")
    print("Resultado:", "Aceita" if aceita else "Rejeitada")
    print("Arquivos Gerados: AFN.txt, AFD.txt, AFD_reverso.txt, AFD_complemento.txt")