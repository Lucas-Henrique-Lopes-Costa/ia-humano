import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# Escopos necessários para Gmail e Drive
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",  # Enviar e-mails
    "https://www.googleapis.com/auth/gmail.modify",  # Modificar e-mails
]


def obter_credenciais(force_new=False):
    """
    Deve pegar as credenciais válidas para as APIs do Google. que estão no arquivo credentials.json
    """
    creds = None
    token_file = "token.pickle"
    credentials_file = "credentials.json"

    # Verificar se credentials.json existe
    if not os.path.exists(credentials_file):
        raise FileNotFoundError(
            f"\n❌ Arquivo '{credentials_file}' não encontrado!\n\n"
            "Por favor, faça o seguinte:\n"
            "1. Acesse: https://console.cloud.google.com/\n"
            "2. Crie um projeto ou selecione um existente\n"
            "3. Habilite a API do Gmail\n"
            "4. Crie credenciais OAuth 2.0\n"
            "5. Baixe o arquivo JSON e salve como 'credentials.json'\n"
        )

    # Tentar carregar token existente
    if os.path.exists(token_file) and not force_new:
        print("📂 Carregando token de autenticação existente...")
        with open(token_file, "rb") as token:
            creds = pickle.load(token)

    # Se não houver credenciais válidas, fazer login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando token de autenticação...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"⚠️  Erro ao renovar token: {e}")
                print("🔐 Solicitando nova autenticação...")
                creds = None

        if not creds:
            print("\n" + "=" * 80)
            print("🔐 AUTENTICAÇÃO NECESSÁRIA")
            print("=" * 80)
            print("\nVocê será redirecionado para o navegador para fazer login.")
            print("Escolha a conta do Google que deseja usar.")
            print("\nApós autorizar, você pode fechar a janela do navegador.")
            print("=" * 80)
            input("\nPressione ENTER para continuar...")

            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

            print("\n✅ Autenticação realizada com sucesso!")

        # Salvar credenciais para uso futuro
        print("💾 Salvando token de autenticação...")
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)
    else:
        print("✅ Token de autenticação válido encontrado!")

    return creds


def obter_servico_gmail():
    """
    Obtém o serviço da API do Gmail autenticado.
    """
    creds = obter_credenciais()
    service = build("gmail", "v1", credentials=creds)
    return service


def verificar_autenticacao():
    """
    Verifica se a autenticação está funcionando corretamente.
    """
    try:
        service = obter_servico_gmail()

        # Testar obtendo o perfil do usuário
        profile = service.users().getProfile(userId="me").execute()

        print("\n" + "=" * 80)
        print("✅ AUTENTICAÇÃO VERIFICADA COM SUCESSO!")
        print("=" * 80)
        print(f"\n📧 E-mail autenticado: {profile['emailAddress']}")
        print(f"📊 Total de mensagens: {profile.get('messagesTotal', 'N/D')}")
        print(f"📨 Total de threads: {profile.get('threadsTotal', 'N/D')}")
        print("\n" + "=" * 80)

        return True

    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERRO NA AUTENTICAÇÃO")
        print("=" * 80)
        print(f"\nErro: {e}")
        print("\n" + "=" * 80)
        return False


def limpar_autenticacao():
    """
    Remove o arquivo de token para forçar nova autenticação.
    """
    token_file = "token.pickle"

    if os.path.exists(token_file):
        os.remove(token_file)
        print(f"✅ Arquivo '{token_file}' removido com sucesso!")
        print("Na próxima execução, será solicitada nova autenticação.")
    else:
        print(f"ℹ️  Arquivo '{token_file}' não existe.")


if __name__ == "__main__":
    """
    Teste do módulo de autenticação.
    Execute: python autenticacao_google.py
    """
    import sys

    print("=" * 80)
    print("TESTE DE AUTENTICAÇÃO - APIs DO GOOGLE")
    print("=" * 80)
    print()

    if len(sys.argv) > 1 and sys.argv[1] == "--limpar":
        limpar_autenticacao()
    else:
        # Tentar autenticar e verificar
        try:
            if verificar_autenticacao():
                print("\n🎉 Tudo pronto para usar as APIs do Google!")
                print("\nVocê pode agora:")
                print("  • Enviar e-mails via Gmail")
                print("  • Ler mensagens")
                print("  • Gerenciar e-mails")
            else:
                print("\n⚠️  Há problemas com a autenticação.")
                print("\nDicas:")
                print("  • Verifique se o arquivo credentials.json está correto")
                print("  • Execute novamente para tentar autenticar")
                print("  • Use --limpar para forçar nova autenticação:")
                print("    python autenticacao_google.py --limpar")

        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
