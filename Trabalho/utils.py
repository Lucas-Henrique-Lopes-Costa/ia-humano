"""
Módulo de utilidades para o Dashboard de Clima
Contém funções auxiliares para formatação e conversão de dados
"""

from datetime import datetime
import requests


def kelvin_to_celsius(kelvin):
    """
    Converte temperatura de Kelvin para Celsius

    Args:
        kelvin (float): Temperatura em Kelvin

    Returns:
        float: Temperatura em Celsius arredondada para 1 casa decimal
    """
    if kelvin:
        return round(kelvin - 273.15, 1)
    return None


def get_weather_icon_url(icon_code):
    """
    Retorna a URL do ícone do clima da OpenWeatherMap

    Args:
        icon_code (str): Código do ícone (ex: "01d")

    Returns:
        str: URL completa do ícone
    """
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"


def format_timestamp(timestamp):
    """
    Formata timestamp Unix para data legível

    Args:
        timestamp (int): Timestamp Unix (UTC)

    Returns:
        str: Data formatada (DD/MM/YYYY HH:MM)
    """
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%d/%m/%Y %H:%M")


def format_date(timestamp):
    """
    Formata timestamp Unix para data (apenas dia)

    Args:
        timestamp (int): Timestamp Unix (UTC)

    Returns:
        str: Data formatada (DD/MM)
    """
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%d/%m")


def get_weekday(timestamp):
    """
    Retorna o dia da semana de um timestamp

    Args:
        timestamp (int): Timestamp Unix (UTC)

    Returns:
        str: Nome do dia da semana em português
    """
    days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dt_object = datetime.fromtimestamp(timestamp)
    return days[dt_object.weekday()]


def translate_weather_description(description):
    """
    Traduz descrições de clima comuns do inglês para português

    Args:
        description (str): Descrição em inglês

    Returns:
        str: Descrição em português ou original se não houver tradução
    """
    translations = {
        "clear sky": "céu limpo",
        "few clouds": "poucas nuvens",
        "scattered clouds": "nuvens dispersas",
        "broken clouds": "nuvens quebradas",
        "overcast clouds": "nublado",
        "shower rain": "chuva forte",
        "rain": "chuva",
        "light rain": "chuva leve",
        "moderate rain": "chuva moderada",
        "heavy intensity rain": "chuva intensa",
        "thunderstorm": "tempestade",
        "snow": "neve",
        "mist": "névoa",
        "fog": "neblina",
        "haze": "neblina",
        "smoke": "fumaça",
        "dust": "poeira",
    }
    return translations.get(description.lower(), description)


def get_wind_direction(degrees):
    """
    Converte graus em direção cardinal do vento

    Args:
        degrees (int): Direção em graus (0-360)

    Returns:
        str: Direção cardinal (N, S, L, O, NE, etc.)
    """
    directions = ["N", "NE", "L", "SE", "S", "SO", "O", "NO"]
    index = round(degrees / 45) % 8
    return directions[index]


def get_geocoding(city_name, api_key):
    """
    Obtém coordenadas geográficas de uma cidade usando a API de Geocoding

    Args:
        city_name (str): Nome da cidade
        api_key (str): Chave da API OpenWeatherMap

    Returns:
        tuple: (latitude, longitude, nome_completo) ou (None, None, None) se não encontrar
    """
    geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city_name, "limit": 1, "appid": api_key}

    try:
        response = requests.get(geocoding_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            name = data[0].get("name", city_name)
            country = data[0].get("country", "")
            full_name = f"{name}, {country}" if country else name
            return lat, lon, full_name
        else:
            return None, None, None

    except Exception as e:
        print(f"Erro ao obter coordenadas: {e}")
        return None, None, None
