"""
Módulo para gerenciamento de assentos em cinema.
"""


def encontrar_melhor_fileira(sala_cinema, tamanho_grupo):
    """
    Encontra a melhor fileira para um grupo se sentar no cinema.

    Args:
        sala_cinema (list): Matriz de booleanos onde cada lista representa uma fileira
                           True = assento ocupado, False = assento livre
        tamanho_grupo (int): Número de pessoas no grupo

    Returns:
        int: Número da fileira com maior sequência consecutiva de assentos livres
             -1 se não houver fileira que caiba todo o grupo
    """
    if tamanho_grupo <= 0:
        return -1

    melhor_fileira = -1
    maior_sequencia = 0

    for i, fileira in enumerate(sala_cinema):
        # Encontrar a maior sequência consecutiva de assentos livres nesta fileira
        sequencia_atual = 0
        maior_sequencia_fileira = 0

        for assento in fileira:
            if not assento:  # Assento livre
                sequencia_atual += 1
                maior_sequencia_fileira = max(maior_sequencia_fileira, sequencia_atual)
            else:  # Assento ocupado
                sequencia_atual = 0

        # Verificar se esta fileira pode acomodar o grupo
        if maior_sequencia_fileira >= tamanho_grupo:
            # Se é a primeira fileira válida ou tem sequência maior
            if melhor_fileira == -1 or maior_sequencia_fileira > maior_sequencia:
                melhor_fileira = i
                maior_sequencia = maior_sequencia_fileira
            # Em caso de empate, preferir a fileira mais ao fundo (maior índice)
            elif maior_sequencia_fileira == maior_sequencia and i > melhor_fileira:
                melhor_fileira = i

    return melhor_fileira
