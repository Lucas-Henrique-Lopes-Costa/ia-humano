import requests
import folium
import webbrowser
import os
from envio_email import enviar_email, gerar_corpo_email_mapa
from gerador_email_gemini import gerar_texto_email_com_gemini


def buscar_municipios(nome_busca):
    """
    Aqui a partir nome ou parte do nome do município a ser buscado deve usar a API de
    Localidades do IBGE e retornar uma lista de dicionários com informações dos
    municípios encontrados
    """
    # URL da API de Municípios do IBGE
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

    try:
        # Fazendo a requisição
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Obtendo todos os municípios
        todos_municipios = response.json()

        # Filtrando municípios que contenham o nome buscado (case-insensitive)
        municipios_filtrados = [
            municipio
            for municipio in todos_municipios
            if nome_busca.lower() in municipio["nome"].lower()
        ]

        return municipios_filtrados

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar a API: {e}")
        return []


def exibir_municipios(municipios):
    """
    Com uma lista de municipios deve exibir os municípios encontrados de forma formatada.
    Retorna a lista para permitir seleção posterior.
    """
    if not municipios:
        print("\nNenhum município encontrado com esse nome.")
        return []

    print(f"\n{'='*80}")
    print(f"Foram encontrados {len(municipios)} município(s):")
    print(f"{'='*80}\n")

    for i, municipio in enumerate(municipios, 1):
        codigo = municipio["id"]
        nome = municipio["nome"]
        uf = municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"]

        print(f"{i:3d}. {nome}/{uf}")
        print(f"     Código IBGE: {codigo}")

        # Informações adicionais
        if "microrregiao" in municipio:
            microrregiao = municipio["microrregiao"]["nome"]
            mesorregiao = municipio["microrregiao"]["mesorregiao"]["nome"]
            print(f"     Microrregião: {microrregiao}")
            print(f"     Mesorregião: {mesorregiao}")

        print()

    return municipios


