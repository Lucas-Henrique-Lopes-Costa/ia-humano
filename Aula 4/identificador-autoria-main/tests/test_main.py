import os
import tempfile
import sys

# Adiciona o diretório app ao path para importar o módulo main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from main import (
    leitura_de_textos,
    extracao_de_palavras,
    contagem_de_letras,
    tamanho_medio_palavras,
    contagem_de_frases,
    contagem_de_oracoes,
    contagem_palavras_diferentes,
    med_palavras_por_frase,
    complexidade_media_frases,
    extracao_de_metricas,
    gerar_array_proximidade,
    identificar_autor_desconhecido,
)


class TestLeituraDeTextos:
    def test_leitura_textos_pasta_existente(self):
        """Testa a leitura de textos de uma pasta com arquivos."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Cria arquivos de teste
            with open(os.path.join(temp_dir, "autor1.txt"), "w", encoding="utf-8") as f:
                f.write("Texto do autor 1")
            with open(os.path.join(temp_dir, "autor2.txt"), "w", encoding="utf-8") as f:
                f.write("Texto do autor 2")

            resultado = leitura_de_textos(temp_dir)

            assert len(resultado) == 2
            assert "autor1" in resultado
            assert "autor2" in resultado
            assert resultado["autor1"] == "Texto do autor 1"
            assert resultado["autor2"] == "Texto do autor 2"

    def test_leitura_textos_pasta_inexistente(self):
        """Testa a leitura de textos de uma pasta que não existe."""
        resultado = leitura_de_textos("/pasta/inexistente")
        assert resultado == {}

    def test_leitura_textos_pasta_vazia(self):
        """Testa a leitura de textos de uma pasta vazia."""
        with tempfile.TemporaryDirectory() as temp_dir:
            resultado = leitura_de_textos(temp_dir)
            assert resultado == {}


class TestExtracaoDePalavras:
    def test_extracao_palavras_basico(self):
        """Testa a extração básica de palavras."""
        texto = "A chuva caía. O guarda-chuva tinha ficado em casa."
        resultado = extracao_de_palavras(texto)
        esperado = [
            "A",
            "chuva",
            "caía",
            "O",
            "guarda-chuva",
            "tinha",
            "ficado",
            "em",
            "casa",
        ]
        assert resultado == esperado

    def test_extracao_palavras_com_pontuacao(self):
        """Testa a extração de palavras removendo pontuação do início e fim."""
        texto = "Olá, mundo! Como vai?"
        resultado = extracao_de_palavras(texto)
        esperado = ["Olá", "mundo", "Como", "vai"]
        assert resultado == esperado

    def test_extracao_palavras_texto_vazio(self):
        """Testa a extração de palavras de um texto vazio."""
        resultado = extracao_de_palavras("")
        assert resultado == []

    def test_extracao_palavras_mantem_hifen(self):
        """Testa que o hífen é mantido nas palavras."""
        texto = "O guarda-chuva está quebrado."
        resultado = extracao_de_palavras(texto)
        assert "guarda-chuva" in resultado


class TestContagemDeLetras:
    def test_contagem_letras_basico(self):
        """Testa a contagem básica de letras."""
        texto = "A chuva caía. O guarda-chuva tinha ficado em casa."
        resultado = contagem_de_letras(texto)
        # A(1) + chuva(5) + caía(4) + O(1) + guarda-chuva(12) + tinha(5) + ficado(6) + em(2) + casa(4) = 40
        assert resultado == 40

    def test_contagem_letras_texto_vazio(self):
        """Testa a contagem de letras em texto vazio."""
        resultado = contagem_de_letras("")
        assert resultado == 0

    def test_contagem_letras_com_hifen(self):
        """Testa que o hífen é contado como letra."""
        texto = "guarda-chuva"
        resultado = contagem_de_letras(texto)
        assert resultado == 12  # inclui o hífen


class TestTamanhoMedioPalavras:
    def test_tamanho_medio_palavras_basico(self):
        """Testa o cálculo do tamanho médio das palavras."""
        texto = "A chuva caía. O guarda-chuva tinha ficado em casa."
        resultado = tamanho_medio_palavras(texto)
        # 40 letras / 9 palavras = 4.44...
        assert abs(resultado - 4.444444444444445) < 0.001

    def test_tamanho_medio_palavras_texto_vazio(self):
        """Testa o tamanho médio de palavras em texto vazio."""
        resultado = tamanho_medio_palavras("")
        assert resultado == 0.0


class TestContagemDeFrases:
    def test_contagem_frases_basico(self):
        """Testa a contagem básica de frases."""
        texto = "A chuva caía. O guarda-chuva tinha ficado em casa."
        resultado = contagem_de_frases(texto)
        assert resultado == 2

    def test_contagem_frases_com_exclamacao_interrogacao(self):
        """Testa a contagem de frases com diferentes delimitadores."""
        texto = "Olá! Como vai? Tudo bem."
        resultado = contagem_de_frases(texto)
        assert resultado == 3

    def test_contagem_frases_texto_sem_delimitadores(self):
        """Testa a contagem de frases em texto sem delimitadores."""
        texto = "Uma frase sem fim"
        resultado = contagem_de_frases(texto)
        assert resultado == 1  # Deve retornar 1 por padrão

    def test_contagem_frases_texto_vazio(self):
        """Testa a contagem de frases em texto vazio."""
        resultado = contagem_de_frases("")
        assert resultado == 1  # Deve retornar 1 por padrão


class TestContagemDeOracoes:
    def test_contagem_oracoes_basico(self):
        """Testa a contagem básica de orações."""
        texto = "No mesmo dia chegou uma carta, que parecia importante; mas não abri."
        resultado = contagem_de_oracoes(texto)
        # 1 (inicial) + 1 (vírgula) + 1 (ponto-e-vírgula) = 3
        assert resultado == 3

    def test_contagem_oracoes_sem_delimitadores(self):
        """Testa a contagem de orações sem delimitadores internos."""
        texto = "Uma oração simples."
        resultado = contagem_de_oracoes(texto)
        assert resultado == 1

    def test_contagem_oracoes_com_dois_pontos(self):
        """Testa a contagem de orações com dois-pontos."""
        texto = "Ele disse: muito bem, vamos começar."
        resultado = contagem_de_oracoes(texto)
        # 1 (inicial) + 1 (dois-pontos) + 1 (vírgula) = 3
        assert resultado == 3


class TestContagemPalavrasDiferentes:
    def test_contagem_palavras_diferentes_basico(self):
        """Testa a contagem de palavras diferentes."""
        texto = "Uma pérola! Uma pérola! Uma pérola brilhante! Rara. Que belo achado."
        resultado = contagem_palavras_diferentes(texto)
        # Palavras diferentes: Uma, pérola, brilhante, Rara, Que, belo, achado = 7
        assert resultado == 7

    def test_contagem_palavras_diferentes_texto_vazio(self):
        """Testa a contagem de palavras diferentes em texto vazio."""
        resultado = contagem_palavras_diferentes("")
        assert resultado == 0

    def test_contagem_palavras_diferentes_sem_repeticao(self):
        """Testa a contagem quando todas as palavras são diferentes."""
        texto = "Cada palavra é única aqui."
        resultado = contagem_palavras_diferentes(texto)
        assert resultado == 5


class TestMedPalavrasPorFrase:
    def test_med_palavras_por_frase_basico(self):
        """Testa o cálculo da média de palavras por frase."""
        texto = "A chuva caía. O guarda-chuva tinha ficado em casa."
        resultado = med_palavras_por_frase(texto)
        # 9 palavras / 2 frases = 4.5
        assert resultado == 4.5

    def test_med_palavras_por_frase_uma_frase(self):
        """Testa a média com apenas uma frase."""
        texto = "Esta é uma frase com cinco palavras."
        resultado = med_palavras_por_frase(texto)
        assert resultado == 7.0

    def test_med_palavras_por_frase_texto_vazio(self):
        """Testa a média com texto vazio."""
        resultado = med_palavras_por_frase("")
        assert resultado == 0.0


class TestComplexidadeMediaFrases:
    def test_complexidade_media_frases_basico(self):
        """Testa o cálculo da complexidade média das frases."""
        texto = "No mesmo dia chegou uma carta, que parecia importante. Mas não abri."
        resultado = complexidade_media_frases(texto)
        # 2 orações / 2 frases = 1.0
        assert resultado == 1.0

    def test_complexidade_media_frases_simples(self):
        """Testa a complexidade com frases simples."""
        texto = "Uma frase simples. Outra frase simples."
        resultado = complexidade_media_frases(texto)
        assert resultado == 0.5

    def test_complexidade_media_frases_texto_vazio(self):
        """Testa a complexidade com texto vazio."""
        resultado = complexidade_media_frases("")
        assert resultado == 1.0


class TestExtracaoDeMetricas:
    def test_extracao_metricas_basico(self):
        """Testa a extração completa de métricas."""
        texto = "Uma pérola! Uma pérola! Uma pérola brilhante! Rara. Que belo achado."
        resultado = extracao_de_metricas(texto)

        assert len(resultado) == 5
        assert all(isinstance(m, float) for m in resultado)

        # Verifica se os valores estão dentro de faixas esperadas
        assert resultado[0] > 0  # tamanho médio das palavras
        assert 0 <= resultado[1] <= 1  # proporção de palavras diferentes
        assert 0 <= resultado[2] <= 1  # proporção de palavras únicas
        assert resultado[3] > 0  # média de palavras por frase
        assert resultado[4] > 0  # complexidade média

    def test_extracao_metricas_texto_vazio(self):
        """Testa a extração de métricas com texto vazio."""
        resultado = extracao_de_metricas("")
        esperado = [0.0, 0.0, 0.0, 0.0, 0.0]
        assert resultado == esperado


class TestGerarArrayProximidade:
    def test_gerar_array_proximidade_basico(self):
        """Testa a geração do array de proximidade."""
        autores_conhecidos = {
            "autor1": "Um texto simples. Muito simples.",
            "autor2": "Outro texto diferente, mais complexo; com várias orações.",
        }
        autor_desconhecido = {"desconhecido1": "Um texto misterioso. Quem escreveu?"}

        resultado = gerar_array_proximidade(autores_conhecidos, autor_desconhecido)

        assert "conhecidos" in resultado
        assert "desconhecidos" in resultado
        assert "autor1" in resultado["conhecidos"]
        assert "autor2" in resultado["conhecidos"]
        assert "desconhecido1" in resultado["desconhecidos"]

        # Verifica se as métricas são listas de 5 elementos
        assert len(resultado["conhecidos"]["autor1"]) == 5
        assert len(resultado["conhecidos"]["autor2"]) == 5
        assert len(resultado["desconhecidos"]["desconhecido1"]) == 5


class TestIdentificarAutorDesconhecido:
    def test_identificar_autor_desconhecido_basico(self):
        """Testa a identificação do autor mais provável."""
        metricas_conhecidos = {
            "autor1": [4.0, 0.7, 0.5, 4.0, 1.0],
            "autor2": [5.0, 0.8, 0.6, 6.0, 2.0],
        }
        metrica_desconhecido = [4.1, 0.69, 0.51, 4.1, 1.1]

        resultado = identificar_autor_desconhecido(
            metricas_conhecidos, metrica_desconhecido
        )

        # O autor1 deve ser mais próximo (diferenças menores)
        assert resultado == "autor1"

    def test_identificar_autor_desconhecido_um_autor(self):
        """Testa a identificação com apenas um autor conhecido."""
        metricas_conhecidos = {"unico_autor": [4.0, 0.7, 0.5, 4.0, 1.0]}
        metrica_desconhecido = [3.0, 0.6, 0.4, 3.0, 0.9]

        resultado = identificar_autor_desconhecido(
            metricas_conhecidos, metrica_desconhecido
        )

        assert resultado == "unico_autor"

    def test_identificar_autor_desconhecido_metricas_identicas(self):
        """Testa a identificação quando as métricas são idênticas."""
        metricas_conhecidos = {"autor1": [4.0, 0.7, 0.5, 4.0, 1.0]}
        metrica_desconhecido = [4.0, 0.7, 0.5, 4.0, 1.0]

        resultado = identificar_autor_desconhecido(
            metricas_conhecidos, metrica_desconhecido
        )

        assert resultado == "autor1"


# Teste de integração
class TestIntegracao:
    def test_fluxo_completo_identificacao(self):
        """Testa o fluxo completo de identificação de autoria."""
        # Simula textos de autores conhecidos
        autores_conhecidos = {
            "shakespeare": "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer.",
            "dickens": "It was the best of times, it was the worst of times; it was the age of wisdom, it was the age of foolishness.",
        }

        # Simula texto de autor desconhecido (similar ao Shakespeare)
        autor_desconhecido = {
            "misterioso": "To live or not to live, that remains the mystery. Whether it's better in the heart to endure."
        }

        # Executa o processo completo
        metricas = gerar_array_proximidade(autores_conhecidos, autor_desconhecido)

        for nome_desconhecido, metrica_desconhecido in metricas[
            "desconhecidos"
        ].items():
            autor_identificado = identificar_autor_desconhecido(
                metricas["conhecidos"], metrica_desconhecido
            )

            # Verifica se retorna um dos autores conhecidos
            assert autor_identificado in ["shakespeare", "dickens"]
