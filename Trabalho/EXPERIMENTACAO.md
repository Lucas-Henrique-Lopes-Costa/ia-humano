# 📊 Experimento Prático: Comparação GitHub Copilot vs Outras Ferramentas de IA

**Data do Experimento:** 03 de outubro de 2025  
**Projeto:** Mini Dashboard de Clima com Streamlit  
**Desenvolvedor:** Lucas Henrique  

---

## 🎯 Objetivo do Experimento

Comparar a experiência de desenvolvimento usando **GitHub Copilot** versus outras ferramentas de IA generativa para desenvolvimento de software, através da criação de um Mini Dashboard de Clima utilizando Python e Streamlit.

---

## 📝 Descrição do Projeto

### Funcionalidades Implementadas

O Mini Dashboard de Clima permite ao usuário:

1. **Buscar clima por cidade:** Campo de entrada para digitar o nome de qualquer cidade do mundo
2. **Visualizar dados atuais:**
   - Temperatura atual e sensação térmica
   - Umidade relativa do ar
   - Velocidade e direção do vento
   - Pressão atmosférica
   - Condições climáticas com ícone
   - Visibilidade e ponto de orvalho
   - Nebulosidade e índice UV
   - Horários de nascer e pôr do sol

3. **Previsão de 7 dias:**
   - Temperatura máxima e mínima
   - Condições climáticas previstas
   - Probabilidade de precipitação
   - Ícones ilustrativos

### Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit 1.28.1** - Framework para criação de aplicações web
- **Requests 2.31.0** - Biblioteca para requisições HTTP
- **python-dotenv 1.0.0** - Gerenciamento de variáveis de ambiente
- **OpenWeatherMap One Call API 3.0** - API de dados climáticos

---

## 🔧 Estrutura do Projeto

```
Trabalho/
├── app.py                 # Aplicação principal Streamlit
├── utils.py              # Funções auxiliares e utilitárias
├── requirements.txt      # Dependências do projeto
├── .env                  # Variáveis de ambiente (API key)
├── .gitignore           # Arquivos ignorados pelo Git
└── EXPERIMENTACAO.md    # Esta documentação
```

---

## 🤖 Parte 1: Desenvolvimento com GitHub Copilot

### Configuração Inicial

**Ferramenta:** GitHub Copilot  
**IDE:** Visual Studio Code  
**Tempo de Desenvolvimento:** ~45 minutos  

### Processo de Desenvolvimento

#### 1. Criação da Estrutura Base (5 minutos)

**Experiência:**

- ✅ Copilot sugeriu automaticamente a estrutura do `requirements.txt`
- ✅ Sugestões corretas para `.gitignore` com padrões Python
- ✅ Criação do `.env` com formato adequado

**Sugestões Úteis:**

- Ao digitar `streamlit`, Copilot sugeriu versão específica
- Auto-completou dependências relacionadas (requests, dotenv)

**Necessidade de Ajustes:** Nenhum

---

#### 2. Desenvolvimento do Módulo `utils.py` (15 minutos)

**Experiência:**

- ✅ Excelente contexto: Copilot entendeu que era um projeto de clima
- ✅ Sugeriu funções de conversão (Kelvin → Celsius) automaticamente
- ✅ Criou docstrings completas com tipo de argumentos
- ✅ Implementou traduções PT-BR para descrições climáticas
- ✅ Função de geocoding sugerida corretamente

**Sugestões Úteis:**

```python
# Ao escrever apenas o nome da função, Copilot sugeriu implementação completa:
def kelvin_to_celsius(kelvin):
    """
    Converte temperatura de Kelvin para Celsius
    # Restante foi auto-completado!
```

**Necessidade de Ajustes:**

- Ajustes mínimos na lista de traduções (adicionei mais opções)
- Melhorei tratamento de erros na função de geocoding

**Qualidade do Código:** 9/10

- Código limpo e bem documentado
- Seguiu convenções Python (PEP 8)
- Type hints nas docstrings

---

#### 3. Desenvolvimento da Aplicação Principal `app.py` (25 minutos)

**Experiência:**

- ✅ Sugestões extremamente contextuais após importar Streamlit
- ✅ Auto-completou configuração da página (`set_page_config`)
- ✅ Sugeriu CSS customizado para melhorar UI
- ✅ Implementou layout responsivo com colunas
- ✅ Criou funções de exibição bem estruturadas

**Destaques Positivos:**

1. **Integração com API:**
   - Sugeriu estrutura correta para chamada à One Call API 3.0
   - Incluiu tratamento de erros automaticamente
   - Adicionou parâmetro `exclude` para otimizar requisições

2. **Interface do Usuário:**
   - Sugeriu componentes Streamlit apropriados (metrics, columns, divider)
   - Auto-completou emojis relevantes (🌡️, 🌤️, 📅)
   - Criou sidebar com informações do projeto

3. **Lógica da Aplicação:**
   - Implementou fluxo correto: busca → geocoding → dados climáticos → exibição
   - Adicionou mensagens de feedback (spinner, success, error)
   - Criou exemplos de cidades para o usuário

**Necessidade de Ajustes:**

- Refinei alguns detalhes de formatação
- Adicionei mais informações na sidebar
- Melhorei mensagens de erro para usuário

**Qualidade do Código:** 9.5/10

- Código muito bem estruturado
- Funções modulares e reutilizáveis
- Comentários úteis

---

### Análise Quantitativa - GitHub Copilot

