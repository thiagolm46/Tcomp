from afn import ler_gramatica_do_arquivo, convert_grammar_to_afn, salvar_afn_em_arquivo
from afd import ler_afn_do_arquivo, determinizar_afn, salvar_afd_em_arquivo
from fechamento import reverter_afd, complemento_afd, salvar_afd_em_arquivo as salvar_afd_fechamento
from cadeia import simular_cadeia

def main():
    caminho = input("Digite o caminho do arquivo .txt da gramática: ").strip()
    # 1. Ler e converter gramática para AFN
    grammar, _ = ler_gramatica_do_arquivo(caminho)
    afn = convert_grammar_to_afn(grammar)
    salvar_afn_em_arquivo(afn, "./output/AFN.txt")
    print("AFN gerado em AFN.txt")

    # 2. Determinizar AFN para AFD
    afd = determinizar_afn(afn)
    salvar_afd_em_arquivo(afd, "./output/AFD.txt")
    print("AFD gerado em AFD.txt")

    # 3. Fechamento: reverso e complemento
    afd_reverso = reverter_afd(afn)  # O reverso deve ser feito sobre o AFN!
    salvar_afd_fechamento(afd_reverso, "./output/AFD_reverso.txt")
    print("AFD reverso gerado em AFD_reverso.txt")

    afd_complemento = complemento_afd(afd)
    salvar_afd_fechamento(afd_complemento, "./output/AFD_complemento.txt")
    print("AFD complemento gerado em AFD_complemento.txt")

    # 4. Simular cadeia
    cadeia = input("Digite a cadeia para testar: ").strip()
    resultado = simular_cadeia(afd, cadeia)
    print(f"Cadeia: {cadeia}")
    print("Resultado:", "Aceita" if resultado else "Rejeitada")
    print("Arquivos Gerados: AFN.txt, AFD.txt, AFD_reverso.txt, AFD_complemento.txt")

if __name__ == "__main__":
    main()