import unicodedata
from flask import Flask, request, jsonify
from scraper import scrapear_partidos
from resolver import buscar_canal_propio

app = Flask(__name__)


def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = texto.replace("vs", "")
    texto = texto.replace(":", "")
    texto = texto.replace("-", " ")
    return texto


def coincide_busqueda(query, partido_texto):
    query = normalizar_texto(query)
    partido_texto = normalizar_texto(partido_texto)

    palabras_query = query.split()

    return all(p in partido_texto for p in palabras_query)


@app.route("/")
def home():
    return "Agenda Scrap API activa"


@app.route("/resolver")
def resolver():

    nombre_partido = request.args.get("partido")

    if not nombre_partido:
        return jsonify({"error": "Falta parámetro 'partido'"}), 400

    partidos = scrapear_partidos()

    for p in partidos:
        if coincide_busqueda(nombre_partido, p["partido"]):

            stream_propio = buscar_canal_propio(p["canal"])

            if stream_propio:
                return jsonify({
                    "tipo": "canal_propio",
                    "url": stream_propio,
                    "partido": p["partido"],
                    "canal": p["canal"]
                })

            else:
                return jsonify({
                    "tipo": "redireccion_externa",
                    "url": p["url_evento"],
                    "partido": p["partido"],
                    "canal": p["canal"]
                })

    return jsonify({"error": "Partido no encontrado"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
