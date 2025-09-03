#!/usr/bin/env python3
"""
Exemplo de uso da função calcular_quantidade_gols
Demonstra diferentes cenários de uso da função
"""

from futebol import calcular_quantidade_gols, ler_arquivo_futebol
from pathlib import Path


def main():
    # Caminho para o arquivo de dados
    caminho_arquivo = Path(__file__).parent / "testes" / "dados" / "futebol.csv"

    # Lê os dados do arquivo
    dados = ler_arquivo_futebol(caminho_arquivo)

    if not dados:
        print("Erro: Não foi possível ler o arquivo de dados")
        return

    # Remove o cabeçalho
    dados_sem_cabecalho = dados[1:]

    print("=== ANÁLISE DE GOLS POR PAÍS E LIGA ===\n")

    # Lista de países para testar
    paises = [
        ("br BRA", "Brasil"),
        ("pt POR", "Portugal"),
        ("es ESP", "Espanha"),
        ("ar ARG", "Argentina"),
        ("xx XXX", "País Inexistente"),
    ]

    for codigo_pais, nome_pais in paises:
        resultado = calcular_quantidade_gols(dados_sem_cabecalho, codigo_pais)

        if resultado:
            print(f"🇧🇷 {nome_pais} ({codigo_pais}):")
            total_gols = 0
            for liga, gols in resultado.items():
                print(f"   📍 {liga}: {gols} gols")
                total_gols += gols
            print(f"   🎯 Total: {total_gols} gols\n")
        else:
            print(f"❌ {nome_pais} ({codigo_pais}): Nenhum jogador encontrado\n")

    print("=== ESTATÍSTICAS GERAIS ===")

    # Conta total de jogadores por liga
    ligas = {}
    for linha in dados_sem_cabecalho:
        if len(linha) >= 5:
            liga = linha[4]
            if liga in ligas:
                ligas[liga] += 1
            else:
                ligas[liga] = 1

    print("\n📊 Jogadores por liga:")
    for liga, quantidade in ligas.items():
        print(f"   {liga}: {quantidade} jogadores")

    # Conta total de gols por liga
    gols_por_liga = {}
    for linha in dados_sem_cabecalho:
        if len(linha) >= 12:
            liga = linha[4]
            try:
                gols = int(linha[11])
                if liga in gols_por_liga:
                    gols_por_liga[liga] += gols
                else:
                    gols_por_liga[liga] = gols
            except ValueError:
                continue

    print("\n⚽ Total de gols por liga:")
    for liga, gols in gols_por_liga.items():
        print(f"   {liga}: {gols} gols")


if __name__ == "__main__":
    main()
