# Sistema de Testes para Função de Futebol

Este projeto demonstra como criar testes para funções que processam arquivos, usando dados artificiais para garantir que os testes sejam rápidos, isolados e reprodutíveis.

## Estrutura do Projeto

```
.
├── futebol.py                    # Arquivo principal com a função calcular_quantidade_gols
├── exemplo_uso.py                # Exemplo prático de uso da função
├── testes/
│   ├── dados/
│   │   └── futebol.csv          # Dados artificiais para testes
│   └── test_futebol.py          # Arquivo de testes
└── README.md                     # Este arquivo
```

## Função Principal

A função `calcular_quantidade_gols(dados, pais)` calcula a quantidade de gols feitos por jogadores de um país específico em cada liga.

### Parâmetros

- `dados`: Lista de listas contendo dados de futebol
- `pais`: Identificação do país (ex.: "br BRA")

### Retorno

- Dicionário com ligas como chaves e total de gols como valores

## Dados de Teste

O arquivo `futebol.csv` contém dados artificiais que cobrem todos os casos de teste:

1. **Brasil (br BRA)**: 5 jogadores na Serie A (15+8+12+0+5 = 40 gols)
2. **Portugal (pt POR)**: 3 jogadores na Primeira Liga (18+6+11 = 35 gols)
3. **Espanha (es ESP)**: 1 jogador na La Liga (20 gols)
4. **Argentina (ar ARG)**: 1 jogador na Primera Division (14 gols)

## Casos de Teste Cobertos

- ✅ País aparece várias vezes em linhas não consecutivas
- ✅ País aparece em linhas consecutivas
- ✅ País aparece apenas uma vez
- ✅ País aparece em apenas uma liga
- ✅ País aparece várias vezes mas alguns jogadores não fizeram gols
- ✅ País não aparece no arquivo
- ✅ País com um jogador por liga
- ✅ Estrutura de dados correta
- ✅ Cálculo correto dos gols

## Como Executar

### Executar a função principal

```bash
python futebol.py
```

### Executar o exemplo de uso

```bash
python exemplo_uso.py
```

### Executar os testes

```bash
python -m pytest testes/test_futebol.py -v
```

Ou usando unittest:

```bash
python testes/test_futebol.py
```

## Vantagens desta Abordagem

1. **Rápido**: Testes executam em milissegundos
2. **Isolado**: Não depende de arquivos externos ou internet
3. **Reprodutível**: Sempre produz os mesmos resultados
4. **Controlado**: Podemos criar cenários específicos para testar
5. **Casos de Borda**: Podemos incluir situações que podem não existir em dados reais

## Por que não usar o arquivo original do Kaggle?

- **Tamanho**: Arquivos grandes tornam testes lentos
- **Disponibilidade**: Arquivo pode não estar acessível
- **Mudanças**: Conteúdo pode ser alterado, quebrando testes
- **Casos de Borda**: Dados reais podem não cobrir todos os cenários
- **Dependências**: Testes ficam acoplados a fontes externas
