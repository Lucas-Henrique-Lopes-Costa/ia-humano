import pandas as pd


def test_totais_produtos():
    # Carregar o arquivo gerado pelo processamento
    df = pd.read_excel("vendas_totais.xlsx")
    # Valores esperados
    valores_esperados = {
        "P008": 17982.43,  # Cadeira Escritório
        "P010": 3699.33,  # HD Externo Seagate
        "P009": 22404.40,  # Headset JBL
        "P005": 3931.24,  # Impressora HP
        "P004": 28756.69,  # Monitor LG
        "P007": 25156.30,  # Mouse Gamer
        "P001": 19085.25,  # Notebook Dell
        "P002": 4438.86,  # Smartphone Samsung
        "P003": 5330.93,  # Tablet Apple
        "P006": 13751.35,  # Teclado Mecânico
    }
    resultados_dict = dict(zip(df["Código do Produto"], df["Total de Vendas"]))
    for codigo, valor_esperado in valores_esperados.items():
        valor_calculado = resultados_dict.get(codigo, 0)
        assert (
            abs(valor_calculado - valor_esperado) < 0.01
        ), f"Produto {codigo}: esperado {valor_esperado}, obtido {valor_calculado}"
