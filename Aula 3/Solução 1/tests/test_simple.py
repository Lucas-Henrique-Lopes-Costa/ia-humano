#!/usr/bin/env python3
"""
Teste simples para verificar se a função está funcionando corretamente.
"""

import sys
import os

# Adiciona o diretório pai ao path para importar o módulo cinema_seats
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cinema_seats import encontrar_melhor_fileira

def test_basico():
    """Teste básico para verificar se a função funciona."""
    sala = [
        [False, False, True, False, False],  # Fileira 0: 2 assentos consecutivos
        [True, False, False, False, True],   # Fileira 1: 3 assentos consecutivos  
        [False, False, False, False, False]  # Fileira 2: 5 assentos consecutivos
    ]
    
    # Teste 1: Grupo de 3 pessoas
    resultado = encontrar_melhor_fileira(sala, 3)
    print(f"Grupo de 3 pessoas: Fileira {resultado} (esperado: 2)")
    assert resultado == 2
    
    # Teste 2: Grupo de 4 pessoas
    resultado = encontrar_melhor_fileira(sala, 4)
    print(f"Grupo de 4 pessoas: Fileira {resultado} (esperado: 2)")
    assert resultado == 2
    
    # Teste 3: Grupo de 6 pessoas
    resultado = encontrar_melhor_fileira(sala, 6)
    print(f"Grupo de 6 pessoas: Fileira {resultado} (esperado: -1)")
    assert resultado == -1
    
    print("Todos os testes básicos passaram!")

if __name__ == "__main__":
    test_basico()
