# Solução para Escolha de Fileira no Cinema

Este projeto implementa uma solução para encontrar a melhor fileira de cinema para um grupo se sentar junto, seguindo o ciclo completo de projeto de funções.

## Problema

Um grupo de pessoas quer escolher uma fileira de cadeiras no cinema que:
- Caiba todo o grupo sentado um ao lado do outro
- Tenha o maior número consecutivo de assentos livres (para maior conforto)
- Em caso de empate, prefira a última fileira (mais ao fundo da sala)

## Solução

A função `encontrar_melhor_fileira()` recebe:
- Uma matriz de booleanos representando a sala de cinema
- O tamanho do grupo

E retorna:
- O número da fileira escolhida (0-indexed)
- -1 se nenhuma fileira couber o grupo

## Estrutura do Projeto

```
.
├── cinema_seats.py          # Implementação principal da função
├── tests/                   # Pasta com todos os testes
│   ├── __init__.py         # Torna tests um módulo Python
│   ├── test_cinema_seats.py # Testes abrangentes usando pytest
│   └── test_simple.py      # Teste básico para verificação inicial
├── exemplo_uso.py          # Exemplos práticos de uso da função
├── pytest.ini             # Configuração do pytest
├── requirements.txt        # Dependências do projeto
└── README.md              # Esta documentação
```

## Como Usar

### Instalação

```bash
pip install -r requirements.txt
```

### Execução dos Testes

```bash
# Executar todos os testes
python -m pytest

# Executar testes específicos
python -m pytest tests/test_cinema_seats.py -v

# Executar teste básico
python tests/test_simple.py

# Executar exemplo de uso
python exemplo_uso.py
```

### Exemplo de Uso

```python
from cinema_seats import encontrar_melhor_fileira

# Sala de cinema (True = ocupado, False = livre)
sala = [
    [False, False, True, False, False],  # Fileira 0
    [True, False, False, False, True],   # Fileira 1
    [False, False, False, False, False]  # Fileira 2
]

# Encontrar melhor fileira para grupo de 3 pessoas
melhor_fileira = encontrar_melhor_fileira(sala, 3)
print(f"Melhor fileira: {melhor_fileira}")  # Saída: 2
```

## Casos de Teste Implementados

O projeto inclui testes abrangentes cobrindo:

1. **Fileira com mais assentos consecutivos** - Uma fileira com mais assentos livres consecutivos que todas as outras
2. **Espaços não consecutivos** - Fileira com dois espaços não consecutivos suficientes para todo o grupo
3. **Assentos exatos** - Fileira com assentos livres do mesmo tamanho do grupo
4. **Múltiplas fileiras sem empate** - Mais de uma fileira adequada, sem empates
5. **Múltiplas fileiras com empate** - Mais de uma fileira adequada, com empates
6. **Nenhuma fileira suficiente** - Fileiras com assentos consecutivos, mas insuficientes
7. **Fileira totalmente livre** - Uma fileira com todos os assentos livres
8. **Sala cheia** - Sala de cinema com todos os assentos ocupados
9. **Sala vazia** - Sala de cinema com todos os assentos livres
10. **Fileiras pequenas** - Fileiras menores que o tamanho do grupo

### Casos de Borda Adicionais

- Sala vazia ou fileiras vazias
- Tamanho do grupo zero ou negativo
- Tamanho do grupo maior que qualquer fileira
- Sequências de assentos livres no início, meio ou final da fileira
- Empates complexos com múltiplas fileiras
- Múltiplas sequências na mesma fileira

## Ciclo de Projeto de Funções

Este projeto segue o ciclo completo de projeto de funções:

1. **Análise do Problema** - Compreensão dos requisitos
2. **Especificação** - Documentação clara da função
3. **Projeto da Solução** - Planejamento da implementação
4. **Implementação** - Código da função
5. **Escrita de Testes** - Testes abrangentes com pytest
6. **Verificação** - Execução e validação dos testes
7. **Validação** - Confirmação de que todos os casos estão cobertos
8. **Documentação** - Documentação completa do projeto

## Algoritmo

A função implementa o seguinte algoritmo:

1. Validação de entrada (sala vazia, tamanho do grupo inválido)
2. Para cada fileira:
   - Conta a maior sequência de assentos consecutivos livres
   - Verifica se pode acomodar o grupo
   - Atualiza a melhor fileira se necessário (mais assentos ou empate resolvido pela posição)
3. Retorna a melhor fileira encontrada ou -1

## Complexidade

- **Tempo**: O(n × m), onde n é o número de fileiras e m é o número de assentos por fileira
- **Espaço**: O(1), usando apenas variáveis auxiliares
