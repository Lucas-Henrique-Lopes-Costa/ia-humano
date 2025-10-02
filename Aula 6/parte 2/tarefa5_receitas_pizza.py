import pandas as pd
import plotly.express as px


def main():
    try:
        # Tentar carregar o arquivo Excel
        print("Carregando dados dos municípios de Minas Gerais...")

        df = pd.read_excel("municipios-mg.xlsx", header=1)
        # Usar a primeira linha como nomes de coluna
        df.columns = df.iloc[0]
        df = df.drop(df.index[0]).reset_index(drop=True)
        print("Arquivo municipios-mg.xlsx carregado com sucesso")

        print("Colunas disponíveis:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")

        # Identificar coluna de receitas 2024
        colunas_receita = [
            col
            for col in df.columns
            if "2024" in str(col) and "receita" in str(col).lower()
        ]
        if not colunas_receita:
            colunas_receita = [
                col for col in df.columns if "receita" in str(col).lower()
            ]

        if not colunas_receita:
            print("ERRO: Coluna de receitas não encontrada.")
            print("Verifique se existe uma coluna com 'receita' no nome.")
            return

        coluna_receita = colunas_receita[0]
        print(f"Usando coluna de receitas: {coluna_receita}")

        # Identificar coluna de nome do município
        colunas_municipio = [
            col
            for col in df.columns
            if "munic" in str(col).lower() or "nome" in str(col).lower()
        ]
        if not colunas_municipio:
            coluna_municipio = df.columns[0]
        else:
            coluna_municipio = colunas_municipio[0]

        print(f"Usando coluna de município: {coluna_municipio}")

        # Municípios do sul de MG de interesse
        municipios_sul = [
            "Poços de Caldas",
            "Pouso Alegre",
            "Varginha",
            "Passos",
            "Lavras",
        ]

        # Filtrar os municípios do sul de MG
        df_sul = df[df[coluna_municipio].isin(municipios_sul)].copy()

        if len(df_sul) == 0:
            print("ERRO: Nenhum dos municípios especificados foi encontrado.")
            print("Municípios procurados:", municipios_sul)
            print("Verifique se os nomes estão corretos no arquivo.")
            return

        print(f"Municípios encontrados: {len(df_sul)}")

        # Converter receitas para numérico
        df_sul[coluna_receita] = pd.to_numeric(df_sul[coluna_receita], errors="coerce")
        df_sul = df_sul.dropna(subset=[coluna_receita])

        print("\nReceitas 2024 dos municípios do sul de MG:")
        for idx, row in df_sul.iterrows():
            print(f"{row[coluna_municipio]}: R$ {row[coluna_receita]:,.2f}")

        # Criar gráfico de pizza
        fig = px.pie(
            df_sul,
            values=coluna_receita,
            names=coluna_municipio,
            title="Proporção das Receitas 2024 - 5 Maiores Municípios do Sul de MG",
        )

        # Personalizar o gráfico
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(height=600)

        # Exibir o gráfico
        fig.show()

        # Estatísticas
        total_receitas = df_sul[coluna_receita].sum()
        print(f"\nTotal de receitas dos 5 municípios: R$ {total_receitas:,.2f}")
        print("Participação percentual:")
        for idx, row in df_sul.iterrows():
            percentual = (row[coluna_receita] / total_receitas) * 100
            print(f"{row[coluna_municipio]}: {percentual:.1f}%")

    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        print("Verifique se o arquivo Excel está no formato correto.")


if __name__ == "__main__":
    main()
