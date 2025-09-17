# 📰 Webscraper de Notícias

Um webscraper em Python que extrai manchetes e URLs de sites de notícias brasileiros populares.

## 🚀 Características

- **Múltiplos Sites**: Extrai notícias do G1, UOL e Folha de S.Paulo
- **Tratamento de Erros**: Robusto contra falhas de rede e mudanças no layout dos sites
- **Respeitoso**: Inclui delays entre requisições para não sobrecarregar os servidores
- **Flexível**: Fácil de estender para incluir novos sites de notícias
- **Saída Organizada**: Exibe as notícias no terminal e salva em arquivo

## 📋 Dependências

- `beautifulsoup4`: Para parsing do HTML
- `requests`: Para fazer requisições HTTP
- `lxml`: Parser rápido para BeautifulSoup

## 🛠️ Instalação

1. Clone este repositório ou baixe os arquivos
2. Crie um ambiente virtual (recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install beautifulsoup4 requests lxml
   ```

## 📖 Como Usar

### Uso Básico

Execute o script principal:

```bash
python webscraper.py
```

O programa irá:

1. Extrair notícias dos sites configurados
2. Exibir as manchetes e URLs no terminal
3. Salvar as notícias em um arquivo `noticias.txt`

### Uso Programático

Você também pode usar a classe `NewsScraper` em seus próprios scripts:

```python
from webscraper import NewsScraper

# Criar o scraper
scraper = NewsScraper(delay=1.0)

# Extrair notícias de todos os sites
noticias = scraper.get_all_news()

# Exibir as notícias
scraper.display_news(noticias)

# Ou extrair de um site específico
noticias_g1 = scraper.extract_news_from_g1()
```

## 🏗️ Estrutura do Código

### Classe NewsScraper

- `__init__(delay)`: Inicializa o scraper com delay entre requisições
- `fetch_page(url)`: Baixa uma página e retorna objeto BeautifulSoup
- `extract_news_from_g1()`: Extrai notícias do G1
- `extract_news_from_uol()`: Extrai notícias do UOL
- `extract_news_from_folha()`: Extrai notícias da Folha de S.Paulo
- `get_all_news()`: Extrai notícias de todos os sites
- `display_news(news)`: Exibe notícias formatadas no terminal
- `save_to_file(news, filename)`: Salva notícias em arquivo

## 🔧 Personalização

### Adicionando Novos Sites

Para adicionar um novo site de notícias:

1. Crie um novo método `extract_news_from_seusite()`:

```python
def extract_news_from_seusite(self) -> List[Dict[str, str]]:
    url = "https://seusite.com/"
    soup = self.fetch_page(url)
    
    if not soup:
        return []
    
    news = []
    
    # Adapte os seletores CSS para o seu site
    links = soup.select('a.link-noticia')
    
    for link in links:
        title = link.get_text(strip=True)
        href = link.get('href')
        
        if title and href:
            full_url = urljoin(url, href)
            news.append({
                'titulo': title,
                'url': full_url,
                'fonte': 'Seu Site'
            })
    
    return news
```

2. Adicione o método à lista de extractors em `get_all_news()`:

```python
extractors = [
    self.extract_news_from_g1,
    self.extract_news_from_uol,
    self.extract_news_from_folha,
    self.extract_news_from_seusite  # Adicione aqui
]
```

### Configurando Delays

Ajuste o delay entre requisições para ser mais ou menos agressivo:

```python
# Mais rápido (cuidado para não ser bloqueado)
scraper = NewsScraper(delay=0.5)

# Mais respeitoso
scraper = NewsScraper(delay=2.0)
```

## ⚠️ Considerações Importantes

### Aspectos Legais e Éticos

- **Respeite os robots.txt**: Sempre verifique o arquivo robots.txt dos sites
- **Use delays**: Não sobrecarregue os servidores com muitas requisições
- **Termos de Uso**: Respeite os termos de uso dos sites
- **Uso Pessoal**: Este código é para fins educacionais e uso pessoal

### Limitações

- **Mudanças no Layout**: Sites podem mudar seus layouts, quebrando os seletores
- **Rate Limiting**: Sites podem limitar o número de requisições
- **JavaScript**: Sites que dependem de JavaScript podem não funcionar
- **Anti-Bot**: Alguns sites têm proteções contra bots

## 🛡️ Tratamento de Erros

O scraper inclui tratamento robusto de erros:

- **Timeouts**: Requisições têm timeout de 10 segundos
- **Exceções HTTP**: Trata erros de rede e status HTTP
- **Parsing**: Continua funcionando mesmo se um site falhar
- **Logging**: Registra todas as atividades e erros

## 📊 Exemplo de Saída

```
================================================================================
📰 NOTÍCIAS MAIS RECENTES (45 encontradas)
================================================================================

 1. [G1] Presidente anuncia novas medidas econômicas para 2025
    🔗 https://g1.globo.com/economia/noticia/2025/09/17/...

 2. [UOL] Copa do Mundo: Brasil confirma convocação
    🔗 https://www.uol.com.br/esporte/futebol/...

 3. [Folha de S.Paulo] Tecnologia brasileira ganha destaque internacional
    🔗 https://www1.folha.uol.com.br/tec/...
```

## 🤝 Contribuindo

Sinta-se à vontade para:

- Reportar bugs
- Sugerir melhorias
- Adicionar novos sites
- Melhorar a documentação

## 📝 Licença

Este projeto é de código aberto para fins educacionais.

---

**Desenvolvido com ❤️ para ajudar pessoas a se manterem informadas!**
