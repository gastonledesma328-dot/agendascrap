import requests
from bs4 import BeautifulSoup
import base64
import unicodedata
import re

AGENDA_URL = "https://pelotalibrestv.org/agenda.html"


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto


def obtener_html():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(AGENDA_URL, headers=headers, timeout=15)
    r.raise_for_status()
    return r.text


def decodificar_base64(href):
    if not href or "r=" not in href:
        return None
    try:
        encoded = href.split("r=")[1]
        return base64.b64decode(encoded).decode("utf-8")
    except:
        return None


def es_partido(texto):
    texto = normalizar(texto)
    # Detecta "vs", "-", "—", " v "
    return bool(re.search(r"\bvs\b|\bv\b| - | — ", texto))


def scrapear_partidos():
    html = obtener_html()
    soup = BeautifulSoup(html, "html.parser")

    resultados = []
    enlaces = soup.find_all("a")

    for i in range(len(enlaces) - 1):

        texto = enlaces[i].get_text(" ", strip=True)

        if not es_partido(texto):
            continue

        hora_tag = enlaces[i].find("span", class_="t")
        hora = hora_tag.text.strip() if hora_tag else None

        siguiente = enlaces[i + 1]
        canal = siguiente.get_text(" ", strip=True)
        href = siguiente.get("href")

        url_evento = decodificar_base64(href)

        resultados.append({
            "partido": texto.strip(),
            "hora": hora,
            "canal": canal.strip(),
            "url_evento": url_evento
        })

    return resultados
