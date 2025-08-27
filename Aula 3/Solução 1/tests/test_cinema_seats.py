#!/usr/bin/env python3
"""
Testes abrangentes para a função encontrar_melhor_fileira usando pytest.

Este módulo testa todos os casos de uso comuns e casos de borda para garantir
que a função funciona corretamente em todas as situações.
"""

import pytest
import sys
import os

# Adiciona o diretório pai ao path para importar o módulo cinema_seats
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cinema_seats import encontrar_melhor_fileira


class TestEncontrarMelhorFileira:
    """Classe de testes para a função encontrar_melhor_fileira."""
    
    def test_caso_1_fileira_com_mais_assentos_consecutivos(self):
        """Teste 1: Uma fileira com mais assentos livres consecutivos que todas as outras."""
        sala = [
            [False, False, True, False, False],  # Fileira 0: 2 assentos consecutivos
            [True, False, False, False, True],   # Fileira 1: 3 assentos consecutivos
            [False, False, False, False, False]  # Fileira 2: 5 assentos consecutivos
        ]
        assert encontrar_melhor_fileira(sala, 3) == 2
        assert encontrar_melhor_fileira(sala, 4) == 2
        assert encontrar_melhor_fileira(sala, 5) == 2
    
    def test_caso_2_dois_espacos_nao_consecutivos(self):
        """Teste 2: Fileira com dois espaços não consecutivos suficientes para todo o grupo."""
        sala = [
            [False, False, True, False, False, True, False, False]  # 2+2 assentos, mas não consecutivos
        ]
        # Não deve encontrar solução pois não há 3 assentos consecutivos
        assert encontrar_melhor_fileira(sala, 3) == -1
        # Mas deve encontrar para grupos menores
        assert encontrar_melhor_fileira(sala, 2) == 0
    
    def test_caso_3_assentos_livres_do_mesmo_tamanho_do_grupo(self):
        """Teste 3: Fileira com assentos livres do mesmo tamanho do grupo."""
        sala = [
            [True, False, False, False, True],   # Fileira 0: exatamente 3 assentos consecutivos
            [False, False, False, True, True]    # Fileira 1: exatamente 3 assentos consecutivos
        ]
        assert encontrar_melhor_fileira(sala, 3) == 1  # Deve escolher a última fileira em caso de empate
    
    def test_caso_4_multiplas_fileiras_sem_empate(self):
        """Teste 4: Mais de uma fileira com mais assentos livres consecutivos que o tamanho do grupo, sem empates."""
        sala = [
            [False, False, True, False, False],  # Fileira 0: 2 assentos consecutivos
            [True, False, False, False, False],  # Fileira 1: 4 assentos consecutivos
            [False, False, False, False, False]  # Fileira 2: 5 assentos consecutivos
        ]
        assert encontrar_melhor_fileira(sala, 3) == 2  # Fileira 2 tem mais assentos consecutivos
    
    def test_caso_5_multiplas_fileiras_com_empate(self):
        """Teste 5: Mais de uma fileira com mais assentos livres consecutivos que o tamanho do grupo, com empates."""
        sala = [
            [False, False, False, True, False],  # Fileira 0: 3 assentos consecutivos
            [True, False, False, False, True],   # Fileira 1: 3 assentos consecutivos
            [False, False, False, True, False]   # Fileira 2: 3 assentos consecutivos
        ]
        assert encontrar_melhor_fileira(sala, 3) == 2  # Deve escolher a última fileira em caso de empate
    
    def test_caso_6_nenhuma_fileira_suficiente(self):
        """Teste 6: Mais de uma fileira com assentos consecutivos livres, mas nenhuma suficiente para todo o grupo."""
        sala = [
            [False, False, True, False, False],  # Fileira 0: 2 assentos consecutivos
            [True, False, False, True, False],   # Fileira 1: 2 assentos consecutivos
            [False, False, True, False, False]   # Fileira 2: 2 assentos consecutivos
        ]
        assert encontrar_melhor_fileira(sala, 3) == -1  # Nenhuma fileira tem 3 assentos consecutivos
    
    def test_caso_7_fileira_com_todos_assentos_livres(self):
        """Teste 7: Uma fileira com todos os assentos livres e suficientes para o tamanho do grupo."""
        sala = [
            [True, True, True, True, True],      # Fileira 0: todos ocupados
            [False, False, False, False, False], # Fileira 1: todos livres
            [True, False, True, False, True]     # Fileira 2: alguns livres
        ]
        assert encontrar_melhor_fileira(sala, 5) == 1  # Fileira 1 tem 5 assentos consecutivos
        assert encontrar_melhor_fileira(sala, 3) == 1  # Fileira 1 tem 5 assentos consecutivos
    
    def test_caso_8_sala_cheia(self):
        """Teste 8: Uma sala de cinema cheia, com todos os assentos ocupados."""
        sala = [
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True]
        ]
        assert encontrar_melhor_fileira(sala, 1) == -1  # Nenhum assento livre
        assert encontrar_melhor_fileira(sala, 3) == -1  # Nenhum assento livre
    
    def test_caso_9_sala_vazia(self):
        """Teste 9: Uma sala de cinema vazia, com todos os assentos livres."""
        sala = [
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False]
        ]
        assert encontrar_melhor_fileira(sala, 5) == 2  # Deve escolher a última fileira
        assert encontrar_melhor_fileira(sala, 3) == 2  # Deve escolher a última fileira
    
    def test_caso_10_fileiras_menores_que_grupo(self):
        """Teste 10: Uma sala de cinema cujas fileiras são menores que o tamanho do grupo."""
        sala = [
            [False, False],  # Fileira 0: 2 assentos
            [False, False],  # Fileira 1: 2 assentos
            [False, False]   # Fileira 2: 2 assentos
        ]
        assert encontrar_melhor_fileira(sala, 3) == -1  # Nenhuma fileira tem 3 assentos
        assert encontrar_melhor_fileira(sala, 2) == 2   # Todas têm 2 assentos, escolhe a última
    
    def test_casos_borda_adicionais(self):
        """Testes para casos de borda adicionais."""
        
        # Sala vazia
        assert encontrar_melhor_fileira([], 1) == -1
        
        # Fileira vazia
        assert encontrar_melhor_fileira([[]], 1) == -1
        
        # Tamanho do grupo zero ou negativo
        sala = [[False, False, False]]
        assert encontrar_melhor_fileira(sala, 0) == -1
        assert encontrar_melhor_fileira(sala, -1) == -1
        
        # Tamanho do grupo maior que qualquer fileira
        sala = [[False, False], [False, False, False]]
        assert encontrar_melhor_fileira(sala, 4) == -1
        
        # Sequência no final da fileira
        sala = [[True, False, False, False]]  # 3 assentos consecutivos no final
        assert encontrar_melhor_fileira(sala, 3) == 0
        
        # Sequência no início da fileira
        sala = [[False, False, False, True]]  # 3 assentos consecutivos no início
        assert encontrar_melhor_fileira(sala, 3) == 0
        
        # Sequência no meio da fileira
        sala = [[True, False, False, False, True]]  # 3 assentos consecutivos no meio
        assert encontrar_melhor_fileira(sala, 3) == 0
    
    def test_empate_complexo(self):
        """Teste para empate complexo com múltiplas fileiras."""
        sala = [
            [False, False, False, True, False, False, False],  # Fileira 0: 3 assentos consecutivos
            [True, False, False, False, True, False, False],   # Fileira 1: 3 assentos consecutivos
            [False, False, False, True, False, False, False],  # Fileira 2: 3 assentos consecutivos
            [True, False, False, False, True, False, False]    # Fileira 3: 3 assentos consecutivos
        ]
        assert encontrar_melhor_fileira(sala, 3) == 3  # Deve escolher a última fileira
    
    def test_sequencias_multiplas_na_mesma_fileira(self):
        """Teste para fileira com múltiplas sequências de assentos livres."""
        sala = [
            [False, False, True, False, False, False, True, False, False]  # 2 + 3 + 2 assentos consecutivos
        ]
        assert encontrar_melhor_fileira(sala, 3) == 0  # Deve encontrar a sequência de 3
        assert encontrar_melhor_fileira(sala, 4) == -1  # Nenhuma sequência tem 4 assentos
        assert encontrar_melhor_fileira(sala, 2) == 0   # Deve encontrar a sequência de 3 (maior)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
