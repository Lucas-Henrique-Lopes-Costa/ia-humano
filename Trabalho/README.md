# 🌤️ Mini Dashboard de Clima

## � Sobre o Projeto

Mini Dashboard de Clima desenvolvido com **Streamlit** e **Python** como parte de um experimento prático para comparação de ferramentas de IA generativa (GitHub Copilot vs outras ferramentas).

### ✨ Funcionalidades

- 🌡️ **Clima Atual**: Temperatura, sensação térmica, umidade, pressão, velocidade do vento
- 📅 **Previsão de 5 dias**: Temperaturas, condições climáticas e probabilidade de chuva
- 🌍 **Busca por cidade**: Sistema de geocodificação para encontrar qualquer cidade do mundo
- 🎨 **Interface intuitiva**: Dashboard responsivo e fácil de usar
- ☀️ **Horários solares**: Nascer e pôr do sol
- 🌐 **Dados em português**: Descrições traduzidas

### 🔑 API Utilizada

Este projeto utiliza a **OpenWeatherMap API 2.5** (gratuita) com os seguintes endpoints:

- **Current Weather Data**: Dados climáticos atuais
- **5 Day / 3 Hour Forecast**: Previsão do tempo
- **Geocoding API**: Conversão de nomes de cidades em coordenadas

> **Nota**: Inicialmente o projeto foi desenvolvido para usar a One Call API 3.0, mas ela requer uma assinatura paga separada. A versão atual usa APIs gratuitas que fornecem funcionalidades similares.

---

## 📋 Pré-requisitos

- Python 3.8 ou superior instalado
- Conta na OpenWeatherMap (gratuita)
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### Passo 1: Criar Ambiente Virtual

```bash
# Navegue até o diretório do projeto
cd /Users/lucashenrique/Projetos/Github/ia-humano/Trabalho

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No macOS/Linux:
source venv/bin/activate

# No Windows:
# venv\Scripts\activate
```

### Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

Isso instalará:

- streamlit (framework web)
- requests (requisições HTTP)
- python-dotenv (variáveis de ambiente)

### Passo 3: Verificar Configuração

O arquivo `.env` já contém a API key:

```
OPENWEATHER_API_KEY=33c899551ef96e489457e0e8c5916b2a
```

Se quiser usar sua própria chave, crie uma conta gratuita em:
<https://openweathermap.org/api>

## ▶️ Executando a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em:
**<http://localhost:8501>**

## 🎯 Como Usar

1. Digite o nome de uma cidade no campo de busca
2. Pressione Enter ou clique em "Buscar"
3. Visualize:
   - Dados climáticos atuais
   - Previsão para os próximos 7 dias

### Exemplos de cidades

- São Paulo
- Rio de Janeiro
- London
- Tokyo
- New York
- Paris

## ⚠️ Solução de Problemas

### Erro: "API Key não encontrada"

- Verifique se o arquivo `.env` existe
- Confirme que a chave está no formato correto

### Erro: "Cidade não encontrada"

- Tente usar o nome em inglês (ex: "Sao Paulo")
- Verifique a ortografia
- Tente adicionar o país (ex: "Paris, FR")

### Erro de importação do Streamlit

```bash
pip install --upgrade streamlit
```

## 🛑 Parar a Aplicação

Pressione `Ctrl + C` no terminal onde o Streamlit está rodando.

## 📦 Estrutura de Arquivos

```
Trabalho/
├── app.py              # Aplicação principal
├── utils.py            # Funções auxiliares
├── requirements.txt    # Dependências
├── .env               # API key
├── README.md          # Este arquivo
└── EXPERIMENTACAO.md  # Documentação do experimento
```

## 🌐 API Utilizada

**OpenWeatherMap One Call API 3.0**

- Endpoint: <https://api.openweathermap.org/data/3.0/onecall>
- Documentação: <https://openweathermap.org/api/one-call-3>

### Dados Fornecidos

- Clima atual
- Previsão horária (48h)
- Previsão diária (7 dias)
- Alertas meteorológicos

## 📝 Notas

- A API gratuita permite 1.000 chamadas/dia
- Os dados são atualizados a cada 10 minutos
- Suporte a cidades de todo o mundo
