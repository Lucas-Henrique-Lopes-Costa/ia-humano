import unittest
import csv
from pathlib import Path
import sys
import os

# Adiciona o diretório pai ao path para importar o módulo futebol
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from futebol import calcular_quantidade_gols


class TestCalcularQuantidadeGols(unittest.TestCase):

    def setUp(self):
        """Configuração inicial para cada teste"""
        # Caminho para o arquivo de dados de teste
        self.caminho_arquivo = Path(__file__).parent / "dados" / "futebol.csv"

        # Lê os dados do arquivo CSV
        self.dados = self.ler_arquivo_csv()

        # Remove o cabeçalho para os testes
        self.dados_sem_cabecalho = self.dados[1:] if self.dados else []

    def ler_arquivo_csv(self):
        """Lê o arquivo CSV e retorna os dados"""
        dados = []
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                leitor_csv = csv.reader(arquivo)
                for linha in leitor_csv:
                    dados.append(linha)
            return dados
        except Exception as e:
            print(f"Erro ao ler arquivo de teste: {e}")
            return []

    def test_pais_aparece_varias_vezes_nao_consecutivas(self):
        """Testa país que aparece várias vezes em linhas não consecutivas"""
        # Brasil aparece nas linhas 1, 2, 3, 8, 9 (não consecutivas)
        resultado = calcular_quantidade_gols(self.dados_sem_cabecalho, "br BRA")

        # Brasil deve aparecer em Serie A com: 15 + 8 + 12 + 0 + 5 = 40 gols
        self.assertEqual(resultado["Serie A"], 40)
        self.assertEqual(len(resultado), 1)  # Apenas uma liga

    def test_pais_aparece_em_linhas_consecutivas(self):
        """Testa país que aparece em linhas consecutivas"""
        # Portugal aparece nas linhas 4, 5, 10 (consecutivas 4-5)
        resultado = calcular_quantidade_gols(self.dados_sem_cabecalho, "pt POR")

        # Portugal deve aparecer em Primeira Liga com: 18 + 6 + 11 = 35 gols
        self.assertEqual(resultado["Primeira Liga"], 35)
        self.assertEqual(len(resultado), 1)  # Apenas uma liga

    def test_pais_aparece_apenas_uma_vez(self):
        """Testa país que aparece apenas uma vez"""
        # Espanha aparece apenas na linha 6
        resultado = calcular_quantidade_gols(self.dados_sem_cabecalho, "es ESP")

        # Espanha deve aparecer em La Liga com: 20 gols
        self.assertEqual(resultado["La Liga"], 20)
        self.assertEqual(len(resultado), 1)  # Apenas uma liga

    def test_pais_aparece_em_apenas_uma_liga(self):
        """Testa país que aparece em apenas uma liga"""
        # Brasil aparece apenas em Serie A
        resultado = calcular_quantidade_gols(self.dados_sem_cabecalho, "br BRA")

        self.assertIn("Serie A", resultado)
        self.assertNotIn("Primeira Liga", resultado)
        self.assertNotIn("La Liga", resultado)
        self.assertNotIn("Primera Division", resultado)

    def test_pais_aparece_varias_vezes_sem_gols(self):
        """Testa país que aparece várias vezes mas alguns jogadores não fizeram gols"""
        # Brasil tem um jogador (Roberto Silva) com 0 gols
        resultado = calcular_quantidade_gols(self.dados_sem_cabecalho, "br BRA")

        # Total deve ser 40 (incluindo o 0)
        self.assertEqual(resultado["Serie A"], 40)

    def test_pais_nao_aparece_no_arquivo(self):
        """Testa país que não existe no arquivo"""
        resultado = calcular_quantidade_gols(self.dados_sem_cabecalho, "xx XXX")

        # Deve retornar dicionário vazio
        self.assertEqual(resultado, {})

    def test_pais_com_um_jogador_por_liga(self):
        """Testa país que tem apenas um jogador por liga"""
        # Argentina tem apenas um jogador em Primera Division
        resultado = calcular_quantidade_gols(self.dados_sem_cabecalho, "ar ARG")

        self.assertEqual(resultado["Primera Division"], 14)
        self.assertEqual(len(resultado), 1)

    def test_estrutura_dados_correta(self):
        """Testa se a função lida corretamente com a estrutura dos dados"""
        # Verifica se os dados têm o formato esperado
        self.assertGreater(len(self.dados_sem_cabecalho), 0)

        # Verifica se cada linha tem pelo menos 13 colunas
        for linha in self.dados_sem_cabecalho:
            self.assertGreaterEqual(len(linha), 13)

    def test_calculo_correto_gols(self):
        """Testa se o cálculo dos gols está correto"""
        # Brasil: 15 + 8 + 12 + 0 + 5 = 40
        resultado_brasil = calcular_quantidade_gols(self.dados_sem_cabecalho, "br BRA")
        self.assertEqual(resultado_brasil["Serie A"], 40)

        # Portugal: 18 + 6 + 11 = 35
        resultado_portugal = calcular_quantidade_gols(
            self.dados_sem_cabecalho, "pt POR"
        )
        self.assertEqual(resultado_portugal["Primeira Liga"], 35)

        # Espanha: 20
        resultado_espanha = calcular_quantidade_gols(self.dados_sem_cabecalho, "es ESP")
        self.assertEqual(resultado_espanha["La Liga"], 20)

        # Argentina: 14
        resultado_argentina = calcular_quantidade_gols(
            self.dados_sem_cabecalho, "ar ARG"
        )
        self.assertEqual(resultado_argentina["Primera Division"], 14)


if __name__ == "__main__":
    # Executa os testes
    unittest.main(verbosity=2)
