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

# Layout da aplicação
app.layout = html.Div(
    [
        html.H1(
            "Dashboard Avançado - Municípios de Minas Gerais",
            style={"textAlign": "center", "marginBottom": 30},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            "Critério de Seleção:", style={"fontWeight": "bold"}
                        ),
                        dcc.Dropdown(
                            id="dropdown-criterio",
                            options=[
                                {"label": "Mais Populosos", "value": "populacao"},
                                {"label": "Maior PIB per capita", "value": "pib"},
                                {
                                    "label": "Menor Mortalidade Infantil",
                                    "value": "mortalidade_menor",
                                },
                                {
                                    "label": "Maior Mortalidade Infantil",
                                    "value": "mortalidade_maior",
                                },
                                {
                                    "label": "Maior Escolarização",
                                    "value": "escolarizacao",
                                },
                            ],
                            value="populacao",
                            style={"width": "100%"},
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Número de Municípios:", style={"fontWeight": "bold"}
                        ),
                        dcc.Slider(
                            id="slider-municipios",
                            min=10,
                            max=100,
                            step=5,
                            value=40,
                            marks={i: str(i) for i in range(10, 101, 20)},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
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
    [Input("dropdown-criterio", "value"), Input("slider-municipios", "value")],
)
def atualizar_grafico(criterio, num_municipios):
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

    # Selecionar municípios baseado no critério
    if criterio == "populacao":
        df_selecionado = df_global.nlargest(num_municipios, col_populacao)
        criterio_nome = "Mais Populosos"
    elif criterio == "pib":
        df_selecionado = df_global.nlargest(num_municipios, col_pib)
        criterio_nome = "Maior PIB per capita"
    elif criterio == "mortalidade_menor":
        df_selecionado = df_global.nsmallest(num_municipios, col_mortalidade)
        criterio_nome = "Menor Mortalidade Infantil"
    elif criterio == "mortalidade_maior":
        df_selecionado = df_global.nlargest(num_municipios, col_mortalidade)
        criterio_nome = "Maior Mortalidade Infantil"
    elif criterio == "escolarizacao":
        df_selecionado = df_global.nlargest(num_municipios, col_escolarizacao)
        criterio_nome = "Maior Escolarização"

    # Criar gráfico de dispersão
    fig = px.scatter(
        df_selecionado,
        x=col_pib,
        y=col_populacao,
        size=col_mortalidade,
        color=col_escolarizacao,
        hover_name=col_municipio,
        title=f"Municípios de MG - {criterio_nome} (Top {num_municipios})",
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
    info = f"Exibindo {num_municipios} municípios com critério: {criterio_nome}"

    return fig, info


if __name__ == "__main__":
    print("Acesse: http://127.0.0.1:8050")
    app.run(debug=True)
