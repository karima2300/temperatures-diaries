import requests
import json
from datetime import datetime

# CANVIA AQUÍ LA CIUTAT QUE VULGUIS
CIUTAT = "Barcelona"
LATITUD = 41.38879
LONGITUD = 2.15899

def obtenir_temperatures():
    """Obté temperatures horàries del dia actual des de Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUD,
        "longitude": LONGITUD,
        "hourly": "temperature_2m",
        "timezone": "Europe/Madrid",
        "forecast_days": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["hourly"]["temperature_2m"]

def calcular_estadistiques(temperatures):
    """Calcula màxima, mínima i mitjana."""
    if not temperatures:
        return None
    return {
        "maxima": round(max(temperatures), 2),
        "minima": round(min(temperatures), 2),
        "mitjana": round(sum(temperatures) / len(temperatures), 2)
    }

def exportar_json(estadistiques):
    """Exporta les dades a un fitxer JSON amb la data actual."""
    data_actual = datetime.now().strftime("%Y%m%d")
    nom_fitxer = f"temp_{data_actual}.json"
    
    contingut = {
        "ciutat": CIUTAT,
        "data": data_actual,
        "coordenades": {"lat": LATITUD, "lon": LONGITUD},
        "estadistiques": estadistiques,
        "unitats": "°C"
    }
    
    with open(nom_fitxer, "w", encoding="utf-8") as f:
        json.dump(contingut, f, indent=4, ensure_ascii=False)
    
    print(f"Fitxer {nom_fitxer} creat correctament.")
    return nom_fitxer

def main():
    print(f"🌡️ Obtenint temperatures per a {CIUTAT}...")
    try:
        temps = obtenir_temperatures()
        print(f"Temperatures obtingudes: {len(temps)} hores")
        stats = calcular_estadistiques(temps)
        print(f"Màxima: {stats['maxima']}°C")
        print(f"Mínima: {stats['minima']}°C")
        print(f"Mitjana: {stats['mitjana']}°C")
        exportar_json(stats)
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()