"""
Testes para o módulo cinema_manager.
"""

import pytest
from cinema.cinema_manager import encontrar_melhor_fileira


def test_fileira_com_sequencia_maior():
    """Testa quando uma fileira tem sequência maior de assentos livres"""
    sala = [
        [False, False, True, False, False, False],  # Fileira 0: 2 assentos consecutivos
        [False, False, False, False, True, False],  # Fileira 1: 4 assentos consecutivos
        [True, False, False, True, False, False],  # Fileira 2: 2 assentos consecutivos
    ]
    assert encontrar_melhor_fileira(sala, 3) == 1


def test_empate_prefere_fileira_mais_ao_fundo():
    """Testa quando há empate, prefere a fileira mais ao fundo"""
    sala = [
        [False, False, False, True, False, False],  # Fileira 0: 3 assentos consecutivos
        [True, False, False, False, True, False],  # Fileira 1: 3 assentos consecutivos
        [False, False, False, True, False, False],  # Fileira 2: 3 assentos consecutivos
    ]
    assert encontrar_melhor_fileira(sala, 3) == 2


def test_nenhuma_fileira_cabe_grupo():
    """Testa quando nenhuma fileira pode acomodar o grupo"""
    sala = [
        [True, False, False, True],  # Fileira 0: 2 assentos consecutivos
        [False, True, True, False],  # Fileira 1: 1 assento consecutivo
        [True, True, False, True],  # Fileira 2: 1 assento consecutivo
    ]
    assert encontrar_melhor_fileira(sala, 3) == -1


def test_grupo_tamanho_zero():
    """Testa com grupo de tamanho zero"""
    sala = [[False, False, False], [True, False, True]]
    assert encontrar_melhor_fileira(sala, 0) == -1


def test_grupo_tamanho_negativo():
    """Testa com grupo de tamanho negativo"""
    sala = [[False, False, False], [True, False, True]]
    assert encontrar_melhor_fileira(sala, -1) == -1


def test_sala_vazia():
    """Testa com sala vazia"""
    sala = []
    assert encontrar_melhor_fileira(sala, 2) == -1


def test_fileira_vazia():
    """Testa com fileira vazia"""
    sala = [[]]
    assert encontrar_melhor_fileira(sala, 1) == -1


def test_todos_assentos_livres():
    """Testa quando todos os assentos estão livres"""
    sala = [
        [False, False, False],  # Fileira 0: 3 assentos consecutivos
        [False, False, False],  # Fileira 1: 3 assentos consecutivos
    ]
    assert encontrar_melhor_fileira(sala, 3) == 1  # Prefere a última fileira


def test_todos_assentos_ocupados():
    """Testa quando todos os assentos estão ocupados"""
    sala = [[True, True, True], [True, True, True]]
    assert encontrar_melhor_fileira(sala, 2) == -1


def test_sequencia_no_final_da_fileira():
    """Testa sequência de assentos livres no final da fileira"""
    sala = [
        [True, False, False, False],  # Fileira 0: 3 assentos consecutivos no final
        [False, True, False, False],  # Fileira 1: 2 assentos consecutivos no final
    ]
    assert encontrar_melhor_fileira(sala, 3) == 0


def test_sequencia_no_inicio_da_fileira():
    """Testa sequência de assentos livres no início da fileira"""
    sala = [
        [False, False, False, True],  # Fileira 0: 3 assentos consecutivos no início
        [False, False, True, False],  # Fileira 1: 2 assentos consecutivos no início
    ]
    assert encontrar_melhor_fileira(sala, 3) == 0
