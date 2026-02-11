from scraper import scrapear_partidos
from resolver import buscar_canal_propio


def resolver_partido(nombre_partido):

    partidos = scrapear_partidos()

    for p in partidos:
        if nombre_partido.lower() in p["partido"].lower():

            stream_propio = buscar_canal_propio(p["canal"])

            if stream_propio:
                return {
                    "tipo": "canal_propio",
                    "url": stream_propio
                }
            else:
                return {
                    "tipo": "redireccion_externa",
                    "url": p["url_evento"]
                }

    return None


if __name__ == "__main__":

    resultado = resolver_partido("América vs Olimpia")

    if resultado:
        print("Destino:")
        print(resultado)
    else:
        print("Partido no encontrado")
