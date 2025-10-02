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

        # Identificar colunas necessárias
        coluna_municipio = None
        coluna_populacao = None
        coluna_pib_per_capita = None
        coluna_mortalidade = None
        coluna_escolarizacao = None

        # Buscar coluna do município
        for col in df.columns:
            if "munic" in str(col).lower() or "nome" in str(col).lower():
                coluna_municipio = col
                break
        if not coluna_municipio:
            coluna_municipio = df.columns[0]

        # Buscar coluna de população
        for col in df.columns:
            if "população" in str(col).lower() or "pop" in str(col).lower():
                coluna_populacao = col
                break

        # Buscar coluna de PIB per capita
        for col in df.columns:
            if "pib" in str(col).lower() and "per" in str(col).lower():
                coluna_pib_per_capita = col
                break
            elif "pib" in str(col).lower() and "capita" in str(col).lower():
                coluna_pib_per_capita = col
                break

        # Buscar coluna de mortalidade infantil
        for col in df.columns:
            if "mortalidade" in str(col).lower() and "infantil" in str(col).lower():
                coluna_mortalidade = col
                break
            elif "mortalidade" in str(col).lower():
                coluna_mortalidade = col
                break

        # Buscar coluna de escolarização
        for col in df.columns:
            if "escolar" in str(col).lower():
                coluna_escolarizacao = col
                break
            elif "educação" in str(col).lower():
                coluna_escolarizacao = col
                break

        # Verificar se todas as colunas foram encontradas
        colunas_necessarias = {
            "Município": coluna_municipio,
            "População": coluna_populacao,
            "PIB per capita": coluna_pib_per_capita,
            "Mortalidade infantil": coluna_mortalidade,
            "Escolarização": coluna_escolarizacao,
        }

        print(f"\nColunas identificadas:")
        for nome, coluna in colunas_necessarias.items():
            print(f"{nome}: {coluna if coluna else 'NÃO ENCONTRADA'}")

        colunas_faltantes = [
            nome for nome, coluna in colunas_necessarias.items() if coluna is None
        ]
        if colunas_faltantes:
            print(f"\nERRO: Colunas não encontradas: {', '.join(colunas_faltantes)}")
            print("Verifique se o arquivo contém as colunas necessárias.")
            return

        # Limpar e converter dados
        colunas_numericas = [
            coluna_populacao,
            coluna_pib_per_capita,
            coluna_mortalidade,
            coluna_escolarizacao,
        ]
        for col in colunas_numericas:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Remover linhas com valores nulos
        df_limpo = df.dropna(subset=colunas_numericas)
        print(f"\nRegistros após limpeza: {len(df_limpo)}")

        # Selecionar os 40 municípios mais populosos
        top40 = df_limpo.nlargest(40, coluna_populacao)

        print(f"\n40 municípios mais populosos selecionados:")
        for i, (idx, row) in enumerate(top40.head(10).iterrows(), 1):
            print(f"{i:2d}. {row[coluna_municipio]}: {row[coluna_populacao]:,.0f} hab")
        print("...")

        # Criar gráfico de dispersão
        fig = px.scatter(
            top40,
            x=coluna_pib_per_capita,
            y=coluna_populacao,
            size=coluna_mortalidade,
            color=coluna_escolarizacao,
            hover_name=coluna_municipio,
            title="Relação entre PIB per capita, População, Mortalidade Infantil e Escolarização - 40 Maiores Municípios de MG",
            labels={
                coluna_pib_per_capita: "PIB per capita (R$)",
                coluna_populacao: "População Estimada",
                coluna_mortalidade: "Mortalidade Infantil",
                coluna_escolarizacao: "Nível de Escolarização",
            },
        )

        # Personalizar o gráfico
        fig.update_layout(
            xaxis_title="PIB per capita (R$)",
            yaxis_title="População Estimada",
            height=700,
            width=1000,
        )

        # Exibir o gráfico
        fig.show()

        # Estatísticas resumo
        print(f"\nEstatísticas dos 40 municípios:")
        print(f"PIB per capita médio: R$ {top40[coluna_pib_per_capita].mean():,.2f}")
        print(f"População média: {top40[coluna_populacao].mean():,.0f} habitantes")
        print(f"Mortalidade infantil média: {top40[coluna_mortalidade].mean():.2f}")
        print(f"Escolarização média: {top40[coluna_escolarizacao].mean():.2f}")

    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        print("Verifique se o arquivo Excel está no formato correto.")


if __name__ == "__main__":
    main()
