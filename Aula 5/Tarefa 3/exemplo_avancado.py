"""
Exemplo de Uso Avançado do Webscraper
=====================================

Este arquivo demonstra como usar o webscraper de forma mais avançada,
incluindo filtragem, análise e relatórios personalizados.
"""

from webscraper import NewsScraper
import json
from collections import Counter
import re


class AdvancedNewsAnalyzer(NewsScraper):
    """Classe estendida para análise avançada de notícias."""

    def filter_news_by_keywords(self, news, keywords):
        """
        Filtra notícias que contenham palavras-chave específicas.

        Args:
            news: Lista de notícias
            keywords: Lista de palavras-chave para filtrar

        Returns:
            Lista de notícias filtradas
        """
        filtered_news = []

        for item in news:
            title_lower = item["titulo"].lower()
            if any(keyword.lower() in title_lower for keyword in keywords):
                filtered_news.append(item)

        return filtered_news

    def analyze_topics(self, news):
        """
        Analisa os tópicos mais comuns nas notícias.

        Args:
            news: Lista de notícias

        Returns:
            Dicionário com estatísticas dos tópicos
        """
        # Palavras comuns em português que serão ignoradas
        stop_words = {
            "de",
            "da",
            "do",
            "das",
            "dos",
            "e",
            "o",
            "a",
            "os",
            "as",
            "em",
            "na",
            "no",
            "nas",
            "nos",
            "para",
            "por",
            "com",
            "sem",
            "que",
            "se",
            "não",
            "é",
            "são",
            "foi",
            "foram",
            "será",
            "serão",
            "tem",
            "têm",
            "teve",
            "tiveram",
            "terá",
            "terão",
            "mais",
            "menos",
            "sobre",
            "após",
            "antes",
            "durante",
            "contra",
            "entre",
            "até",
            "pela",
            "pelo",
            "pelas",
            "pelos",
            "sua",
            "seu",
            "suas",
            "seus",
        }

        all_words = []

        for item in news:
            # Remove pontuação e converte para minúsculas
            title = re.sub(r"[^\w\s]", " ", item["titulo"].lower())
            words = title.split()

            # Filtra palavras significativas
            significant_words = [
                word for word in words if len(word) > 3 and word not in stop_words
            ]

            all_words.extend(significant_words)

        # Conta a frequência das palavras
        word_counter = Counter(all_words)

        return {
            "total_words": len(all_words),
            "unique_words": len(word_counter),
            "most_common": word_counter.most_common(10),
            "news_count": len(news),
        }

    def generate_report(self, news):
        """
        Gera um relatório detalhado das notícias.

        Args:
            news: Lista de notícias

        Returns:
            Dicionário com relatório completo
        """
        # Análise por fonte
        sources = Counter(item["fonte"] for item in news)

        # Análise de tópicos
        topics = self.analyze_topics(news)

        # Análise de URLs
        domains = Counter()
        for item in news:
            try:
                from urllib.parse import urlparse

                domain = urlparse(item["url"]).netloc
                domains[domain] += 1
            except:
                pass

        return {
            "summary": {
                "total_news": len(news),
                "sources": dict(sources),
                "domains": dict(domains.most_common(5)),
            },
            "topics": topics,
            "recent_news": news[:5],  # 5 mais recentes
        }

    def save_json_report(self, news, filename="relatorio_noticias.json"):
        """
        Salva um relatório em formato JSON.

        Args:
            news: Lista de notícias
            filename: Nome do arquivo JSON
        """
        report = self.generate_report(news)

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            print(f"📊 Relatório JSON salvo em {filename}")

        except Exception as e:
            print(f"❌ Erro ao salvar relatório JSON: {e}")


def demo_basic_usage():
    """Demonstração de uso básico."""
    print("=" * 60)
    print("🔥 DEMONSTRAÇÃO - USO BÁSICO")
    print("=" * 60)

    scraper = NewsScraper(delay=1.0)

    # Extrair apenas do G1
    print("\n📰 Extraindo notícias apenas do G1...")
    noticias_g1 = scraper.extract_news_from_g1()
    print(f"✅ Encontradas {len(noticias_g1)} notícias do G1")

    # Exibir apenas as 5 primeiras
    print("\n🔝 Top 5 notícias do G1:")
    for i, noticia in enumerate(noticias_g1[:5], 1):
        print(f"{i}. {noticia['titulo']}")


