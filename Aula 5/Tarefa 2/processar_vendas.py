#!/usr/bin/env python3
"""
Script para processar dados de vendas mensais de produtos.
Lê o arquivo vendas_produtos.xlsx, calcula totais por produto
e gera o arquivo vendas_totais.xlsx.

Autor: GitHub Copilot
Data: 17 de setembro de 2025
"""

import pandas as pd
import locale
from pathlib import Path


def configurar_locale():
    """Configura o locale para formatação de moeda brasileira."""
    try:
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, "pt_BR")
        except locale.Error:
            print("⚠️  Aviso: Não foi possível configurar o locale brasileiro")
            return False
    return True


def formatar_moeda(valor):
    """Formata um valor numérico como moeda brasileira."""
    try:
        return locale.currency(valor, grouping=True)
    except:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_dados(arquivo):
    """Carrega os dados do arquivo Excel."""
    try:
        print(f"📂 Carregando dados de '{arquivo}'...")
        df = pd.read_excel(arquivo)
        print(f"✅ Dados carregados: {df.shape[0]} registros, {df.shape[1]} colunas")
        return df
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{arquivo}' não encontrado!")
        return None
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        return None


def explorar_dados(df):
    """Explora e exibe informações sobre os dados."""
    print("\n📊 Estrutura dos dados:")
    print(f"Colunas: {list(df.columns)}")
    print(f"\nPrimeiros registros:")
    print(df.head())
    print(f"\nTipos de dados:")
    print(df.dtypes)
    print(f"\nProdutos únicos: {df['Descrição do Produto'].nunique()}")
    print(f"Códigos únicos: {df['Código do Produto'].nunique()}")


def calcular_totais_por_produto(df):
    """Calcula o total de vendas por produto."""
    print("\n🔢 Calculando totais por produto...")

    # Agrupar por Descrição e Código do Produto, somando as vendas
    totais = (
        df.groupby(["Descrição do Produto", "Código do Produto"])["Valor das Vendas"]
        .sum()
        .reset_index()
    )

    # Renomear a coluna para o resultado final
    totais.rename(columns={"Valor das Vendas": "Total de Vendas"}, inplace=True)

    # Ordenar por Total de Vendas (decrescente)
    totais = totais.sort_values("Total de Vendas", ascending=False)

    print(f"✅ Totais calculados para {len(totais)} produtos")
    return totais


def exibir_resultados(df_totais):
    """Exibe os resultados calculados."""
    print("\n📈 Resultados calculados:")
    print("=" * 80)

    for _, row in df_totais.iterrows():
        produto = row["Descrição do Produto"]
        codigo = row["Código do Produto"]
        total = formatar_moeda(row["Total de Vendas"])
        print(f"{produto:<20} | {codigo} | {total}")

    print("=" * 80)


def salvar_resultados(df_totais, arquivo_saida):
    """Salva os resultados em um arquivo Excel."""
    try:
        print(f"\n💾 Salvando resultados em '{arquivo_saida}'...")

        # Criar uma cópia do DataFrame para formatação
        df_formatado = df_totais.copy()

        # Salvar no Excel sem formatação de moeda (valores numéricos)
        df_formatado.to_excel(arquivo_saida, index=False, engine="openpyxl")

        print(f"✅ Arquivo '{arquivo_saida}' criado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")
        return False


def validar_resultados(df_totais):
    """Valida os resultados comparando com valores esperados."""
    print("\n🔍 Validando resultados...")

    # Valores esperados do usuário
    valores_esperados = {
        "P008": 17982.43,  # Cadeira Escritório
        "P010": 3699.33,  # HD Externo Seagate
        "P009": 22404.40,  # Headset JBL
        "P005": 3931.24,  # Impressora HP
        "P004": 28756.69,  # Monitor LG
        "P007": 25156.30,  # Mouse Gamer
        "P001": 19085.25,  # Notebook Dell
        "P002": 4438.86,  # Smartphone Samsung
        "P003": 5330.93,  # Tablet Apple
        "P006": 13751.35,  # Teclado Mecânico
    }

    # Converter para dicionário para comparação
    resultados_dict = dict(
        zip(df_totais["Código do Produto"], df_totais["Total de Vendas"])
    )

    print("Comparação com valores esperados:")
    print("-" * 60)

    todos_corretos = True
    for codigo, valor_esperado in valores_esperados.items():
        valor_calculado = resultados_dict.get(codigo, 0)
        diferenca = abs(valor_calculado - valor_esperado)

        if diferenca < 0.01:  # Tolerância para diferenças de centavos
            status = "✅"
        else:
            status = "❌"
            todos_corretos = False

        print(
            f"{status} {codigo}: Esperado: {formatar_moeda(valor_esperado)} | "
            f"Calculado: {formatar_moeda(valor_calculado)}"
        )

    print("-" * 60)
    if todos_corretos:
        print("🎉 Todos os valores estão corretos!")
    else:
        print("⚠️  Alguns valores não conferem. Verifique os dados.")

    return todos_corretos


def main():
    """Função principal do script."""
    print("🚀 Iniciando processamento de vendas de produtos")
    print("=" * 50)

    # Configurar locale para formatação de moeda
    configurar_locale()

    # Definir arquivos
    arquivo_entrada = "vendas_produtos.xlsx"
    arquivo_saida = "vendas_totais.xlsx"

    # Verificar se o arquivo de entrada existe
    if not Path(arquivo_entrada).exists():
        print(f"❌ Arquivo '{arquivo_entrada}' não encontrado!")
        return

    # 1. Carregar dados
    df_vendas = carregar_dados(arquivo_entrada)
    if df_vendas is None:
        return

    # 2. Explorar dados
    explorar_dados(df_vendas)

    # 3. Calcular totais por produto
    df_totais = calcular_totais_por_produto(df_vendas)

    # 4. Exibir resultados
    exibir_resultados(df_totais)

    # 5. Salvar resultados
    if salvar_resultados(df_totais, arquivo_saida):
        # 6. Validar resultados
        validar_resultados(df_totais)

        print(f"\n🎯 Processamento concluído!")
        print(f"📄 Arquivo de entrada: {arquivo_entrada}")
        print(f"📄 Arquivo de saída: {arquivo_saida}")
    else:
        print("\n❌ Falha no processamento!")


if __name__ == "__main__":
    main()
