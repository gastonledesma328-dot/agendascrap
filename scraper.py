import json
import requests
from bs4 import BeautifulSoup


class CanalManager:
    def __init__(self, json_path="canales.json"):
        self.json_path = json_path
        self.canales = self.cargar_canales()

    def cargar_canales(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error cargando JSON:", e)
            return []

    def buscar_canal_local(self, nombre_canal):
        for canal in self.canales:
            if nombre_canal.lower() in canal["nombre"].lower():
                return canal["url"]
        return None


class ScrapManager:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def scrapear_canal(self, url_partido):
        try:
            response = requests.get(url_partido, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # ⚠️ Esto después lo ajustamos según la web real
            enlaces = soup.find_all("a")

            for a in enlaces:
                href = a.get("href")
                if href and ".m3u8" in href:
                    return href

            return None

        except Exception as e:
            print("Error en scraping:", e)
            return None


def obtener_link_final(nombre_canal, url_partido):
    canal_manager = CanalManager()
    scrap_manager = ScrapManager()

    # 1️⃣ Primero busco en mi JSON
    link_local = canal_manager.buscar_canal_local(nombre_canal)

    if link_local:
        print("Canal encontrado en JSON")
        return link_local

    # 2️⃣ Si no está → hago scraping
    print("Canal NO encontrado, haciendo scraping...")
    return scrap_manager.scrapear_canal(url_partido)
