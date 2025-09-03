import csv
from pathlib import Path


def calcular_quantidade_gols(dados, pais):
    """
    dados contém dados estatísticos de futebol:
    - a terceira coluna traz o nome do país do jogador
    - a quinta coluna o nome da liga
    - a décima segunda coluna o número de gols feitos pelo jogador
    pais é a identificação do país de interesse (ex.: "br BRA")

    A função calcula e retorna a quantidade de gols feitos
    por jogadores do país passado em cada liga
    """
    gols_por_liga = {}

    for linha in dados:
        if len(linha) >= 13:  # Verifica se a linha tem pelo menos 13 colunas
            pais_jogador = linha[2]  # Terceira coluna (índice 2)
            liga = linha[4]  # Quinta coluna (índice 4) - Liga
            gols = linha[11]  # Décima segunda coluna (índice 11) - Gols_Ano

            if pais_jogador == pais:
                try:
                    gols_int = int(gols)
                    if liga in gols_por_liga:
                        gols_por_liga[liga] += gols_int
                    else:
                        gols_por_liga[liga] = gols_int
                except ValueError:
                    # Se não conseguir converter para int, ignora a linha
                    continue

    return gols_por_liga


def ler_arquivo_futebol(caminho_arquivo):
    """
    Lê o arquivo CSV de futebol e retorna os dados como uma lista de listas
    """
    dados = []
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            leitor_csv = csv.reader(arquivo)
            for linha in leitor_csv:
                dados.append(linha)
        return dados
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return []
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return []


if __name__ == "__main__":
    # Exemplo de uso
    CAMINHO_ARQUIVO = Path(__file__).parent / "testes" / "dados" / "futebol.csv"

    dados = ler_arquivo_futebol(CAMINHO_ARQUIVO)
    if dados:
        # Remove o cabeçalho
        dados_sem_cabecalho = dados[1:]

        # Testa com Brasil
        resultado_brasil = calcular_quantidade_gols(dados_sem_cabecalho, "br BRA")
        print(f"Gols de jogadores brasileiros por liga: {resultado_brasil}")

        # Testa com Portugal
        resultado_portugal = calcular_quantidade_gols(dados_sem_cabecalho, "pt POR")
        print(f"Gols de jogadores portugueses por liga: {resultado_portugal}")

        # Testa com Espanha
        resultado_espanha = calcular_quantidade_gols(dados_sem_cabecalho, "es ESP")
        print(f"Gols de jogadores espanhóis por liga: {resultado_espanha}")

        # Testa com país que não existe
        resultado_inexistente = calcular_quantidade_gols(dados_sem_cabecalho, "xx XXX")
        print(f"Gols de país inexistente: {resultado_inexistente}")
