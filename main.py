from flask import Flask, request, jsonify
from scraper import scrapear_partidos

app = Flask(__name__)


@app.route("/")
def home():
    return "Agenda Scrap API activa"


@app.route("/debug")
def debug():
    return jsonify(scrapear_partidos())


@app.route("/resolver")
def resolver():
    partido = request.args.get("partido")
    if not partido:
        return jsonify({"error": "Falta parámetro partido"}), 400

    partido = partido.lower()
    partidos = scrapear_partidos()

    for p in partidos:
        if partido in p["partido"].lower():
            return jsonify(p)

    return jsonify({"error": "Partido no encontrado"}), 404
