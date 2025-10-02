import pandas as pd
from datetime import datetime


def main():
    # Leitura do arquivo CSV
    df = pd.read_csv("relacao_consumo_restaurante_universitario.csv")

    # Identificar e exibir as colunas disponíveis
    for i, coluna in enumerate(df.columns, 1):
        print(f"{i:2d}. {coluna}")

    # Identificar a coluna de data e analisar o período
    coluna_data = "data_consumo"

    df[coluna_data] = pd.to_datetime(df[coluna_data])

    data_inicial = df[coluna_data].min()
    data_final = df[coluna_data].max()
    total_refeicoes = len(df)

    print(f"Total de refeições: {total_refeicoes:,}")
    print(f"Data inicial: {data_inicial.strftime('%d/%m/%Y')}")
    print(f"Data final: {data_final.strftime('%d/%m/%Y')}")

    duracao = data_final - data_inicial
    print(f"Período total: {duracao.days:,} dias")
    print(f"Anos de dados: {duracao.days / 365.25:.1f} anos")


if __name__ == "__main__":
    main()
