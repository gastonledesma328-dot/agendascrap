import requests
from bs4 import BeautifulSoup
import base64

BASE_URL = "https://pelotalibrestv.org/agenda.html"


def obtener_html():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(BASE_URL, headers=headers)
    r.raise_for_status()
    return r.text


def decodificar_base64_url(href):
    if "r=" not in href:
        return None
    encoded = href.split("r=")[1]
    decoded = base64.b64decode(encoded).decode("utf-8")
    return decoded


def scrapear_partidos():
    html = obtener_html()
    soup = BeautifulSoup(html, "html.parser")

    resultados = []

    bloques = soup.find_all("a")

    for i in range(len(bloques) - 1):

        texto = bloques[i].get_text(strip=True)

        if ":" in texto and "vs" in texto.lower():

            partido = texto
            hora = bloques[i].find("span", class_="t")
            hora = hora.text if hora else None

            siguiente = bloques[i + 1]
            canal = siguiente.get_text(strip=True)

            href = siguiente.get("href")
            url_evento = decodificar_base64_url(href) if href else None

            resultados.append({
                "partido": partido,
                "hora": hora,
                "canal": canal,
                "url_evento": url_evento
            })

    return resultados
