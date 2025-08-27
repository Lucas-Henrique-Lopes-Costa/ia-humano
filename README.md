# Cinema - Gerenciamento de Assentos

Pacote Python para encontrar a melhor fileira de assentos em uma sala de cinema para um grupo de pessoas.

## Funcionalidades

- Encontrar a fileira com maior sequência consecutiva de assentos livres
- Considerar o tamanho do grupo
- Em caso de empate, preferir a fileira mais ao fundo da sala
- Validação de entradas

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar o pacote em modo desenvolvimento
pip install -e .
```

## Uso

```python
from cinema import encontrar_melhor_fileira

# Exemplo de sala de cinema
sala = [
    [False, False, True, False, False, False],  # Fileira 0
    [False, False, False, False, True, False],  # Fileira 1
    [True, False, False, True, False, False],   # Fileira 2
]

# Encontrar melhor fileira para grupo de 3 pessoas
melhor_fileira = encontrar_melhor_fileira(sala, 3)
print(f"Melhor fileira: {melhor_fileira}")
```

## Executar Exemplo

```bash
python exemplo_uso.py
```

## Testes

```bash
# Executar todos os testes
python -m pytest cinema/tests/ -v

# Executar testes com cobertura
python -m pytest cinema/tests/ --cov=cinema -v
```

## Estrutura do Projeto

```
cinema/
├── __init__.py              # Inicialização do pacote
├── cinema_manager.py        # Módulo principal com a lógica
└── tests/
    ├── __init__.py          # Inicialização dos testes
    └── test_cinema_manager.py  # Testes do módulo principal
```

## Casos de Teste

O pacote inclui testes abrangentes para:

- Fileira com maior sequência de assentos livres
- Empate (preferência pela fileira mais ao fundo)
- Nenhuma fileira adequada
- Entradas inválidas (tamanho zero/negativo)
- Sala vazia
- Fileira vazia
- Todos os assentos livres/ocupados
- Sequências no início/final da fileira
