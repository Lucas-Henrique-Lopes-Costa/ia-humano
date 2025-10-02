"""
Tarefa 3.3 - Gerador de Texto de E-mail com Gemini

Este módulo usa a API do Google Gemini para gerar
textos personalizados de e-mails com informações de municípios.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar API Key do Gemini a partir do .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY não encontrada! " "Por favor, configure a chave no arquivo .env"
    )


def configurar_gemini():
    """
    Configura a API do Gemini com a chave de autenticação.
    """
    genai.configure(api_key=GEMINI_API_KEY)
    print("✓ Gemini API configurada")


def gerar_texto_email_com_gemini(municipios_info):
    """
    Gera o texto do corpo do e-mail usando o Gemini.

    Args:
        municipios_info (list): Lista de dicionários com informações dos municípios:
            - nome: Nome do município
            - uf: Sigla do estado
            - codigo: Código IBGE
            - pib_per_capita: PIB per capita (opcional)

    Returns:
        str: Texto do e-mail gerado pelo Gemini em formato HTML
    """
    try:
        # Configurar Gemini
        configurar_gemini()

        # Preparar informações dos municípios para o prompt
        lista_municipios = []
        for info in municipios_info:
            nome_completo = f"{info['nome']}/{info['uf']}"

            if "pib_per_capita" in info and info["pib_per_capita"]:
                pib_formatado = f"R$ {info['pib_per_capita']:,.2f}"
                lista_municipios.append(
                    f"{nome_completo} (PIB per capita: {pib_formatado})"
                )
            else:
                lista_municipios.append(nome_completo)

        municipios_texto = ", ".join(lista_municipios[:-1])
        if len(lista_municipios) > 1:
            municipios_texto += f" e {lista_municipios[-1]}"
        else:
            municipios_texto = lista_municipios[0]

        # Criar prompt para o Gemini
        prompt = f"""
Escreva um e-mail formal e conciso apresentando um mapa interativo com polígonos geográficos e dados de PIB per capita dos seguintes municípios brasileiros:

{municipios_texto}

O e-mail deve:
1. Ter uma saudação formal
2. Explicar brevemente que se trata de um mapa interativo com dados do IBGE
3. Mencionar que os dados incluem polígonos geográficos e PIB per capita (quando disponível)
4. Instruir o destinatário a abrir o arquivo HTML anexado
5. Explicar que o mapa é interativo (pode passar o mouse sobre os polígonos)
6. Ter uma despedida profissional

IMPORTANTE: 
- O e-mail deve ser em português do Brasil
- Usar tom profissional mas amigável
- Ser conciso (máximo 3 parágrafos curtos)
- NÃO incluir tags HTML, apenas texto simples
- NÃO incluir assinatura (será adicionada automaticamente)
"""

        print("🤖 Gerando texto do e-mail com Gemini...")

        # Usar o modelo Gemini 2.5 Flash (versão mais recente disponível)
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Gerar conteúdo
        response = model.generate_content(prompt)

        texto_gerado = response.text.strip()

        print("✓ Texto gerado com sucesso!")

        # Converter o texto simples em HTML formatado
        html_corpo = converter_texto_para_html(texto_gerado, municipios_info)

        return html_corpo

    except Exception as e:
        print(f"⚠️  Erro ao gerar texto com Gemini: {e}")
        print("📝 Usando texto padrão...")

        # Fallback: usar texto padrão se houver erro
        return gerar_email_padrao(municipios_info)


def converter_texto_para_html(texto, municipios_info):
    """
    Converte o texto gerado pelo Gemini em HTML formatado.

    Args:
        texto (str): Texto gerado pelo Gemini
        municipios_info (list): Informações dos municípios

    Returns:
        str: HTML formatado
    """
    # Separar em parágrafos
    paragrafos = texto.strip().split("\n\n")

    # Construir HTML
    html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }
            .header {
                background-color: #4285f4;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px;
            }
            .content {
                padding: 20px;
            }
            .content p {
                margin: 15px 0;
            }
            .municipios-box {
                background-color: #e8f0fe;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                border-left: 4px solid #4285f4;
            }
            .municipio-item {
                background-color: white;
                padding: 10px;
                margin: 8px 0;
                border-radius: 3px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .footer {
                margin-top: 30px;
                padding: 20px;
                background-color: #f5f5f5;
                border-radius: 5px;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🗺️ Mapa de Municípios Brasileiros</h1>
            <p>Dados do IBGE - Instituto Brasileiro de Geografia e Estatística</p>
        </div>
        
        <div class="content">
    """

    # Adicionar parágrafos do texto gerado pelo Gemini
    for paragrafo in paragrafos:
        if paragrafo.strip():
            html += f"            <p>{paragrafo.strip()}</p>\n"

    # Adicionar box com informações detalhadas dos municípios
    html += """
            <div class="municipios-box">
                <h3>📍 Municípios incluídos no mapa:</h3>
    """

    for i, info in enumerate(municipios_info, 1):
        nome = info.get("nome", "N/D")
        uf = info.get("uf", "")
        codigo = info.get("codigo", "N/D")
        pib_pc = info.get("pib_per_capita")

        html += f"""
                <div class="municipio-item">
                    <strong>{i}. {nome}/{uf}</strong><br>
                    <small>Código IBGE: {codigo}</small>
        """

        if pib_pc:
            html += f"<br><small>💰 PIB per capita: R$ {pib_pc:,.2f}</small>"

        html += """
                </div>
        """

    html += """
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🤖 E-mail gerado automaticamente com IA</strong></p>
            <p>Texto criado por: Google Gemini 1.5 Flash</p>
            <p>Dados: API de Localidades, Malhas e SIDRA (IBGE)</p>
            <p>Sistema desenvolvido para demonstração de integração com APIs</p>
        </div>
    </body>
    </html>
    """

    return html