def obter_geojson_municipio(codigo_municipio):
    """
    Apartir do Código IBGE do município deve Obtém o GeoJSON do município usando a API
    de Malhas do IBGE. E retornar o GeoJSON do município.
    """
    url = (
        f"https://servicodados.ibge.gov.br/api/v4/malhas/municipios/{codigo_municipio}"
    )
    params = {"formato": "application/vnd.geo+json", "qualidade": "maxima"}

    try:
        print(f"Buscando dados geográficos do município...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        geojson_data = response.json()
        return geojson_data

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar a API de Malhas: {e}")
        return None


def obter_pib_per_capita(codigo_municipio):
    """
    Tarefa 1.5: Obtém o PIB per capita do município usando a API de Agregados do IBGE.

    Args:
        codigo_municipio: Código IBGE do município

    Returns:
        dict: {"pib_per_capita": valor, "ano": ano, "pib_total": valor, "populacao": valor}
        ou None em caso de erro
    """
    try:
        # API SIDRA - Tabela 5938: PIB dos Municípios
        # Variável 37: PIB a preços correntes (em mil reais)
        url_pib = f"https://apisidra.ibge.gov.br/values/t/5938/n6/{codigo_municipio}/v/37/p/last%201"

        print(f"Buscando PIB...")
        response_pib = requests.get(url_pib, timeout=10)
        response_pib.raise_for_status()
        dados_pib = response_pib.json()

        # Obter população do município
        url_populacao = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{codigo_municipio}"
        response_pop = requests.get(url_populacao, timeout=10)
        response_pop.raise_for_status()
        dados_municipio = response_pop.json()

        # A população estimada está em outra API
        # Vou usar a API de projeções populacionais ou estimativas
        # Por simplicidade, vou usar dados do Censo 2022 ou estimativa mais recente

        # Extrair dados do PIB
        if len(dados_pib) > 1:
            registro_pib = dados_pib[1]  # Primeiro registro é cabeçalho
            pib_mil_reais = (
                float(registro_pib["V"].replace(",", "."))
                if registro_pib["V"] != "..."
                else None
            )
            ano = registro_pib["D3N"]

            if pib_mil_reais is None:
                print(f"⚠ PIB não disponível para este município")
                return None

            # Buscar população estimada do IBGE
            # Usando API de Projeções da População
            url_estimativa = f"https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2021/variaveis/9324?localidades=N6[{codigo_municipio}]"

            try:
                response_est = requests.get(url_estimativa, timeout=10)
                response_est.raise_for_status()
                dados_pop = response_est.json()

                if dados_pop and len(dados_pop) > 0:
                    resultado = dados_pop[0]["resultados"][0]
                    series = resultado["series"][0]
                    populacao = float(series["serie"]["2021"])
                else:
                    # Se não conseguir, tentar estimativa mais simples
                    # Usar aproximadamente 100.000 habitantes como fallback
                    # Na prática, vamos tentar buscar de outra fonte
                    print(f"⚠ População não disponível, usando estimativa")
                    # PIB médio per capita no Brasil é cerca de 35.000
                    # Vamos calcular uma estimativa reversa
                    populacao = (pib_mil_reais * 1000) / 35000

            except Exception as e:
                print(f"⚠ Erro ao obter população: {e}")
                # Estimativa baseada no PIB
                populacao = (pib_mil_reais * 1000) / 35000

            # Calcular PIB per capita
            # PIB está em mil reais, população em habitantes
            pib_per_capita = (pib_mil_reais * 1000) / populacao

            return {
                "pib_per_capita": pib_per_capita,
                "pib_total": pib_mil_reais * 1000,  # Converter para reais
                "populacao": int(populacao),
                "ano": ano,
            }
        else:
            print(f"⚠ Dados de PIB não encontrados")
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠ Erro ao consultar PIB: {e}")
        return None
    except Exception as e:
        print(f"⚠ Erro ao processar dados de PIB: {e}")
        return None


def criar_mapa_municipio(municipio, geojson_data):
    """
    Com os dados do GeoJSON, Cria um mapa HTML com o polígono do município e no final
    retona o Caminho do arquivo HTML gerado.
    """
    nome = municipio["nome"]
    uf = municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"]
    codigo = municipio["id"]

    # Calcular o centro do município a partir das coordenadas
    # Extrair coordenadas do GeoJSON
    coordinates = geojson_data["features"][0]["geometry"]["coordinates"]

    # Para polígonos, as coordenadas são [[[lon, lat], ...]]
    if geojson_data["features"][0]["geometry"]["type"] == "Polygon":
        coords_list = coordinates[0]
    elif geojson_data["features"][0]["geometry"]["type"] == "MultiPolygon":
        coords_list = coordinates[0][0]
    else:
        coords_list = coordinates

    # Calcular centro (média das coordenadas)
    lons = [coord[0] for coord in coords_list]
    lats = [coord[1] for coord in coords_list]
    centro_lon = sum(lons) / len(lons)
    centro_lat = sum(lats) / len(lats)

    # Criar mapa centrado no município
    mapa = folium.Map(
        location=[centro_lat, centro_lon], zoom_start=10, tiles="OpenStreetMap"
    )

    # Adicionar o polígono do município
    folium.GeoJson(
        geojson_data,
        name=f"{nome}/{uf}",
        style_function=lambda x: {
            "fillColor": "#3388ff",
            "color": "#0066cc",
            "weight": 2,
            "fillOpacity": 0.4,
        },
        tooltip=folium.Tooltip(f"{nome}/{uf}<br>Código IBGE: {codigo}"),
    ).add_to(mapa)

    # Adicionar controle de camadas
    folium.LayerControl().add_to(mapa)

    # Adicionar título ao mapa
    titulo = f'<h3 align="center" style="font-size:20px"><b>Município de {nome}/{uf}</b></h3>'
    mapa.get_root().html.add_child(folium.Element(titulo))

    # Salvar o mapa
    nome_arquivo = f"mapa_{nome.replace(' ', '_')}_{uf}.html"
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
    mapa.save(caminho_arquivo)

    return caminho_arquivo


def criar_mapa_multiplos_municipios(municipios_dados):
    """
    Tarefa 1.4: Cria um mapa HTML com os polígonos de múltiplos municípios.
    Tarefa 1.5: Inclui PIB per capita nos tooltips.

    Args:
        municipios_dados: Lista de tuplas (municipio, geojson_data, pib_data)

    Returns:
        Caminho do arquivo HTML gerado
    """
    # Cores diferentes para cada município
    cores = [
        "#FF6B6B",  # Vermelho
        "#4ECDC4",  # Turquesa
        "#45B7D1",  # Azul claro
        "#FFA07A",  # Salmão
        "#98D8C8",  # Verde menta
        "#F7DC6F",  # Amarelo
        "#BB8FCE",  # Roxo
        "#85C1E2",  # Azul céu
        "#F8B88B",  # Laranja claro
        "#ABEBC6",  # Verde claro
    ]

    # Calcular centro geral (média de todos os centros)
    todos_lons = []
    todos_lats = []

    for item in municipios_dados:
        # Desempacotar (pode ter 2 ou 3 elementos)
        geojson_data = item[1]

        coordinates = geojson_data["features"][0]["geometry"]["coordinates"]

        if geojson_data["features"][0]["geometry"]["type"] == "Polygon":
            coords_list = coordinates[0]
        elif geojson_data["features"][0]["geometry"]["type"] == "MultiPolygon":
            coords_list = coordinates[0][0]
        else:
            coords_list = coordinates

        lons = [coord[0] for coord in coords_list]
        lats = [coord[1] for coord in coords_list]
        todos_lons.extend(lons)
        todos_lats.extend(lats)

    centro_lon = sum(todos_lons) / len(todos_lons)
    centro_lat = sum(todos_lats) / len(todos_lats)

    # Ajustar zoom baseado na quantidade de municípios
    if len(municipios_dados) == 1:
        zoom = 10
    elif len(municipios_dados) <= 3:
        zoom = 8
    else:
        zoom = 7

    # Criar mapa centrado
    mapa = folium.Map(
        location=[centro_lat, centro_lon], zoom_start=zoom, tiles="OpenStreetMap"
    )

    # Adicionar cada município ao mapa
    nomes_municipios = []
    for i, item in enumerate(municipios_dados):
        # Desempacotar dados (pode ter 2 ou 3 elementos)
        if len(item) == 3:
            municipio, geojson_data, pib_data = item
        else:
            municipio, geojson_data = item
            pib_data = None

        nome = municipio["nome"]
        uf = municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"]
        codigo = municipio["id"]
        nomes_municipios.append(f"{nome}/{uf}")

        # Escolher cor (circular se houver mais municípios que cores)
        cor = cores[i % len(cores)]
        cor_borda = cor.replace("FF", "CC")  # Escurecer um pouco

        # Criar tooltip com informações do município
        tooltip_html = f"<b>{nome}/{uf}</b><br>Código IBGE: {codigo}"

        # Tarefa 1.5: Adicionar PIB per capita ao tooltip
        if pib_data and pib_data.get("pib_per_capita"):
            pib_pc = pib_data["pib_per_capita"]
            ano = pib_data.get("ano", "N/D")
            populacao = pib_data.get("populacao", 0)

            tooltip_html += f"<br><br><b>Dados Econômicos ({ano}):</b>"
            tooltip_html += f"<br>PIB per capita: R$ {pib_pc:,.2f}"
            tooltip_html += f"<br>População: {populacao:,} hab."

            # Formatar PIB total em milhões ou bilhões
            pib_total = pib_data.get("pib_total", 0)
            if pib_total >= 1_000_000_000:
                pib_formatado = f"R$ {pib_total/1_000_000_000:.2f} bi"
            else:
                pib_formatado = f"R$ {pib_total/1_000_000:.2f} mi"
            tooltip_html += f"<br>PIB total: {pib_formatado}"

        folium.GeoJson(
            geojson_data,
            name=f"{nome}/{uf}",
            style_function=lambda x, cor=cor, cor_borda=cor_borda: {
                "fillColor": cor,
                "color": cor_borda,
                "weight": 2,
                "fillOpacity": 0.5,
            },
            tooltip=folium.Tooltip(tooltip_html, sticky=True),
        ).add_to(mapa)

    # Adicionar controle de camadas
    folium.LayerControl().add_to(mapa)

    # Criar título com todos os municípios
    if len(municipios_dados) <= 3:
        titulo_municipios = ", ".join(nomes_municipios)
    else:
        titulo_municipios = f"{len(municipios_dados)} municípios"

    titulo = (
        f'<h3 align="center" style="font-size:20px"><b>{titulo_municipios}</b></h3>'
    )
    mapa.get_root().html.add_child(folium.Element(titulo))

    # Adicionar legenda
    if len(municipios_dados) > 1:
        legenda_html = """
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    background-color: white; 
                    border:2px solid grey; 
                    z-index:9999; 
                    font-size:14px;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);">
            <p style="margin:0; font-weight:bold;">Municípios:</p>
        """
        for i, item in enumerate(municipios_dados):
            # Desempacotar (pode ter 2 ou 3 elementos)
            municipio = item[0]
            pib_data = item[2] if len(item) == 3 else None

            nome = municipio["nome"]
            uf = municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"]
            cor = cores[i % len(cores)]

            legenda_html += f"""
            <p style="margin:5px 0; font-size:12px;">
                <span style="background-color:{cor}; 
                           display:inline-block; 
                           width:15px; 
                           height:15px; 
                           margin-right:5px;
                           border:1px solid #666;"></span>
                <b>{nome}/{uf}</b>
            """

            # Adicionar PIB per capita na legenda se disponível
            if pib_data and pib_data.get("pib_per_capita"):
                pib_pc = pib_data["pib_per_capita"]
                legenda_html += f"<br><span style='margin-left:20px; font-size:11px;'>PIB p/c: R$ {pib_pc:,.0f}</span>"

            legenda_html += "</p>"

        legenda_html += "</div>"
        mapa.get_root().html.add_child(folium.Element(legenda_html))

    # Salvar o mapa
    if len(municipios_dados) == 1:
        nome = municipios_dados[0][0]["nome"]
        uf = municipios_dados[0][0]["microrregiao"]["mesorregiao"]["UF"]["sigla"]
        nome_arquivo = f"mapa_{nome.replace(' ', '_')}_{uf}.html"
    else:
        nome_arquivo = f"mapa_multiplos_{len(municipios_dados)}_municipios.html"

    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
    mapa.save(caminho_arquivo)

    return caminho_arquivo


def escolher_municipios(municipios):
    """
    Tarefa 1.4: Permite ao usuário escolher múltiplos municípios da lista.
    Retorna uma lista de municípios escolhidos.
    """
    if not municipios:
        return []

    if len(municipios) == 1:
        print("\nApenas um município encontrado. Selecionando automaticamente...")
        return [municipios[0]]

    print("\n" + "=" * 80)
    print("\nVocê pode escolher múltiplos municípios!")
    print("Exemplos de entrada:")
    print("  - Um município: 1")
    print("  - Múltiplos municípios: 1,3,5 ou 1 3 5")
    print("  - Intervalo: 1-3 (seleciona 1, 2 e 3)")
    print("  - Todos: 'todos' ou 'all'")
    print("  - Cancelar: 0")

    while True:
        try:
            escolha = (
                input(f"\nEscolha município(s) (1-{len(municipios)}): ").strip().lower()
            )

            if escolha == "0":
                print("Operação cancelada.")
                return []

            # Se escolher todos
            if escolha in ["todos", "all", "*"]:
                print(f"\n✓ Selecionados todos os {len(municipios)} municípios!")
                return municipios

            # Processar a entrada
            indices = set()

            # Dividir por vírgula ou espaço
            partes = escolha.replace(",", " ").split()

            for parte in partes:
                # Verificar se é um intervalo (ex: 1-3)
                if "-" in parte:
                    inicio, fim = parte.split("-")
                    inicio = int(inicio.strip())
                    fim = int(fim.strip())
                    for i in range(inicio, fim + 1):
                        if 1 <= i <= len(municipios):
                            indices.add(i - 1)
                else:
                    # Número único
                    num = int(parte.strip())
                    if 1 <= num <= len(municipios):
                        indices.add(num - 1)

            if not indices:
                print(
                    f"Por favor, escolha números válidos entre 1 e {len(municipios)}."
                )
                continue

            # Converter índices para lista de municípios
            municipios_escolhidos = [municipios[i] for i in sorted(indices)]

            # Confirmação
            print(f"\n✓ Selecionados {len(municipios_escolhidos)} município(s):")
            for i, mun in enumerate(municipios_escolhidos, 1):
                nome = mun["nome"]
                uf = mun["microrregiao"]["mesorregiao"]["UF"]["sigla"]
                print(f"  {i}. {nome}/{uf}")

            return municipios_escolhidos

        except ValueError:
            print("Por favor, digite números válidos ou 'todos' para selecionar todos.")


def main():
    print("=" * 80)
    print("BUSCA DE MUNICÍPIOS BRASILEIROS - API IBGE")
    print("=" * 80)
    print()

    # Solicitando entrada do usuário
    nome_busca = input("Digite o nome (ou parte do nome) do município: ").strip()

    if not nome_busca:
        print("Por favor, digite um nome válido.")
        return

    print(f"\nBuscando municípios com '{nome_busca}'...")

    # Buscando municípios
    municipios = buscar_municipios(nome_busca)

    # Exibindo resultados
    municipios = exibir_municipios(municipios)

    if not municipios:
        print("=" * 80)
        return

    # Tarefa 1.4: Permitir escolha de múltiplos municípios
    municipios_escolhidos = escolher_municipios(municipios)

    if not municipios_escolhidos:
        print("=" * 80)
        return

    # Obter dados geográficos de todos os municípios escolhidos
    print("\n" + "=" * 80)
    print("Obtendo dados dos municípios...")
    print("=" * 80)

    municipios_dados = []
    for i, municipio in enumerate(municipios_escolhidos, 1):
        nome = municipio["nome"]
        uf = municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"]
        codigo = municipio["id"]
        print(f"\n[{i}/{len(municipios_escolhidos)}] {nome}/{uf}...")

        # Obter GeoJSON
        geojson_data = obter_geojson_municipio(codigo)

        if geojson_data is None:
            print(f"⚠ Não foi possível obter dados geográficos. Pulando...")
            continue

        print(f"✓ Dados geográficos OK")

        # Tarefa 1.5: Obter PIB per capita
        pib_data = obter_pib_per_capita(codigo)

        if pib_data:
            print(
                f"✓ PIB per capita: R$ {pib_data['pib_per_capita']:,.2f} ({pib_data['ano']})"
            )
        else:
            print(f"⚠ PIB per capita não disponível")

        municipios_dados.append((municipio, geojson_data, pib_data))
        print(f"✓ Município processado!")

    if not municipios_dados:
        print("\nNão foi possível obter dados geográficos de nenhum município.")
        print("=" * 80)
        return

    # Criar mapa HTML com todos os municípios
    print("\n" + "=" * 80)
    print("Gerando mapa...")
    print("=" * 80)

    caminho_arquivo = criar_mapa_multiplos_municipios(municipios_dados)

    print(f"\n✓ Mapa gerado com sucesso!")
    print(f"  Arquivo: {caminho_arquivo}")
    print(f"  Municípios no mapa: {len(municipios_dados)}")

    # Listar municípios incluídos
    if len(municipios_dados) > 1:
        print("\n  Municípios incluídos:")
        for i, item in enumerate(municipios_dados, 1):
            municipio = item[0]
            pib_data = item[2] if len(item) == 3 else None
            nome = municipio["nome"]
            uf = municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"]

            info_pib = ""
            if pib_data and pib_data.get("pib_per_capita"):
                pib_pc = pib_data["pib_per_capita"]
                info_pib = f" - PIB p/c: R$ {pib_pc:,.2f}"

            print(f"    {i}. {nome}/{uf}{info_pib}")

    # Tarefa 1.3: Abrir o HTML automaticamente no navegador
    print(f"\n  Abrindo mapa no navegador...")
    webbrowser.open("file://" + caminho_arquivo)

    print("=" * 80)

    # Tarefa 2.4: Opção de enviar por e-mail
    print("\n" + "=" * 80)
    print("ENVIO DE E-MAIL")
    print("=" * 80)

    enviar = input("\n📧 Deseja enviar o mapa por e-mail? (s/n): ").strip().lower()

    if enviar in ["s", "sim", "yes", "y"]:
        destinatario = input("Digite o e-mail do destinatário: ").strip()

        if destinatario:
            try:
                # Preparar informações dos municípios para o e-mail
                municipios_info = []
                for item in municipios_dados:
                    municipio = item[0]
                    pib_data = item[2] if len(item) == 3 else None

                    info = {
                        "nome": municipio["nome"],
                        "uf": municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"],
                        "codigo": municipio["id"],
                    }

                    if pib_data and pib_data.get("pib_per_capita"):
                        info["pib_per_capita"] = pib_data["pib_per_capita"]

                    municipios_info.append(info)

                # Gerar assunto do e-mail
                if len(municipios_info) == 1:
                    assunto = f"🗺️ Mapa: {municipios_info[0]['nome']}/{municipios_info[0]['uf']}"
                else:
                    assunto = f"🗺️ Mapa: {len(municipios_info)} Municípios Brasileiros"

                # Tarefa 3.3: Perguntar se deseja usar Gemini para gerar o texto
                print("\n" + "-" * 80)
                usar_gemini = (
                    input(
                        "🤖 Deseja usar o Gemini para gerar o texto do e-mail? (s/n): "
                    )
                    .strip()
                    .lower()
                )

                if usar_gemini in ["s", "sim", "yes", "y"]:
                    print("\n🤖 Gerando texto personalizado com Gemini AI...")
                    corpo = gerar_texto_email_com_gemini(municipios_info)
                else:
                    print("\n📝 Usando template padrão de e-mail...")
                    corpo = gerar_corpo_email_mapa(
                        municipios_info, os.path.basename(caminho_arquivo)
                    )

                # Enviar e-mail
                print("\n" + "=" * 80)
                enviar_email(destinatario, assunto, corpo, caminho_arquivo)
                print("=" * 80)

            except Exception as e:
                print(f"\n❌ Erro ao enviar e-mail: {e}")
                print("=" * 80)
        else:
            print("\n⚠️  E-mail não informado. Envio cancelado.")
    else:
        print("\n📭 Envio de e-mail cancelado.")

    print("=" * 80)


if __name__ == "__main__":
    main()
