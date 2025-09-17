import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class NewsScraper:
    """Classe para fazer scraping de notícias de diferentes sites."""

    def __init__(self, delay: float = 1.0):
        """
        Inicializa o scraper.

        Args:
            delay: Tempo de espera entre requisições (em segundos)
        """
        self.delay = delay
        self.session = requests.Session()
        # Headers para parecer uma requisição de navegador real
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Faz o download de uma página e retorna um objeto BeautifulSoup.

        Args:
            url: URL da página a ser baixada

        Returns:
            Objeto BeautifulSoup ou None em caso de erro
        """
        try:
            logger.info(f"Fazendo requisição para: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            # Pausa entre requisições para ser respeitoso com o servidor
            time.sleep(self.delay)

            return BeautifulSoup(response.content, "html.parser")

        except requests.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return None

    def extract_news_from_g1(self) -> List[Dict[str, str]]:
        """
        Extrai notícias do site G1.

        Returns:
            Lista de dicionários com título e URL das notícias
        """
        url = "https://g1.globo.com/"
        soup = self.fetch_page(url)

        if not soup:
            return []

        news = []

        # Procura por links de notícias no G1
        # O G1 usa diferentes classes, vamos tentar algumas principais
        selectors = [
            "a.feed-post-link",
            'a[href*="/noticia/"]',
            ".feed-post-body-title a",
            ".feed-media-wrapper a",
        ]

        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                title = link.get_text(strip=True)
                href = link.get("href")

                if title and href:
                    # Converte URLs relativas em absolutas
                    full_url = urljoin(url, href)

                    news.append({"titulo": title, "url": full_url, "fonte": "G1"})

        # Remove duplicatas baseadas na URL
        seen_urls = set()
        unique_news = []
        for item in news:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                unique_news.append(item)

        return unique_news[:20]  # Retorna até 20 notícias mais recentes

    def extract_news_from_uol(self) -> List[Dict[str, str]]:
        """
        Extrai notícias do site UOL.

        Returns:
            Lista de dicionários com título e URL das notícias
        """
        url = "https://www.uol.com.br/"
        soup = self.fetch_page(url)

        if not soup:
            return []

        news = []

        # Selectors para o UOL
        selectors = [
            "a.manchete-link",
            'a[href*="uol.com.br"]',
            ".manchete a",
            ".titulo a",
        ]

        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                title = link.get_text(strip=True)
                href = link.get("href")

                if title and href and len(title) > 10:  # Filtrar títulos muito curtos
                    full_url = (
                        urljoin(url, href) if not href.startswith("http") else href
                    )

                    news.append({"titulo": title, "url": full_url, "fonte": "UOL"})

        # Remove duplicatas
        seen_urls = set()
        unique_news = []
        for item in news:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                unique_news.append(item)

        return unique_news[:20]

    def extract_news_from_folha(self) -> List[Dict[str, str]]:
        """
        Extrai notícias do site Folha de S.Paulo.

        Returns:
            Lista de dicionários com título e URL das notícias
        """
        url = "https://www1.folha.uol.com.br/"
        soup = self.fetch_page(url)

        if not soup:
            return []

        news = []

        # Selectors para a Folha
        selectors = [
            "a.c-headline__url",
            'a[href*="folha.uol.com.br"]',
            ".c-main-headline a",
            ".c-headline a",
        ]

        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                title = link.get_text(strip=True)
                href = link.get("href")

                if title and href and len(title) > 10:
                    full_url = (
                        urljoin(url, href) if not href.startswith("http") else href
                    )

                    news.append(
                        {"titulo": title, "url": full_url, "fonte": "Folha de S.Paulo"}
                    )

        # Remove duplicatas
        seen_urls = set()
        unique_news = []
        for item in news:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                unique_news.append(item)

        return unique_news[:20]

    def get_all_news(self) -> List[Dict[str, str]]:
        """
        Extrai notícias de todos os sites configurados.

        Returns:
            Lista consolidada de todas as notícias
        """
        all_news = []

        logger.info("Iniciando extração de notícias...")

        # Extrai de cada site
        extractors = [
            self.extract_news_from_g1,
            self.extract_news_from_uol,
            self.extract_news_from_folha,
        ]

        for extractor in extractors:
            try:
                news = extractor()
                all_news.extend(news)
                logger.info(f"Extraídas {len(news)} notícias de {extractor.__name__}")
            except Exception as e:
                logger.error(f"Erro em {extractor.__name__}: {e}")

        logger.info(f"Total de notícias extraídas: {len(all_news)}")
        return all_news

    def display_news(self, news: List[Dict[str, str]]) -> None:
        """
        Exibe as notícias de forma organizada.

        Args:
            news: Lista de notícias para exibir
        """
        if not news:
            print("❌ Nenhuma notícia encontrada.")
            return

        print("=" * 80)
        print(f"📰 NOTÍCIAS MAIS RECENTES ({len(news)} encontradas)")
        print("=" * 80)

        for i, item in enumerate(news, 1):
            print(f"\n{i:2d}. [{item['fonte']}] {item['titulo']}")
            print(f"    🔗 {item['url']}")

        print("\n" + "=" * 80)

    def save_to_file(
        self, news: List[Dict[str, str]], filename: str = "noticias.txt"
    ) -> None:
        """
        Salva as notícias em um arquivo de texto.

        Args:
            news: Lista de notícias para salvar
            filename: Nome do arquivo
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"NOTÍCIAS EXTRAÍDAS - {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                for i, item in enumerate(news, 1):
                    f.write(f"{i:2d}. [{item['fonte']}] {item['titulo']}\n")
                    f.write(f"    URL: {item['url']}\n\n")

            logger.info(f"Notícias salvas em {filename}")

        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {e}")


def main():
    """Função principal do programa."""
    print("🚀 Iniciando Webscraper de Notícias...")

    # Cria o scraper
    scraper = NewsScraper(delay=1.5)

    # Extrai todas as notícias
    news = scraper.get_all_news()

    # Exibe as notícias
    scraper.display_news(news)

    # Salva em arquivo
    scraper.save_to_file(news)

    print("\n✅ Processo concluído!")


if __name__ == "__main__":
    main()
