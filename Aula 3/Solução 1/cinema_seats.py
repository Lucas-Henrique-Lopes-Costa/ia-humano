"""
Módulo para encontrar a melhor fileira de cinema para um grupo se sentar junto.

Este módulo contém uma função que analisa a disponibilidade de assentos em uma sala de cinema
e encontra a fileira ideal para um grupo se sentar junto, considerando a maior quantidade
de assentos consecutivos livres.
"""

def encontrar_melhor_fileira(sala_cinema, tamanho_grupo):
    """
    Encontra a melhor fileira de cinema para um grupo se sentar junto.
    
    A função analisa todas as fileiras da sala e retorna o número da fileira que:
    - Tem pelo menos 'tamanho_grupo' assentos consecutivos livres
    - Entre as fileiras que atendem ao critério acima, escolhe a que tem mais assentos consecutivos livres
    - Em caso de empate, escolhe a fileira mais ao fundo (maior índice)
    
    Args:
        sala_cinema (list): Lista de listas de booleanos representando a sala de cinema.
                           Cada lista interna representa uma fileira, onde True = ocupado, False = livre.
                           A primeira fileira tem índice 0.
        tamanho_grupo (int): Número de pessoas no grupo que precisam se sentar juntos.
    
    Returns:
        int: Número da fileira escolhida (0-indexed), ou -1 se nenhuma fileira couber o grupo.
    
    Examples:
        >>> sala = [[False, False, True, False, False],  # Fileira 0: 2 assentos consecutivos
        ...         [True, False, False, False, True],   # Fileira 1: 3 assentos consecutivos
        ...         [False, False, False, False, False]] # Fileira 2: 5 assentos consecutivos
        >>> encontrar_melhor_fileira(sala, 3)
        2
        >>> encontrar_melhor_fileira(sala, 4)
        2
        >>> encontrar_melhor_fileira(sala, 6)
        -1
    """
    if not sala_cinema or tamanho_grupo <= 0:
        return -1
    
    melhor_fileira = -1
    max_consecutivos = 0
    
    for i, fileira in enumerate(sala_cinema):
        if not fileira:  # Fileira vazia
            continue
            
        # Encontrar a maior sequência de assentos consecutivos livres
        max_atual = 0
        contador_atual = 0
        
        for assento in fileira:
            if not assento:  # Assento livre
                contador_atual += 1
            else:  # Assento ocupado
                max_atual = max(max_atual, contador_atual)
                contador_atual = 0
        
        # Verificar se há uma sequência no final da fileira
        max_atual = max(max_atual, contador_atual)
        
        # Verificar se esta fileira pode acomodar o grupo
        if max_atual >= tamanho_grupo:
            # Se tem mais assentos consecutivos que a melhor até agora, ou
            # se tem a mesma quantidade mas é uma fileira mais ao fundo
            if max_atual > max_consecutivos or (max_atual == max_consecutivos and i > melhor_fileira):
                melhor_fileira = i
                max_consecutivos = max_atual
    
    return melhor_fileira
