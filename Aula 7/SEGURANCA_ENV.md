# 🔐 Segurança: Uso de Variáveis de Ambiente

## ✅ Implementação Concluída

As **chaves de API** foram movidas do código para arquivos `.env` seguindo boas práticas de segurança.

---

## 🎯 Por que usar .env?

### ❌ Antes (INSEGURO)
```python
# API key exposta no código
GEMINI_API_KEY = "AIzaSyDpPJJU4nC5F0il9oTcNDTw0NbsPiCtXQc"
```

**Problemas:**
- ❌ Chave exposta no código-fonte
- ❌ Risco ao commitar no Git
- ❌ Difícil trocar chaves por ambiente (dev/prod)
- ❌ Compartilhar código compartilha a chave

### ✅ Depois (SEGURO)
```python
import os
from dotenv import load_dotenv

# Carregar do arquivo .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

**Vantagens:**
- ✅ Chave protegida em arquivo separado
- ✅ `.env` está no `.gitignore`
- ✅ Fácil trocar chaves sem alterar código
- ✅ Pode compartilhar código sem expor chaves

---

## 📁 Estrutura de Arquivos

```
tarefa 2/
├── .env                    # Arquivo com chaves (NÃO commitado)
├── .env.example            # Exemplo sem chaves (commitado)
├── .gitignore              # Ignora .env e credentials.json
├── gerador_email_gemini.py # Usa load_dotenv()
└── ...

tarefa 3/
├── .env                    # Arquivo com chaves (NÃO commitado)
├── .env.example            # Exemplo sem chaves (commitado)
├── gerador_email_gemini.py # Usa load_dotenv()
└── ...
```

---

## 📝 Conteúdo dos Arquivos

### `.env` (NÃO commitar)
```env
# Configurações de API Keys
# ATENÇÃO: Este arquivo não deve ser commitado no Git!

# Google Gemini API Key
GEMINI_API_KEY=AIzaSyDpPJJU4nC5F0il9oTcNDTw0NbsPiCtXQc
```

### `.env.example` (Commitar)
```env
# Arquivo de exemplo para configuração de variáveis de ambiente
# Copie este arquivo para .env e preencha com suas próprias chaves

# Google Gemini API Key
# Obtenha sua chave em: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=sua_chave_aqui
```

### `.gitignore`
```
/credentials.json
.env
```

---

## 🔧 Como o Código Foi Atualizado

### Mudanças em `gerador_email_gemini.py`

**Antes:**
```python
import google.generativeai as genai

# Configurar API Key do Gemini
GEMINI_API_KEY = "AIzaSyDpPJJU4nC5F0il9oTcNDTw0NbsPiCtXQc"
```

**Depois:**
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar API Key do Gemini a partir do .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY não encontrada! "
        "Por favor, configure a chave no arquivo .env"
    )
```

---

## 📦 Dependência Adicionada

### `requirements.txt`
```txt
requests
folium
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
google-generativeai
python-dotenv          # ← NOVA DEPENDÊNCIA
```

### Instalação
```bash
pip install python-dotenv
```

ou

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Usar

### 1. Para quem já tem o projeto

Se você já tem o código, basta:

```bash
# Já tem o .env? Então só precisa instalar a biblioteca
pip install python-dotenv

# Testar
cd "tarefa 3"
python gerador_email_gemini.py
```

### 2. Para quem está clonando o repositório

```bash
# 1. Clonar o repositório
git clone <repo>
cd "Aula 7"

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar arquivo .env a partir do exemplo
cd "tarefa 3"
cp .env.example .env

# 4. Editar o .env e colocar sua chave
nano .env  # ou vim, vscode, etc.

# 5. Testar
python gerador_email_gemini.py
```

---

## 🛡️ Validação de Segurança

O código agora valida se a chave existe:

```python
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY não encontrada! "
        "Por favor, configure a chave no arquivo .env"
    )
```

**Se esquecer de criar o `.env`, verá:**
```
ValueError: GEMINI_API_KEY não encontrada! 
Por favor, configure a chave no arquivo .env
```

---

## 📋 Checklist de Segurança

- [x] Chaves removidas do código-fonte
- [x] Arquivo `.env` criado
- [x] `.env` adicionado ao `.gitignore`
- [x] Arquivo `.env.example` criado para documentação
- [x] Código atualizado para usar `load_dotenv()`
- [x] Validação de chave ausente implementada
- [x] Dependência `python-dotenv` adicionada ao `requirements.txt`
- [x] Testes realizados e funcionando

---

## 🎓 Boas Práticas Aprendidas

1. **Nunca commitar chaves de API** no código-fonte
2. **Usar arquivos .env** para configurações sensíveis
3. **Sempre ter .env.example** para documentar variáveis necessárias
4. **Adicionar .env ao .gitignore** imediatamente
5. **Validar se variáveis existem** antes de usar
6. **Documentar no README** como configurar

---

## 📚 Referências

- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [12 Factor App - Config](https://12factor.net/config)
- [OWASP - Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

---

## ✅ Resultado

✨ **Agora o código está seguro e pode ser compartilhado publicamente sem expor as chaves de API!**

---

**Data:** 1 de outubro de 2025  
**Status:** ✅ Implementado e testado