def demo_advanced_usage():
    """Demonstração de uso avançado."""
    print("\n" + "=" * 60)
    print("🚀 DEMONSTRAÇÃO - USO AVANÇADO")
    print("=" * 60)

    analyzer = AdvancedNewsAnalyzer(delay=1.0)

    # Extrair todas as notícias
    print("\n📊 Extraindo todas as notícias...")
    all_news = analyzer.get_all_news()

    # Filtrar notícias sobre política
    print("\n🏛️ Filtrando notícias sobre política...")
    political_keywords = [
        "bolsonaro",
        "lula",
        "presidente",
        "câmara",
        "senado",
        "política",
        "deputado",
    ]
    political_news = analyzer.filter_news_by_keywords(all_news, political_keywords)

    print(f"✅ Encontradas {len(political_news)} notícias sobre política:")
    for i, noticia in enumerate(political_news[:3], 1):
        print(f"  {i}. [{noticia['fonte']}] {noticia['titulo']}")

    # Filtrar notícias sobre economia
    print("\n💰 Filtrando notícias sobre economia...")
    economic_keywords = [
        "economia",
        "dólar",
        "juros",
        "ibovespa",
        "mercado",
        "inflação",
        "banco",
    ]
    economic_news = analyzer.filter_news_by_keywords(all_news, economic_keywords)

    print(f"✅ Encontradas {len(economic_news)} notícias sobre economia:")
    for i, noticia in enumerate(economic_news[:3], 1):
        print(f"  {i}. [{noticia['fonte']}] {noticia['titulo']}")

    # Análise de tópicos
    print("\n🔍 Analisando tópicos mais comuns...")
    topics = analyzer.analyze_topics(all_news)

    print(f"📈 Estatísticas:")
    print(f"  • Total de palavras: {topics['total_words']}")
    print(f"  • Palavras únicas: {topics['unique_words']}")
    print(f"  • Total de notícias: {topics['news_count']}")

    print(f"\n🏆 Top 5 palavras mais comuns:")
    for word, count in topics["most_common"][:5]:
        print(f"  • {word}: {count} vezes")

    # Gerar relatório completo
    print("\n📋 Gerando relatório completo...")
    analyzer.save_json_report(all_news)

    # Salvar notícias filtradas
    analyzer.save_to_file(political_news, "noticias_politica.txt")
    analyzer.save_to_file(economic_news, "noticias_economia.txt")


def demo_custom_scraping():
    """Demonstração de scraping personalizado."""
    print("\n" + "=" * 60)
    print("🛠️ DEMONSTRAÇÃO - SCRAPING PERSONALIZADO")
    print("=" * 60)

    scraper = NewsScraper(delay=0.5)  # Mais rápido para demonstração

    # Exemplo de como adicionar um novo site
    def extract_news_from_custom_site(self, url, selectors):
        """Método genérico para extrair notícias de qualquer site."""
        soup = self.fetch_page(url)

        if not soup:
            return []

        news = []

        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                title = link.get_text(strip=True)
                href = link.get("href")

                if title and href and len(title) > 10:
                    from urllib.parse import urljoin

                    full_url = (
                        urljoin(url, href) if not href.startswith("http") else href
                    )

                    news.append(
                        {
                            "titulo": title,
                            "url": full_url,
                            "fonte": "Site Personalizado",
                        }
                    )

        return news[:10]  # Limite de 10 notícias

    print("✅ Função de scraping personalizado criada!")
    print("💡 Esta função pode ser usada para qualquer site de notícias")
    print("   Basta fornecer a URL e os seletores CSS apropriados.")


if __name__ == "__main__":
    print("🎯 DEMONSTRAÇÕES DO WEBSCRAPER DE NOTÍCIAS")
    print("=" * 60)

    try:
        # Executar demonstrações
        demo_basic_usage()
        demo_advanced_usage()
        demo_custom_scraping()

        print("\n" + "=" * 60)
        print("🎉 TODAS AS DEMONSTRAÇÕES CONCLUÍDAS!")
        print("=" * 60)
        print("\n📁 Arquivos gerados:")
        print("  • webscraper.py - Código principal")
        print("  • exemplo_avancado.py - Este arquivo")
        print("  • noticias.txt - Todas as notícias")
        print("  • noticias_politica.txt - Notícias de política")
        print("  • noticias_economia.txt - Notícias de economia")
        print("  • relatorio_noticias.json - Relatório em JSON")

    except KeyboardInterrupt:
        print("\n\n⚠️ Demonstração interrompida pelo usuário.")
    except Exception as e:
        print(f"\n\n❌ Erro durante a demonstração: {e}")
