import pandas as pd
import plotly.express as px


def main():
    # Carregar dados
    df = pd.read_csv("relacao_consumo_restaurante_universitario.csv")

    # Converter data_consumo para datetime
    df["data_consumo"] = pd.to_datetime(df["data_consumo"])

    # Filtrar apenas estudantes (tipo_usuario contém "Aluno")
    df_alunos = df[df["tipo_usuario"].str.contains("Aluno", na=False)]

    # Filtrar apenas os cursos de interesse
    cursos_interesse = ["Ciência da Computação", "Sistemas de Informação"]
    df_filtrado = df_alunos[df_alunos["nome_curso"].isin(cursos_interesse)]

    # Verificar se existem dados para os cursos
    cursos_encontrados = df_filtrado["nome_curso"].unique()
    print(f"Cursos encontrados: {list(cursos_encontrados)}")

    if len(df_filtrado) == 0:
        print("Nenhum registro encontrado para os cursos especificados.")
        return

    # Agrupar por cidade de nascimento e contar refeições
    consumo_por_cidade = (
        df_filtrado.groupby("cidade_nascimento")
        .size()
        .reset_index(name="quantidade_refeicoes")
    )

    # Ordenar por quantidade de refeições (decrescente)
    consumo_por_cidade = consumo_por_cidade.sort_values(
        "quantidade_refeicoes", ascending=False
    )

    print(f"Total de cidades diferentes: {len(consumo_por_cidade)}")
    print("\nTop 10 cidades com mais refeições:")
    print(consumo_por_cidade.head(10))

    # Criar gráfico de colunas
    fig = px.bar(
        consumo_por_cidade,
        x="cidade_nascimento",
        y="quantidade_refeicoes",
        title="Consumo de Refeições por Cidade de Nascimento - Ciência da Computação e Sistemas de Informação",
        labels={
            "cidade_nascimento": "Cidade de Nascimento",
            "quantidade_refeicoes": "Quantidade de Refeições",
        },
    )

    # Personalizar o gráfico
    fig.update_layout(
        xaxis_title="Cidade de Nascimento",
        yaxis_title="Quantidade de Refeições",
        xaxis_tickangle=-45,
        height=600,
    )

    # Exibir o gráfico
    fig.show()

    # Mostrar estatísticas resumo
    print(f"\nEstatísticas gerais:")
    print(f"Total de refeições: {consumo_por_cidade['quantidade_refeicoes'].sum()}")
    print(f"Média por cidade: {consumo_por_cidade['quantidade_refeicoes'].mean():.1f}")
    print(
        f"Cidade com mais refeições: {consumo_por_cidade.iloc[0]['cidade_nascimento']} ({consumo_por_cidade.iloc[0]['quantidade_refeicoes']} refeições)"
    )


if __name__ == "__main__":
    main()
