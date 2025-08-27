#!/usr/bin/env python3
"""
Exemplo de uso da função encontrar_melhor_fileira.

Este arquivo demonstra como usar a função para encontrar a melhor fileira
de cinema para um grupo se sentar junto.
"""

from cinema_seats import encontrar_melhor_fileira


def main():
    """Função principal com exemplos de uso."""

    print("=== Exemplo de Uso: Escolha de Fileira no Cinema ===\n")

    # Exemplo 1: Sala com múltiplas fileiras
    print("Exemplo 1: Sala com múltiplas fileiras")
    sala1 = [
        [False, False, True, False, False],  # Fileira 0: 2 assentos consecutivos
        [True, False, False, False, True],  # Fileira 1: 3 assentos consecutivos
        [False, False, False, False, False],  # Fileira 2: 5 assentos consecutivos
    ]

    print("Sala de cinema:")
    for i, fileira in enumerate(sala1):
        status = ["L" if not assento else "O" for assento in fileira]
        print(f"Fileira {i}: {' '.join(status)}")

    for tamanho_grupo in [2, 3, 4, 5, 6]:
        melhor_fileira = encontrar_melhor_fileira(sala1, tamanho_grupo)
        if melhor_fileira != -1:
            print(f"Grupo de {tamanho_grupo} pessoas: Fileira {melhor_fileira}")
        else:
            print(f"Grupo de {tamanho_grupo} pessoas: Nenhuma fileira adequada")

    print("\n" + "=" * 50 + "\n")

    # Exemplo 2: Empate entre fileiras
    print("Exemplo 2: Empate entre fileiras")
    sala2 = [
        [False, False, False, True, False],  # Fileira 0: 3 assentos consecutivos
        [True, False, False, False, True],  # Fileira 1: 3 assentos consecutivos
        [False, False, False, True, False],  # Fileira 2: 3 assentos consecutivos
    ]

    print("Sala de cinema:")
    for i, fileira in enumerate(sala2):
        status = ["L" if not assento else "O" for assento in fileira]
        print(f"Fileira {i}: {' '.join(status)}")

    melhor_fileira = encontrar_melhor_fileira(sala2, 3)
    print(
        f"Grupo de 3 pessoas: Fileira {melhor_fileira} (escolhida por ser a mais ao fundo)"
    )

    print("\n" + "=" * 50 + "\n")

    # Exemplo 3: Sala cheia
    print("Exemplo 3: Sala cheia")
    sala3 = [
        [True, True, True, True, True],
        [True, True, True, True, True],
        [True, True, True, True, True],
    ]

    print("Sala de cinema (todos os assentos ocupados):")
    for i, fileira in enumerate(sala3):
        status = ["O" for _ in fileira]
        print(f"Fileira {i}: {' '.join(status)}")

    melhor_fileira = encontrar_melhor_fileira(sala3, 2)
    print(
        f"Grupo de 2 pessoas: {'Nenhuma fileira adequada' if melhor_fileira == -1 else f'Fileira {melhor_fileira}'}"
    )

    print("\n" + "=" * 50 + "\n")

    # Exemplo 4: Sala vazia
    print("Exemplo 4: Sala vazia")
    sala4 = [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
    ]

    print("Sala de cinema (todos os assentos livres):")
    for i, fileira in enumerate(sala4):
        status = ["L" for _ in fileira]
        print(f"Fileira {i}: {' '.join(status)}")

    melhor_fileira = encontrar_melhor_fileira(sala4, 4)
    print(
        f"Grupo de 4 pessoas: Fileira {melhor_fileira} (escolhida por ser a mais ao fundo)"
    )


if __name__ == "__main__":
    main()
