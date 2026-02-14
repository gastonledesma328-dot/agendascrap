import requests
import unicodedata
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENDA_API = "https://agenda-futbol.onrender.com/agenda"
CANALES_URL = "https://raw.githubusercontent.com/gastonledesma328-dot/agendascrap/refs/heads/main/canales%20(8).json"


# =========================
# UTILIDADES
# =========================

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = texto.replace("vs", "")
    texto = texto.replace("-", " ")
    texto = texto.replace(":", "")
    return texto


def cargar_agenda():
    r = requests.get(AGENDA_API, timeout=15)
    r.raise_for_status()
    return r.json()


def cargar_canales():
    r = requests.get(CANALES_URL, timeout=15)
    r.raise_for_status()
    return r.json()


def buscar_canal_propio(nombre_canal):
    canales = cargar_canales()
    nombre_canal = normalizar(nombre_canal)

    for c in canales:
        if normalizar(c["name"]) in nombre_canal:
            return c["streamUrl"]

    return None


def coincide_busqueda(query, partido):
    q = normalizar(query).split()
    p = normalizar(partido)

    return all(word in p for word in q)


# =========================
# ENDPOINTS
# =========================

@app.route("/")
def home():
    return "Agenda Scrap API activa"


@app.route("/debug")
def debug():
    """Devuelve la agenda completa"""
    return jsonify(cargar_agenda())


@app.route("/resolver")
def resolver():
    query = request.args.get("partido")

    if not query:
        return jsonify({"error": "Falta parámetro partido"}), 400

    agenda = cargar_agenda()

    for item in agenda:
        partido = item.get("partido", "")
        canal = item.get("canal", "")
        hora = item.get("hora")
        link = item.get("link")

        if coincide_busqueda(query, partido):

            canal_propio = buscar_canal_propio(canal)

            if canal_propio:
                return jsonify({
                    "tipo": "canal_propio",
                    "url": canal_propio,
                    "partido": partido,
                    "canal": canal,
                    "hora": hora
                })

            return jsonify({
                "tipo": "redireccion_externa",
                "url": link,
                "partido": partido,
                "canal": canal,
                "hora": hora
            })

    return jsonify({"error": "Partido no encontrado"}), 404


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