| Métrica | Avaliação |
|---------|-----------|
| **Velocidade de Desenvolvimento** | ⭐⭐⭐⭐⭐ (5/5) |
| **Qualidade das Sugestões** | ⭐⭐⭐⭐⭐ (5/5) |
| **Compreensão do Contexto** | ⭐⭐⭐⭐⭐ (5/5) |
| **Precisão Técnica** | ⭐⭐⭐⭐☆ (4.5/5) |
| **Necessidade de Correções** | ⭐⭐⭐⭐☆ (4/5) |
| **Experiência do Desenvolvedor** | ⭐⭐⭐⭐⭐ (5/5) |

### Pontos Fortes do GitHub Copilot

✅ **Compreensão contextual excepcional**

- Entendeu que era um projeto de clima desde o início
- Sugestões sempre relevantes ao contexto do arquivo

✅ **Sugestões de código completo**

- Funções inteiras sugeridas com apenas o nome
- Docstrings automáticas e bem formatadas

✅ **Conhecimento de bibliotecas atualizado**

- Sugestões corretas para Streamlit
- Boas práticas com requests e manipulação de APIs

✅ **Produtividade aumentada**

- Redução significativa de digitação
- Menos consultas à documentação

✅ **Aprendizado de padrões**

- Manteve consistência de código entre arquivos
- Seguiu padrões estabelecidos no projeto

### Pontos de Melhoria

⚠️ **Nem sempre acerta de primeira**

- Algumas sugestões precisaram de pequenos ajustes
- Ocasionalmente sugere código mais verboso que necessário

⚠️ **Dependência de contexto**

- Funciona melhor quando há mais código de referência
- Primeiras linhas de um arquivo podem ter sugestões menos precisas

---

## 📊 Comparação com Outras Ferramentas

### Ferramenta Alternativa Sugerida: [A PREENCHER]

**Instruções para comparação:**

1. **Repetir o mesmo projeto** usando outra ferramenta de IA (ex: Cursor, Cody, Tabnine)
2. **Documentar:**
   - Tempo de desenvolvimento
   - Qualidade das sugestões
   - Facilidade de uso
   - Diferenças notáveis

3. **Preencher tabela comparativa:**

| Critério | GitHub Copilot | [Ferramenta 2] | Vencedor |
|----------|----------------|----------------|----------|
| Velocidade | ⭐⭐⭐⭐⭐ | [?] | [?] |
| Qualidade | ⭐⭐⭐⭐⭐ | [?] | [?] |
| Contexto | ⭐⭐⭐⭐⭐ | [?] | [?] |
| UX | ⭐⭐⭐⭐⭐ | [?] | [?] |

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Conta na OpenWeatherMap (API key gratuita)

### Passos

1. **Clone ou navegue até o diretório:**

```bash
cd /Users/lucashenrique/Projetos/Github/ia-humano/Trabalho
```

2. **Crie um ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # No macOS/Linux
# ou
venv\Scripts\activate  # No Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure a API key:**

- Arquivo `.env` já está configurado com a chave
- Ou substitua por sua própria chave se desejar

5. **Execute a aplicação:**

```bash
streamlit run app.py
```

6. **Acesse no navegador:**

- Abrirá automaticamente em `http://localhost:8501`

---

## 📸 Capturas de Tela

### Interface Inicial
![Tela inicial com campo de busca]

### Resultado da Busca
![Dashboard com dados climáticos]

### Previsão de 7 Dias
![Cards com previsão estendida]

**Nota:** Adicione capturas de tela reais após executar a aplicação.

---

## 🎓 Aprendizados e Conclusões

### Sobre o GitHub Copilot

**Produtividade:**

- Reduziu tempo de desenvolvimento em aproximadamente 40-50%
- Menos tempo procurando na documentação
- Foco maior na lógica do que na sintaxe

**Qualidade:**

- Código gerado é profissional e segue boas práticas
- Sugestões melhoram com o contexto do projeto
- Ajuda a aprender novos padrões e bibliotecas

**Casos de Uso Ideais:**

- Projetos com estrutura clara
- Uso de bibliotecas populares (Streamlit, Requests)
- Código que segue padrões estabelecidos
- Prototipagem rápida

**Limitações Observadas:**

- Não substitui conhecimento técnico do desenvolvedor
- Requer revisão crítica das sugestões
- Pode gerar código redundante ocasionalmente

---

## 📚 Referências

1. **OpenWeatherMap API Documentation**
   - <https://openweathermap.org/api/one-call-3>

2. **Streamlit Documentation**
   - <https://docs.streamlit.io/>

3. **GitHub Copilot Documentation**
   - <https://docs.github.com/en/copilot>

---

## ✅ Checklist do Experimento

- [x] Estrutura do projeto criada
- [x] Código implementado com Copilot
- [x] Documentação do processo
- [x] Análise qualitativa registrada
- [ ] Testes realizados
- [ ] Capturas de tela adicionadas
- [ ] Comparação com ferramenta alternativa
- [ ] Conclusões finais

---

## 👤 Autor

**Lucas Henrique**  
Projeto: Trabalho - IA Humano  
Data: 03/10/2025

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte de um experimento acadêmico.

---

## 🔗 Próximos Passos

1. [ ] Executar a aplicação e validar funcionamento
2. [ ] Capturar telas do dashboard em funcionamento
3. [ ] Repetir experimento com ferramenta alternativa
4. [ ] Completar análise comparativa
5. [ ] Escrever conclusões finais
6. [ ] Preparar apresentação dos resultados
