import matplotlib.pyplot as plt


def carregar_dados_futebol(nome_arquivo_csv):
    """
    A função abre o arquivo CSV passado por parâmetro e retorna os dados carregados
    """
    import csv

    with open(nome_arquivo_csv, mode="r", encoding="utf-8") as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)
        dados = [linha for linha in leitor_csv]

    return dados


def calcular_quantidade_gols(dados, pais, idade_maxima):
    """
    dados contém dados estatísticos de futebol:
    - a terceira coluna traz o nome do país do jogador
    - a sexta coluna o nome da liga
    - a sétima coluna a idade do jogador
    - a nona coluna o número de gols feitos pelo jogador
    pais é a identificação do país de interesse (ex.: "br BRA")
    idade_maxima é a idade máxima dos jogadores a serem considerados

    A função calcula e retorna a quantidade de gols feitos
    por jogadores do país passado em cada liga, considerando apenas
    jogadores com idade menor ou igual à idade_maxima.
    """
    quantidade_gols = {}
    for linha in dados:
        if linha[list(linha.keys())[2]] == pais:
            idade = int(linha[list(linha.keys())[6]])
            if idade <= idade_maxima:
                liga = linha[list(linha.keys())[5]]
                gols = int(linha[list(linha.keys())[8]])
                if liga in quantidade_gols:
                    quantidade_gols[liga] += gols
                else:
                    quantidade_gols[liga] = gols
    return quantidade_gols


def exibir_gols_por_liga(quantidade_gols):
    """
    A função exibe a quantidade de gols feitos por
    jogadores de um país em cada liga em ordem decrescente,
    agora em um gráfico de barras.
    """

    ligas = {
        "eng": "Inglaterra",
        "es": "Espanha",
        "it": "Itália",
        "fr": "França",
        "de": "Alemanha",
    }

    # Ordena as ligas pela quantidade de gols em ordem decrescente
    ligas_ordenadas = sorted(quantidade_gols.items(), key=lambda x: x[1], reverse=True)

    nomes_ligas = []
    gols = []
    for liga, qtd_gols in ligas_ordenadas:
        sigla_pais = liga.split()[0]
        nome_pais = ligas.get(sigla_pais, sigla_pais)
        nome_liga = f"{nome_pais} {liga.split()[1]}"
        nomes_ligas.append(nome_liga)
        gols.append(qtd_gols)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(nomes_ligas, gols, color="skyblue")

    # Aumenta o tamanho das fontes
    plt.xlabel("Liga", fontsize=16)
    plt.ylabel("Quantidade de Gols", fontsize=16)
    plt.title("Gols por Liga", fontsize=18)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)

    # Exibe o número de gols nas barras
    for bar, qtd in zip(bars, gols):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(qtd),
            ha="center",
            va="bottom",
            fontsize=14,
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig("gols_por_liga.png", dpi=150)
    plt.show()


def exibir_top5_goleadores_por_liga(dados, pais, idade_maxima):
    """
    Exibe os nomes e quantidade de gols dos cinco jogadores que mais fizeram gols em cada liga,
    ordenados pela quantidade de gols.
    """
    from collections import defaultdict

    jogadores_por_liga = defaultdict(list)
    for linha in dados:
        if linha[list(linha.keys())[2]] == pais:
            idade = int(linha[list(linha.keys())[6]])
            if idade <= idade_maxima:
                liga = linha[list(linha.keys())[5]]
                nome = linha[list(linha.keys())[0]]
                gols = int(linha[list(linha.keys())[8]])
                jogadores_por_liga[liga].append((nome, gols))

    for liga, jogadores in jogadores_por_liga.items():
        print(f"\nLiga: {liga}")
        top5 = sorted(jogadores, key=lambda x: x[1], reverse=True)[:5]
        for i, (nome, gols) in enumerate(top5, 1):
            print(f"{i}. {nome}: {gols} gols")


def exibir_jogador_mais_jovem_com_gol_por_liga(dados, pais):
    """
    Encontra o jogador mais jovem que marcou gol em cada liga e exibe seu nome, idade, equipe e número de gols.
    """
    from collections import defaultdict

    mais_jovem_por_liga = {}
    for linha in dados:
        if linha[list(linha.keys())[2]] == pais:
            gols = int(linha[list(linha.keys())[8]])
            if gols > 0:
                liga = linha[list(linha.keys())[5]]
                idade = int(linha[list(linha.keys())[6]])
                nome = linha[list(linha.keys())[0]]
                equipe = linha[list(linha.keys())[4]]
                if (liga not in mais_jovem_por_liga) or (
                    idade < mais_jovem_por_liga[liga][1]
                ):
                    mais_jovem_por_liga[liga] = (nome, idade, equipe, gols)

    for liga, (nome, idade, equipe, gols) in mais_jovem_por_liga.items():
        print(f"\nLiga: {liga}")
        print(
            f"Jogador mais jovem com gol: {nome} | Idade: {idade} | Equipe: {equipe} | Gols: {gols}"
        )


def exibir_equipe_menos_cartoes_por_liga(dados, pais):
    """
    Encontra a equipe que menos tomou cartões (amarelos e vermelhos) em cada liga.
    Exibe o nome da equipe e a quantidade de cartões recebidos de cada tipo.
    """
    from collections import defaultdict

    cartoes_por_liga_equipe = defaultdict(
        lambda: defaultdict(lambda: [0, 0])
    )  # [amarelos, vermelhos]
    for linha in dados:
        if linha[list(linha.keys())[2]] == pais:
            liga = linha[list(linha.keys())[5]]
            equipe = linha[list(linha.keys())[4]]
            amarelos = int(float(linha[list(linha.keys())[10]]))
            vermelhos = int(float(linha[list(linha.keys())[11]]))
            cartoes_por_liga_equipe[liga][equipe][0] += amarelos
            cartoes_por_liga_equipe[liga][equipe][1] += vermelhos

    for liga, equipes in cartoes_por_liga_equipe.items():
        equipe_menos_cartoes = min(
            equipes.items(), key=lambda x: (x[1][0] + x[1][1], x[1][0], x[1][1])
        )
        equipe, (amarelos, vermelhos) = equipe_menos_cartoes
        print(f"\nLiga: {liga}")
        print(
            f"Equipe com menos cartões: {equipe} | Amarelos: {amarelos} | Vermelhos: {vermelhos}"
        )


if __name__ == "__main__":
    dados = carregar_dados_futebol("top5-players.csv")
    exibir_gols_por_liga(quantidade_gols)
    quantidade_gols = calcular_quantidade_gols(dados, "br BRA", 23)
    exibir_top5_goleadores_por_liga(dados, "br BRA", 23)
    exibir_jogador_mais_jovem_com_gol_por_liga(dados, "br BRA")
    exibir_equipe_menos_cartoes_por_liga(dados, "br BRA")
    print("Análise concluída.")
