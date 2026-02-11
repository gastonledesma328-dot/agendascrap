import requests

CANALES_URL = "https://raw.githubusercontent.com/gastonledesma328-dot/agendascrap/refs/heads/main/canales%20(8).json"


def normalizar(texto):
    return texto.lower().replace("+", "").replace(" ", "")


def cargar_canales():
    r = requests.get(CANALES_URL, timeout=10)
    r.raise_for_status()
    return r.json()


def buscar_canal_propio(nombre_detectado):
    canales = cargar_canales()

    for canal in canales:
        if normalizar(nombre_detectado) in normalizar(canal["name"]):
            return canal["streamUrl"]

    return None
