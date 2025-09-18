# Processamento de Vendas de Produtos

Este projeto contém um script Python para processar dados de vendas mensais de diferentes produtos, calcular o total de vendas por produto e gerar um relatório em Excel. Também inclui testes automatizados com pytest para validar os resultados.

## Como usar

1. **Processar os dados**

   Execute o script principal para gerar o arquivo de totais:

   ```bash
   python3 processar_vendas.py
   ```

   Isso irá ler o arquivo `vendas_produtos.xlsx` e criar o arquivo `vendas_totais.xlsx` com o total de vendas por produto.

2. **Testar os resultados**

   Os testes automatizados estão em `test_vendas.py` e usam o framework pytest. Para rodar os testes:

   ```bash
   pytest test_vendas.py
   ```

   O teste irá validar se os totais calculados correspondem aos valores esperados para cada produto.

## Estrutura dos arquivos

- `processar_vendas.py`: Script principal para processamento dos dados e geração do relatório.
- `test_vendas.py`: Testes automatizados para validação dos resultados usando pytest.
- `vendas_produtos.xlsx`: Arquivo de entrada com os dados de vendas mensais.
- `vendas_totais.xlsx`: Arquivo gerado com o total de vendas por produto.

## Requisitos

- Python 3
- pandas
- openpyxl
- pytest (para rodar os testes)

Instale as dependências com:

```bash
pip install -r requirements.txt
```
