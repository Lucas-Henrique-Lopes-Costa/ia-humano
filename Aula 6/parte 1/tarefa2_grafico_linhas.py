import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

    if len(df_filtrado) == 0:
        print("Nenhum registro encontrado para os cursos especificados.")
        return

    # Criar coluna de ano-mês para agrupamento
    df_filtrado = df_filtrado.copy()
    df_filtrado["ano_mes"] = df_filtrado["data_consumo"].dt.to_period("M")

    # Agrupar por curso e mês, contando as refeições
    consumo_mensal = (
        df_filtrado.groupby(["nome_curso", "ano_mes"])
        .size()
        .reset_index(name="quantidade_refeicoes")
    )

    # Converter período para string para compatibilidade com Plotly
    consumo_mensal["ano_mes_str"] = consumo_mensal["ano_mes"].astype(str)

    # Criar gráfico de linhas
    fig = px.line(
        consumo_mensal,
        x="ano_mes_str",
        y="quantidade_refeicoes",
        color="nome_curso",
        title="Consumo de Refeições por Mês - Ciência da Computação vs Sistemas de Informação",
        labels={
            "ano_mes_str": "Mês",
            "quantidade_refeicoes": "Quantidade de Refeições",
            "nome_curso": "Curso",
        },
    )

    # Personalizar o gráfico
    fig.update_layout(
        xaxis_title="Mês", yaxis_title="Quantidade de Refeições", hovermode="x unified"
    )

    fig.update_traces(mode="lines+markers")

    # Exibir o gráfico
    fig.show()

    # Mostrar estatísticas resumo
    print("\nEstatísticas por curso:")
    for curso in cursos_encontrados:
        dados_curso = consumo_mensal[consumo_mensal["nome_curso"] == curso]
        total = dados_curso["quantidade_refeicoes"].sum()
        media = dados_curso["quantidade_refeicoes"].mean()
        print(f"{curso}: Total = {total}, Média mensal = {media:.1f}")


if __name__ == "__main__":
    main()