def gerar_email_padrao(municipios_info):
    """
    Gera um e-mail com texto padrão (fallback).

    Args:
        municipios_info (list): Informações dos municípios

    Returns:
        str: HTML do e-mail
    """
    # Preparar lista de municípios
    lista_municipios = []
    for info in municipios_info:
        nome_completo = f"{info['nome']}/{info['uf']}"
        lista_municipios.append(nome_completo)

    if len(lista_municipios) == 1:
        municipios_texto = lista_municipios[0]
    elif len(lista_municipios) == 2:
        municipios_texto = f"{lista_municipios[0]} e {lista_municipios[1]}"
    else:
        municipios_texto = (
            ", ".join(lista_municipios[:-1]) + f" e {lista_municipios[-1]}"
        )

    texto_padrao = f"""
Olá,

Segue em anexo o mapa interativo dos municípios {municipios_texto}, gerado a partir dos dados oficiais do IBGE (Instituto Brasileiro de Geografia e Estatística).

O mapa contém polígonos geográficos detalhados e informações de PIB per capita. Para visualizá-lo, basta abrir o arquivo HTML anexado em seu navegador. O mapa é totalmente interativo - você pode passar o mouse sobre os polígonos para ver os detalhes de cada município.

Atenciosamente.
    """.strip()

    return converter_texto_para_html(texto_padrao, municipios_info)


if __name__ == "__main__":
    """
    Teste do gerador de texto com Gemini
    """
    print("=" * 80)
    print("TESTE - GERADOR DE TEXTO COM GEMINI")
    print("=" * 80)

    # Dados de exemplo
    municipios_teste = [
        {"nome": "Lavras", "uf": "MG", "codigo": "3138203", "pib_per_capita": 27818.10},
        {
            "nome": "São Paulo",
            "uf": "SP",
            "codigo": "3550308",
            "pib_per_capita": 56370.00,
        },
    ]

    print("\n📊 Municípios de teste:")
    for m in municipios_teste:
        print(f"  • {m['nome']}/{m['uf']} - R$ {m['pib_per_capita']:,.2f}")

    print("\n" + "=" * 80)

    try:
        html_gerado = gerar_texto_email_com_gemini(municipios_teste)

        print("\n" + "=" * 80)
        print("✅ HTML gerado com sucesso!")
        print("=" * 80)

        # Salvar para visualização
        arquivo_teste = "teste_email_gemini.html"
        with open(arquivo_teste, "w", encoding="utf-8") as f:
            f.write(html_gerado)

        print(f"\n📄 HTML salvo em: {arquivo_teste}")
        print("🌐 Abra o arquivo no navegador para visualizar")

        # Mostrar preview do texto
        print("\n" + "=" * 80)
        print("PREVIEW DO TEXTO GERADO:")
        print("=" * 80)

        import re

        # Extrair apenas o texto dos parágrafos
        textos = re.findall(r"<p>(.*?)</p>", html_gerado, re.DOTALL)
        for texto in textos:
            print(f"\n{texto.strip()}")

    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback

        traceback.print_exc()
