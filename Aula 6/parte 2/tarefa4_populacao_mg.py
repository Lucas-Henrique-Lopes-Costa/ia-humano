import pandas as pd
import plotly.express as px


def main():
    try:
        # Dados
        df = pd.read_excel("municipios-mg.xlsx", header=1)

        # Usar a primeira linha como nomes de coluna
        df.columns = df.iloc[0]
        df = df.drop(df.index[0]).reset_index(drop=True)

        print(f"Total de registros: {len(df)}")
        print("Colunas disponíveis:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")

        # Identificar coluna de população 2025
        colunas_populacao = [
            col
            for col in df.columns
            if "2025" in str(col) and "pop" in str(col).lower()
        ]
        if not colunas_populacao:
            colunas_populacao = [
                col for col in df.columns if "população" in str(col).lower()
            ]

        if not colunas_populacao:
            print("ERRO: Coluna de população não encontrada.")
            print("Verifique se existe uma coluna com 'população' ou '2025' no nome.")
            return

        coluna_populacao = colunas_populacao[0]
        print(f"Usando coluna de população: {coluna_populacao}")

        # Identificar coluna de nome do município
        colunas_municipio = [
            col
            for col in df.columns
            if "munic" in str(col).lower() or "nome" in str(col).lower()
        ]
        if not colunas_municipio:
            coluna_municipio = df.columns[0]  # Primeira coluna como fallback
        else:
            coluna_municipio = colunas_municipio[0]

        print(f"Usando coluna de município: {coluna_municipio}")

        # Limpar dados e converter população para numérico
        df[coluna_populacao] = pd.to_numeric(df[coluna_populacao], errors="coerce")
        df = df.dropna(subset=[coluna_populacao])

        # Selecionar os 20 municípios mais populosos
        top20 = df.nlargest(20, coluna_populacao)

        print("\n20 municípios mais populosos:")
        for i, (idx, row) in enumerate(top20.iterrows(), 1):
            print(
                f"{i:2d}. {row[coluna_municipio]}: {row[coluna_populacao]:,.0f} habitantes"
            )

        # Criar gráfico de colunas
        fig = px.bar(
            top20,
            x=coluna_municipio,
            y=coluna_populacao,
            title="População Estimada 2025 - 20 Municípios Mais Populosos de MG",
            labels={
                coluna_municipio: "Município",
                coluna_populacao: "População Estimada 2025",
            },
        )

        # Personalizar o gráfico
        fig.update_layout(
            xaxis_title="Município",
            yaxis_title="População Estimada 2025",
            xaxis_tickangle=-45,
            height=600,
        )

        fig.update_traces(texttemplate="%{y:,.0f}", textposition="outside")

        # Exibir o gráfico
        fig.show()

    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        print("Verifique se o arquivo Excel está no formato correto.")


if __name__ == "__main__":
    main()
