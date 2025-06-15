# calendar_api.py
import os
import requests
from datetime import datetime

def obtener_festivos():
    key = os.getenv("CALENDARIFIC_KEY")
    country = os.getenv("CALENDARIFIC_COUNTRY", "MX")
    year = datetime.now().year

    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": key,
        "country": country,
        "year": year
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data["response"]["holidays"]
    except Exception as e:
        print("Error al consultar Calendarific:", e)
        return []
