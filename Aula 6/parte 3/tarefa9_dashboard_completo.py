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


# Carregar dados globalmente
df_global = carregar_dados()
opcoes_colunas = []
col_municipio = None

if df_global is not None:
    # Identificar coluna do município
    for col in df_global.columns:
        if "munic" in str(col).lower() or "nome" in str(col).lower():
            col_municipio = col
            break
    if not col_municipio:
        col_municipio = df_global.columns[0]

    # Identificar colunas numéricas
    colunas_numericas = df_global.select_dtypes(include=["number"]).columns.tolist()

    # Tentar converter colunas que podem ser numéricas
    for col in df_global.columns:
        if col != col_municipio and col not in colunas_numericas:
            try:
                df_global[col] = pd.to_numeric(df_global[col], errors="coerce")
                if not df_global[col].isna().all():
                    colunas_numericas.append(col)
            except:
                pass

    # Criar opções para dropdowns
    opcoes_colunas = [{"label": col, "value": col} for col in colunas_numericas]

    # Limpar dados nulos das colunas numéricas
    df_global = df_global.dropna(subset=colunas_numericas)

# Layout da aplicação
app.layout = html.Div(
    [
        html.H1(
            "Dashboard Personalizado - Municípios de Minas Gerais",
            style={"textAlign": "center", "marginBottom": 30},
        ),
        # Controles superiores
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
                    style={
                        "width": "24%",
                        "display": "inline-block",
                        "marginRight": "1%",
                    },
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
                            marks={i: str(i) for i in range(10, 101, 30)},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    style={"width": "74%", "float": "right", "display": "inline-block"},
                ),
            ],
            style={"margin": "20px"},
        ),
        # Controles de colunas
        html.Div(
            [
                html.H3("Configuração do Gráfico", style={"textAlign": "center"}),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Eixo X:", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="dropdown-x",
                                    options=opcoes_colunas,
                                    value=(
                                        opcoes_colunas[0]["value"]
                                        if opcoes_colunas
                                        else None
                                    ),
                                    style={"width": "100%"},
                                ),
                            ],
                            style={
                                "width": "24%",
                                "display": "inline-block",
                                "marginRight": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Label("Eixo Y:", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="dropdown-y",
                                    options=opcoes_colunas,
                                    value=(
                                        opcoes_colunas[1]["value"]
                                        if len(opcoes_colunas) > 1
                                        else None
                                    ),
                                    style={"width": "100%"},
                                ),
                            ],
                            style={
                                "width": "24%",
                                "display": "inline-block",
                                "marginRight": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Tamanho dos Pontos:", style={"fontWeight": "bold"}
                                ),
                                dcc.Dropdown(
                                    id="dropdown-size",
                                    options=opcoes_colunas,
                                    value=(
                                        opcoes_colunas[2]["value"]
                                        if len(opcoes_colunas) > 2
                                        else None
                                    ),
                                    style={"width": "100%"},
                                ),
                            ],
                            style={
                                "width": "24%",
                                "display": "inline-block",
                                "marginRight": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Cor dos Pontos:", style={"fontWeight": "bold"}
                                ),
                                dcc.Dropdown(
                                    id="dropdown-color",
                                    options=opcoes_colunas,
                                    value=(
                                        opcoes_colunas[3]["value"]
                                        if len(opcoes_colunas) > 3
                                        else None
                                    ),
                                    style={"width": "100%"},
                                ),
                            ],
                            style={
                                "width": "24%",
                                "float": "right",
                                "display": "inline-block",
                            },
                        ),
                    ]
                ),
            ],
            style={
                "margin": "20px",
                "padding": "10px",
                "border": "1px solid #ddd",
                "borderRadius": "5px",
            },
        ),
        dcc.Graph(id="grafico-dispersao"),
        html.Div(id="info-municipios", style={"margin": "20px", "textAlign": "center"}),
    ]
)


# Função para determinar critério de ordenação
def aplicar_criterio_ordenacao(
    df, criterio, col_populacao, col_pib, col_mortalidade, col_escolarizacao
):
    if criterio == "populacao" and col_populacao in df.columns:
        return df.nlargest(100, col_populacao)
    elif criterio == "pib" and col_pib in df.columns:
        return df.nlargest(100, col_pib)
    elif criterio == "mortalidade_menor" and col_mortalidade in df.columns:
        return df.nsmallest(100, col_mortalidade)
    elif criterio == "mortalidade_maior" and col_mortalidade in df.columns:
        return df.nlargest(100, col_mortalidade)
    elif criterio == "escolarizacao" and col_escolarizacao in df.columns:
        return df.nlargest(100, col_escolarizacao)
    else:
        # Fallback: ordenar pela primeira coluna numérica
        primeira_numerica = df.select_dtypes(include=["number"]).columns[0]
        return df.nlargest(100, primeira_numerica)


# Callback para atualizar o gráfico
@app.callback(
    [Output("grafico-dispersao", "figure"), Output("info-municipios", "children")],
    [
        Input("dropdown-criterio", "value"),
        Input("slider-municipios", "value"),
        Input("dropdown-x", "value"),
        Input("dropdown-y", "value"),
        Input("dropdown-size", "value"),
        Input("dropdown-color", "value"),
    ],
)
def atualizar_grafico(criterio, num_municipios, col_x, col_y, col_size, col_color):
    if df_global is None:
        fig = px.scatter(title="Erro: Arquivo de dados não encontrado")
        info = "Por favor, adicione o arquivo Excel com dados dos municípios de MG."
        return fig, info

    if not all([col_x, col_y]):
        fig = px.scatter(title="Erro: Selecione pelo menos os eixos X e Y")
        info = "Selecione as colunas para os eixos X e Y."
        return fig, info

    # Identificar colunas para critério (para compatibilidade)
    col_populacao = None
    col_pib = None
    col_mortalidade = None
    col_escolarizacao = None

    for col in df_global.columns:
        if "população" in str(col).lower() or "pop" in str(col).lower():
            col_populacao = col
        elif "pib" in str(col).lower() and (
            "per" in str(col).lower() or "capita" in str(col).lower()
        ):
            col_pib = col
        elif "mortalidade" in str(col).lower():
            col_mortalidade = col
        elif "escolar" in str(col).lower() or "educação" in str(col).lower():
            col_escolarizacao = col

    # Aplicar critério de seleção
    df_ordenado = aplicar_criterio_ordenacao(
        df_global, criterio, col_populacao, col_pib, col_mortalidade, col_escolarizacao
    )
    df_selecionado = df_ordenado.head(num_municipios)

    # Criar gráfico de dispersão
    fig = px.scatter(
        df_selecionado,
        x=col_x,
        y=col_y,
        size=col_size if col_size else None,
        color=col_color if col_color else None,
        hover_name=col_municipio,
        title=f"Gráfico Personalizado - {num_municipios} Municípios de MG",
        labels={
            col_x: col_x,
            col_y: col_y,
            col_size: col_size if col_size else "",
            col_color: col_color if col_color else "",
        },
    )

    fig.update_layout(height=600, xaxis_title=col_x, yaxis_title=col_y)

    # Informações
    info_texto = f"Gráfico: X={col_x}, Y={col_y}"
    if col_size:
        info_texto += f", Tamanho={col_size}"
    if col_color:
        info_texto += f", Cor={col_color}"
    info_texto += f" | {num_municipios} municípios"

    return fig, info_texto


if __name__ == "__main__":
    print("Acesse: http://127.0.0.1:8050")
    app.run(debug=True)
