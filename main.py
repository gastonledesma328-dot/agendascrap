import requests
from datetime import datetime
import time
from scraper import scrapear_partidos

CANALES_URL = "https://raw.githubusercontent.com/gastonledesma328-dot/agendascrap/refs/heads/main/canales%20(8).json"


def cargar_canales():
    r = requests.get(CANALES_URL)
    r.raise_for_status()
    return r.json()


def normalizar(texto):
    return texto.lower().replace("+", "").replace(" ", "")


def buscar_canal(canal_detectado, canales):
    for canal in canales:
        if normalizar(canal_detectado) in normalizar(canal["name"]):
            return canal
    return None


def convertir_hora_24(hora_str):
    return datetime.strptime(hora_str, "%H:%M").time()


def faltan_5_minutos(hora_partido):
    ahora = datetime.now().time()
    hora_obj = convertir_hora_24(hora_partido)

    diferencia = (
        datetime.combine(datetime.today(), hora_obj) -
        datetime.combine(datetime.today(), ahora)
    ).total_seconds()

    return 0 < diferencia <= 300


def ejecutar_scraping_profundo(url_evento):
    print("🔍 Scraping profundo para encontrar M3U8...")
    # acá después mejoramos esto
    return "M3U8_ENCONTRADO"


def main():
    print("📡 Iniciando sistema...")
    canales = cargar_canales()
    partidos = scrapear_partidos()

    for p in partidos:

        print(f"\n🎯 {p['partido']}")

        canal = buscar_canal(p["canal"], canales)

        if canal:
            print("✅ Canal encontrado en JSON")
            print("→", canal["streamUrl"])
        else:
            print("⚠ Canal no encontrado")

            if p["hora"] and faltan_5_minutos(p["hora"]):
                link = ejecutar_scraping_profundo(p["url_evento"])
                print("→", link)
            else:
                print("⏳ Aún no es momento de scrapear")


if __name__ == "__main__":
    main()
