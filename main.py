import logging
import os
import signal
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from flask import Flask, request, render_template

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8080))
AUTHOR = "Kacper Sawicki"
API_KEY = os.environ.get("OWM_API_KEY")

app = Flask(__name__)

log.info(f"Aplikacja została uruchomiona o godzinie: {datetime.now(ZoneInfo('Europe/Warsaw')).isoformat()}, autor: {AUTHOR}, port{PORT}")

LOCATIONS: dict[str, list[str]] = {
    "Polska": ["Lublin", "Kraków", "Poznań"],
    "USA": ["Los Angeles", "New York", "Houston"],
    "Japonia": ["Tokyo", "Osaka", "Kyoto"],
    "Niemcy": ["Berlin", "Munich", "Hamburg"]
}

def get_weather(city: str) -> dict | None:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "pl"}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        log.error(f"Błąd przy pobieraniu pogody dla {city}: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    selected_country = None
    selected_city = None
    error = None

    if request.method == "POST":
        selected_country = request.form.get("country")
        selected_city = request.form.get("city")
        if selected_city:
            data = get_weather(selected_city)
            if data:
                weather = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "icon": data["weather"][0]["icon"],
                    "wind_speed": data["wind"]["speed"],
                    "pressure": data["main"]["pressure"],
                }
            else:
                error = "Nie udało się pobrać informacji o pogodzie, sprawdź poprawność klucza API"

    return render_template(
        "index.html",
        locations=LOCATIONS,
        weather=weather,
        selected_country=selected_country,
        selected_city=selected_city,
        error=error
    )

@app.route("/health")
def health():
    return {"status": "ok"}, 200

def _shutdown(sig, frame):
    log.info(f"Otrzymano sygnał {sig}, zamykanie aplikacji")
    sys.exit(0)

signal.signal(signal.SIGTERM, _shutdown)
signal.signal(signal.SIGINT, _shutdown)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)