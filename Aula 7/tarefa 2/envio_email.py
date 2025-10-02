import base64
import os
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from autenticacao_google import obter_servico_gmail


def criar_mensagem_com_anexo(
    remetente, destinatario, assunto, corpo_texto, arquivo_anexo
):
    """
    Cria uma mensagem de e-mail com anexo em formato MIME.
    """
    # Criar mensagem MIME
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    # Adicionar corpo do e-mail (suporta HTML)
    corpo = MIMEText(corpo_texto, "html")
    mensagem.attach(corpo)

    # Adicionar anexo se fornecido
    if arquivo_anexo and os.path.exists(arquivo_anexo):
        # Detectar tipo MIME do arquivo
        tipo_mime, _ = mimetypes.guess_type(arquivo_anexo)

        if tipo_mime is None:
            tipo_mime = "application/octet-stream"

        tipo_principal, subtipo = tipo_mime.split("/", 1)

        # Ler o arquivo
        with open(arquivo_anexo, "rb") as arquivo:
            anexo = MIMEBase(tipo_principal, subtipo)
            anexo.set_payload(arquivo.read())

        # Codificar em base64
        encoders.encode_base64(anexo)

        # Adicionar cabeçalho
        nome_arquivo = os.path.basename(arquivo_anexo)
        anexo.add_header("Content-Disposition", f"attachment; filename={nome_arquivo}")

        mensagem.attach(anexo)

    # Codificar mensagem em base64
    mensagem_raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode()

    return {"raw": mensagem_raw}


def enviar_email(destinatario, assunto, corpo_texto, arquivo_anexo=None):
    """
    Envia um e-mail via Gmail API.
    """
    try:
        # Obter serviço do Gmail
        service = obter_servico_gmail()

        # Obter perfil do usuário para usar como remetente
        profile = service.users().getProfile(userId="me").execute()
        remetente = profile["emailAddress"]

        print(f"\n📧 Preparando e-mail...")
        print(f"   De: {remetente}")
        print(f"   Para: {destinatario}")
        print(f"   Assunto: {assunto}")

        if arquivo_anexo:
            nome_arquivo = os.path.basename(arquivo_anexo)
            tamanho_kb = os.path.getsize(arquivo_anexo) / 1024
            print(f"   Anexo: {nome_arquivo} ({tamanho_kb:.1f} KB)")

        # Criar mensagem
        mensagem = criar_mensagem_com_anexo(
            remetente, destinatario, assunto, corpo_texto, arquivo_anexo
        )

        # Enviar mensagem
        print(f"\n📤 Enviando e-mail...")
        resultado = (
            service.users().messages().send(userId="me", body=mensagem).execute()
        )

        print(f"\n✅ E-mail enviado com sucesso!")
        print(f"   ID da mensagem: {resultado['id']}")

        return resultado

    except Exception as e:
        print(f"\n❌ Erro ao enviar e-mail: {e}")
        raise


def gerar_corpo_email_mapa(municipios_info, arquivo_mapa):
    """
    Gera o corpo HTML do e-mail com informações sobre o mapa.
    """
    # Cabeçalho
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
            .municipio {
                background-color: #f5f5f5;
                padding: 10px;
                margin: 10px 0;
                border-left: 4px solid #4285f4;
                border-radius: 3px;
            }
            .footer {
                margin-top: 30px;
                padding: 20px;
                background-color: #f5f5f5;
                border-radius: 5px;
                font-size: 12px;
                color: #666;
            }
            .info {
                background-color: #e8f0fe;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🗺️ Mapa de Municípios Brasileiros</h1>
            <p>Gerado pela API do IBGE</p>
        </div>
        
        <div class="content">
            <p>Olá!</p>
            
            <p>Segue em anexo o mapa interativo com os municípios selecionados.</p>
    """

    # Informações dos municípios
    if municipios_info:
        html += f"""
            <div class="info">
                <h3>📍 Municípios incluídos no mapa ({len(municipios_info)}):</h3>
        """

        for i, info in enumerate(municipios_info, 1):
            nome = info.get("nome", "N/D")
            uf = info.get("uf", "")
            codigo = info.get("codigo", "N/D")
            pib_pc = info.get("pib_per_capita")

            html += f"""
                <div class="municipio">
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
        """

    # Instruções
    html += """
            <div class="info">
                <h3>📂 Como visualizar o mapa:</h3>
                <ol>
                    <li>Baixe o arquivo HTML anexado</li>
                    <li>Abra o arquivo no seu navegador (Chrome, Firefox, Safari, etc.)</li>
                    <li>Interaja com o mapa:
                        <ul>
                            <li>Passe o mouse sobre os polígonos para ver detalhes</li>
                            <li>Use os controles de zoom e navegação</li>
                            <li>Ative/desative camadas no controle superior direito</li>
                        </ul>
                    </li>
                </ol>
            </div>
            
            <h3>ℹ️ Sobre os dados:</h3>
            <ul>
                <li><strong>Malhas geográficas:</strong> API de Malhas do IBGE (versão 4)</li>
                <li><strong>PIB per capita:</strong> API SIDRA - Tabela 5938 (ano 2021)</li>
                <li><strong>Formato:</strong> GeoJSON processado com Folium</li>
            </ul>
            
            <p>O mapa é totalmente interativo e pode ser visualizado offline após o download.</p>
        </div>
        
        <div class="footer">
            <p><strong>🤖 E-mail gerado automaticamente</strong></p>
            <p>Sistema de Visualização de Municípios - APIs do IBGE</p>
            <p>Desenvolvido como parte do projeto de integração com APIs</p>
        </div>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    """
    Teste do módulo de envio de e-mail.
    """
    print("=" * 80)
    print("TESTE DE ENVIO DE E-MAIL")
    print("=" * 80)
    print()

    # Solicitar informações
    destinatario = input("Digite o e-mail do destinatário: ").strip()

    if not destinatario:
        print("❌ E-mail do destinatário é obrigatório!")
        exit(1)

    # E-mail de teste simples
    assunto = "🗺️ Teste - Sistema de Mapas IBGE"
    corpo = """
    <html>
    <body>
        <h2>Teste de Envio de E-mail</h2>
        <p>Este é um e-mail de teste do sistema de envio via Gmail API.</p>
        <p>Se você recebeu este e-mail, significa que o sistema está funcionando corretamente! ✅</p>
        <hr>
        <p><small>E-mail enviado automaticamente pelo sistema de visualização de municípios.</small></p>
    </body>
    </html>
    """

    try:
        print("\n" + "=" * 80)
        enviar_email(destinatario, assunto, corpo)
        print("=" * 80)
        print("\n🎉 Teste concluído! Verifique a caixa de entrada do destinatário.")

    except Exception as e:
        print("\n" + "=" * 80)
        print(f"❌ Erro no teste: {e}")
        print("=" * 80)
