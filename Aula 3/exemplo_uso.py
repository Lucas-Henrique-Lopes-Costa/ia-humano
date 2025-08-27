"""
Exemplo de uso do pacote cinema.
"""

from cinema import encontrar_melhor_fileira


def main():
    """Função principal com exemplo de uso."""
    # Exemplo de sala de cinema
    sala_exemplo = [
        [False, False, True, False, False, False],  # Fileira 0
        [False, False, False, False, True, False],  # Fileira 1
        [True, False, False, True, False, False],  # Fileira 2
    ]

    tamanho_grupo = 3
    melhor_fileira = encontrar_melhor_fileira(sala_exemplo, tamanho_grupo)

    if melhor_fileira != -1:
        print(
            f"Melhor fileira para o grupo de {tamanho_grupo} pessoas: {melhor_fileira}"
        )
    else:
        print(f"Não há fileira que acomode o grupo de {tamanho_grupo} pessoas")

    # Exemplo adicional - sala com empate
    print("\n--- Exemplo com empate ---")
    sala_empate = [
        [False, False, False, True, False, False],  # Fileira 0: 3 assentos consecutivos
        [True, False, False, False, True, False],  # Fileira 1: 3 assentos consecutivos
        [False, False, False, True, False, False],  # Fileira 2: 3 assentos consecutivos
    ]
    
    melhor_fileira_empate = encontrar_melhor_fileira(sala_empate, 3)
    print(f"Em caso de empate, escolhe a fileira: {melhor_fileira_empate}")


if __name__ == "__main__":
    main()
