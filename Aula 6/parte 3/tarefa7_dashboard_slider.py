import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Inicializar a aplicação Dash
app = dash.Dash(__name__)


# Função para carregar dados
def carregar_dados():
    try:
        df = pd.read_excel("municipios-mg.xlsx", header=1)
        # Usar a primeira linha como nomes de coluna
        df.columns = df.iloc[0]
        df = df.drop(df.index[0]).reset_index(drop=True)
        print("Arquivo municipios-mg.xlsx carregado com sucesso")
        return df
    except FileNotFoundError:
        print("ERRO: Arquivo municipios-mg.xlsx não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None


# Função para identificar colunas
def identificar_colunas(df):
    if df is None:
        return None, None, None, None, None

    coluna_municipio = None
    coluna_populacao = None
    coluna_pib_per_capita = None
    coluna_mortalidade = None
    coluna_escolarizacao = None

    # Buscar colunas
    for col in df.columns:
        if "munic" in str(col).lower() or "nome" in str(col).lower():
            coluna_municipio = col
        elif "população" in str(col).lower() or "pop" in str(col).lower():
            coluna_populacao = col
        elif "pib" in str(col).lower() and (
            "per" in str(col).lower() or "capita" in str(col).lower()
        ):
            coluna_pib_per_capita = col
        elif "mortalidade" in str(col).lower():
            coluna_mortalidade = col
        elif "escolar" in str(col).lower() or "educação" in str(col).lower():
            coluna_escolarizacao = col

    if not coluna_municipio:
        coluna_municipio = df.columns[0]

    return (
        coluna_municipio,
        coluna_populacao,
        coluna_pib_per_capita,
        coluna_mortalidade,
        coluna_escolarizacao,
    )


# Carregar dados globalmente
df_global = carregar_dados()
if df_global is not None:
    # Identificar colunas
    col_municipio, col_populacao, col_pib, col_mortalidade, col_escolarizacao = (
        identificar_colunas(df_global)
    )

    # Limpar dados
    if all([col_municipio, col_populacao, col_pib, col_mortalidade, col_escolarizacao]):
        colunas_numericas = [col_populacao, col_pib, col_mortalidade, col_escolarizacao]
        for col in colunas_numericas:
            df_global[col] = pd.to_numeric(df_global[col], errors="coerce")

        df_global = df_global.dropna(subset=colunas_numericas)
        df_global = df_global.sort_values(col_populacao, ascending=False)

# Layout da aplicação
app.layout = html.Div(
    [
        html.H1(
            "Dashboard Interativo - Municípios de Minas Gerais",
            style={"textAlign": "center", "marginBottom": 30},
        ),
        html.Div(
            [
                html.Label("Número de Municípios:", style={"fontWeight": "bold"}),
                dcc.Slider(
                    id="slider-municipios",
                    min=10,
                    max=100,
                    step=5,
                    value=40,
                    marks={i: str(i) for i in range(10, 101, 10)},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
            style={"margin": "20px"},
        ),
        dcc.Graph(id="grafico-dispersao"),
        html.Div(id="info-municipios", style={"margin": "20px", "textAlign": "center"}),
    ]
)


# Callback para atualizar o gráfico
@app.callback(
    [Output("grafico-dispersao", "figure"), Output("info-municipios", "children")],
    [Input("slider-municipios", "value")],
)
def atualizar_grafico(num_municipios):
    if df_global is None:
        fig = px.scatter(title="Erro: Arquivo de dados não encontrado")
        info = "Por favor, adicione o arquivo Excel com dados dos municípios de MG."
        return fig, info

    if not all(
        [col_municipio, col_populacao, col_pib, col_mortalidade, col_escolarizacao]
    ):
        fig = px.scatter(title="Erro: Colunas necessárias não encontradas")
        info = "Verifique se o arquivo contém as colunas necessárias."
        return fig, info

    # Selecionar top N municípios
    df_top = df_global.head(num_municipios)

    # Criar gráfico de dispersão
    fig = px.scatter(
        df_top,
        x=col_pib,
        y=col_populacao,
        size=col_mortalidade,
        color=col_escolarizacao,
        hover_name=col_municipio,
        title=f"Relação entre PIB per capita, População, Mortalidade e Escolarização - {num_municipios} Maiores Municípios de MG",
        labels={
            col_pib: "PIB per capita (R$)",
            col_populacao: "População Estimada",
            col_mortalidade: "Mortalidade Infantil",
            col_escolarizacao: "Nível de Escolarização",
        },
    )

    fig.update_layout(
        height=600, xaxis_title="PIB per capita (R$)", yaxis_title="População Estimada"
    )

    # Informações
    info = f"Exibindo {num_municipios} municípios mais populosos de Minas Gerais"

    return fig, info


if __name__ == "__main__":
    print("Acesse: http://127.0.0.1:8050")
    app.run(debug=True)
