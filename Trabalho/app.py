"""
Mini Dashboard de Clima - Streamlit
Desenvolvido como parte do experimento de comparação de ferramentas de IA
utilizando GitHub Copilot
"""

import streamlit as st
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from utils import (
    kelvin_to_celsius,
    get_weather_icon_url,
    format_timestamp,
    format_date,
    get_weekday,
    translate_weather_description,
    get_wind_direction,
    get_geocoding,
)

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Clima",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado para melhorar a aparência
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def get_current_weather(lat, lon, api_key):
    """
    Busca dados climáticos atuais da API OpenWeatherMap (API 2.5 - Gratuita)

    Args:
        lat (float): Latitude
        lon (float): Longitude
        api_key (str): Chave da API

    Returns:
        dict: Dados climáticos ou None em caso de erro
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",  # Já retorna em Celsius
        "lang": "pt_br",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return None


def get_forecast_weather(lat, lon, api_key):
    """
    Busca previsão do tempo para os próximos dias (API 2.5 - Gratuita)

    Args:
        lat (float): Latitude
        lon (float): Longitude
        api_key (str): Chave da API

    Returns:
        dict: Dados de previsão ou None em caso de erro
    """
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "lang": "pt_br",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar previsão: {e}")
        return None


def display_current_weather(current_data):
    """
    Exibe os dados climáticos atuais

    Args:
        current_data (dict): Dados do clima atual
    """
    st.header("🌡️ Clima Atual")

    col1, col2, col3, col4 = st.columns(4)

    # Dados principais
    main = current_data.get("main", {})
    wind = current_data.get("wind", {})

    with col1:
        st.metric(
            label="Temperatura",
            value=f"{main.get('temp', 0):.1f}°C",
            delta=f"Sensação: {main.get('feels_like', 0):.1f}°C",
        )

    with col2:
        st.metric(label="Umidade", value=f"{main.get('humidity', 0)}%")

    with col3:
        wind_speed = wind.get("speed", 0)
        wind_dir = get_wind_direction(wind.get("deg", 0))
        st.metric(
            label="Vento", value=f"{wind_speed:.1f} m/s", delta=f"Direção: {wind_dir}"
        )

    with col4:
        st.metric(label="Pressão", value=f"{main.get('pressure', 0)} hPa")

    # Informações adicionais
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        weather = current_data.get("weather", [{}])[0]
        icon_url = get_weather_icon_url(weather.get("icon", "01d"))
        st.image(icon_url, width=100)
        description = weather.get("description", "N/A")
        st.write(f"**Condição:** {description.title()}")

    with col2:
        st.write(f"**Visibilidade:** {current_data.get('visibility', 0) / 1000:.1f} km")
        st.write(f"**Temperatura Mínima:** {main.get('temp_min', 0):.1f}°C")

    with col3:
        st.write(f"**Nebulosidade:** {current_data.get('clouds', {}).get('all', 0)}%")
        st.write(f"**Temperatura Máxima:** {main.get('temp_max', 0):.1f}°C")

    # Horários de nascer e pôr do sol
    st.divider()
    col1, col2 = st.columns(2)

    sys_data = current_data.get("sys", {})
    with col1:
        if "sunrise" in sys_data:
            st.write(f"🌅 **Nascer do Sol:** {format_timestamp(sys_data['sunrise'])}")

    with col2:
        if "sunset" in sys_data:
            st.write(f"🌇 **Pôr do Sol:** {format_timestamp(sys_data['sunset'])}")


def display_forecast(forecast_data):
    """
    Exibe a previsão do tempo para os próximos dias

    Args:
        forecast_data (dict): Dados da previsão
    """
    st.header("📅 Previsão para os Próximos Dias")

    if not forecast_data or "list" not in forecast_data:
        st.warning("Dados de previsão não disponíveis")
        return

    # Agrupar previsões por dia (pegar uma previsão por dia, ao meio-dia se possível)
    daily_forecasts = {}

    for item in forecast_data["list"]:
        date = datetime.fromtimestamp(item["dt"]).date()
        hour = datetime.fromtimestamp(item["dt"]).hour

        # Preferir previsões do meio-dia (12h)
        if date not in daily_forecasts or hour == 12:
            daily_forecasts[date] = item

    # Limitar a 5 dias
    days = list(daily_forecasts.values())[:5]

    cols = st.columns(min(len(days), 5))

    for idx, day_data in enumerate(days):
        with cols[idx]:
            dt = datetime.fromtimestamp(day_data["dt"])

            st.subheader(f"{dt.strftime('%d/%m')}")
            st.write(f"**{get_weekday(day_data['dt'])}**")

            # Ícone
            weather = day_data["weather"][0]
            icon_url = get_weather_icon_url(weather["icon"])
            st.image(icon_url, width=80)

            # Temperatura
            main = day_data["main"]
            st.metric(
                "Temp",
                f"{main['temp']:.1f}°C",
                delta=f"Min: {main['temp_min']:.0f}° Max: {main['temp_max']:.0f}°",
            )

            # Descrição
            description = weather.get("description", "")
            st.caption(description.title())

            # Probabilidade de chuva
            if "pop" in day_data:
                pop = day_data["pop"] * 100
                st.caption(f"☔ Chuva: {pop:.0f}%")


def display_daily_forecast(daily_data):
    """
    Exibe a previsão para os próximos dias

    Args:
        daily_data (list): Lista com dados diários
    """
    st.header("📅 Previsão para os Próximos Dias")

    # Exibir até 7 dias (ignorando o dia atual)
    cols = st.columns(min(7, len(daily_data) - 1))

    for idx, day in enumerate(daily_data[1:8]):  # Pula o dia atual
        with cols[idx]:
            # Data e dia da semana
            date = format_date(day["dt"])
            weekday = get_weekday(day["dt"])
            st.write(f"**{weekday}**")
            st.write(f"{date}")

            # Ícone do clima
            weather = day["weather"][0]
            icon_url = get_weather_icon_url(weather["icon"])
            st.image(icon_url, width=80)

            # Descrição
            description = translate_weather_description(weather["description"])
            st.caption(description.title())

            # Temperaturas
            temp_max = day["temp"]["max"]
            temp_min = day["temp"]["min"]
            st.write(f"🔺 {temp_max:.0f}°C")
            st.write(f"🔻 {temp_min:.0f}°C")

            # Probabilidade de chuva
            pop = day.get("pop", 0) * 100
            if pop > 0:
                st.write(f"💧 {pop:.0f}%")

            st.divider()


def main():
    """
    Função principal da aplicação
    """
    # Título
    st.title("🌤️ Mini Dashboard de Clima")
    st.markdown(
        '<p class="subtitle">Consulte o clima atual e previsão para qualquer cidade do mundo</p>',
        unsafe_allow_html=True,
    )

    # Sidebar com informações
    with st.sidebar:
        st.header("ℹ️ Sobre")
        st.write(
            """
        Este dashboard foi desenvolvido como parte de um experimento prático 
        para comparar ferramentas de IA no desenvolvimento de software.
        """
        )

        st.divider()

        st.write("**Tecnologias utilizadas:**")
        st.write("- Python")
        st.write("- Streamlit")
        st.write("- OpenWeatherMap API")

        st.divider()

        st.write("**Desenvolvido com:**")
        st.write("- GitHub Copilot")

        st.divider()

        st.caption("Dados fornecidos pela OpenWeatherMap")

    # Obter API key
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        st.error("⚠️ API Key não encontrada! Verifique o arquivo .env")
        st.stop()

    # Campo de entrada para cidade
    st.subheader("🔍 Buscar Cidade")

    col1, col2 = st.columns([3, 1])

    with col1:
        city_name = st.text_input(
            "Digite o nome da cidade:",
            placeholder="Ex: São Paulo, London, Tokyo",
            label_visibility="collapsed",
        )

    with col2:
        search_button = st.button("🔎 Buscar", use_container_width=True, type="primary")

    # Buscar dados quando o botão for clicado ou Enter for pressionado
    if search_button or city_name:
        if city_name:
            with st.spinner("🌍 Buscando informações..."):
                # Obter coordenadas da cidade
                lat, lon, full_name = get_geocoding(city_name, api_key)

                if lat is None or lon is None:
                    st.error(
                        f"❌ Cidade '{city_name}' não encontrada. Tente outro nome."
                    )
                else:
                    # Buscar dados climáticos atuais
                    current_weather = get_current_weather(lat, lon, api_key)

                    # Buscar previsão
                    forecast_weather = get_forecast_weather(lat, lon, api_key)

                    if current_weather:
                        # Exibir nome da cidade encontrada
                        st.success(f"✅ Exibindo dados para: **{full_name}**")

                        st.divider()

                        # Exibir clima atual
                        display_current_weather(current_weather)

                        st.divider()

                        # Exibir previsão
                        if forecast_weather:
                            display_forecast(forecast_weather)
                    else:
                        st.error("❌ Erro ao buscar dados climáticos. Tente novamente.")
        else:
            st.info("👆 Digite o nome de uma cidade acima para começar")
    else:
        # Mensagem inicial
        st.info("👆 Digite o nome de uma cidade e pressione Enter ou clique em Buscar")

        # Mostrar exemplos
        st.subheader("💡 Exemplos de cidades:")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("🇧🇷 São Paulo")
            st.write("🇧🇷 Rio de Janeiro")
            st.write("🇧🇷 Brasília")

        with col2:
            st.write("🇺🇸 New York")
            st.write("🇬🇧 London")
            st.write("🇫🇷 Paris")

        with col3:
            st.write("🇯🇵 Tokyo")
            st.write("🇦🇺 Sydney")
            st.write("🇦🇪 Dubai")


if __name__ == "__main__":
    main()
