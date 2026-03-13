import json
import os
from datetime import datetime
import pytz

ARCHIVO = "jugador.json"

def calcular_rango(nivel):
    if nivel <= 10:
        return "E"
    elif nivel <= 20:
        return "D"
    elif nivel <= 30:
        return "C"
    elif nivel <= 40:
        return "B"
    elif nivel <= 50:
        return "A"
    else:
        return "S"

def dias_para_subir_nivel(nivel):
    return nivel

def obtener_hora_local(timezone_str):
    tz = pytz.timezone(timezone_str)
    return datetime.now(tz)

def datos_iniciales():
    return {
        "nombre": "Hunter",
        "nivel": 1,
        "rango": "E",
        "xp": 0,
        "dias_consecutivos": 0,
        "dias_requeridos": 1,
        "ultima_vez": None,
        "dias_sin_completar": 0,
        "timezone": "America/Argentina/Buenos_Aires",
        "penalizacion_activa": [],
        "misiones": [
            {"nombre": "100 Flexiones", "xp": 50, "completada": False},
            {"nombre": "100 Abdominales", "xp": 50, "completada": False},
            {"nombre": "100 Sentadillas", "xp": 50, "completada": False},
            {"nombre": "Correr 10km", "xp": 80, "completada": False},
            {"nombre": "Estudiar 2hs", "xp": 60, "completada": False},
            {"nombre": "Leer 30min", "xp": 30, "completada": False},
        ],
        "penalizaciones_pool": [
            "No usar el celular por 1 hora",
            "50 Flexiones de brazos",
            "10 Dominadas",
            "Correr 5km",
            "100 Sentadillas",
            "30 minutos de meditación",
            "Estudiar 1 hora sin distracciones"
        ]
    }

def cargar_jugador():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    else:
        jugador = datos_iniciales()
        guardar_jugador(jugador)
        return jugador

def guardar_jugador(jugador):
    with open(ARCHIVO, "w") as f:
        json.dump(jugador, f, indent=4)

def resetear_misiones(jugador):
    for mision in jugador["misiones"]:
        mision["completada"] = False
    jugador["xp"] = 0
    return jugador

def verificar_nuevo_dia(jugador):
    tz = pytz.timezone(jugador.get("timezone", "America/Argentina/Buenos_Aires"))
    hoy = datetime.now(tz).strftime("%Y-%m-%d")
    resultado = {"nuevo_dia": False, "penalizo": False, "subio_nivel": False}

    if jugador["ultima_vez"] is None:
        jugador["ultima_vez"] = hoy
        guardar_jugador(jugador)
        return resultado

    if jugador["ultima_vez"] == hoy:
        return resultado

    resultado["nuevo_dia"] = True
    todas_completas = all(m["completada"] for m in jugador["misiones"])

    if todas_completas:
        jugador["dias_consecutivos"] += 1
        jugador["dias_sin_completar"] = 0
        jugador["penalizacion_activa"] = []

        if jugador["dias_consecutivos"] >= jugador["dias_requeridos"]:
            jugador["nivel"] += 1
            jugador["rango"] = calcular_rango(jugador["nivel"])
            jugador["dias_consecutivos"] = 0
            jugador["dias_requeridos"] = dias_para_subir_nivel(jugador["nivel"])
            resultado["subio_nivel"] = True
    else:
        jugador["dias_consecutivos"] = 0
        jugador["dias_sin_completar"] += 1
        resultado["penalizo"] = True

        import random
        cantidad = min(jugador["dias_sin_completar"], 3)
        jugador["penalizacion_activa"] = random.sample(
            jugador["penalizaciones_pool"], cantidad
        )

        perdida = {1: 30, 2: 60}.get(jugador["dias_sin_completar"], 100)
        jugador["xp"] = max(0, jugador["xp"] - perdida)

    guardar_historial(jugador)
    jugador = resetear_misiones(jugador)
    jugador["ultima_vez"] = hoy
    guardar_jugador(jugador)
    return resultado
def guardar_historial(jugador):
    """Guarda el registro del día actual en el historial."""
    tz = pytz.timezone(jugador.get("timezone", "America/Argentina/Buenos_Aires"))
    hoy = datetime.now(tz).strftime("%Y-%m-%d")

    if "historial" not in jugador:
        jugador["historial"] = []

    misiones_completadas = sum(1 for m in jugador["misiones"] if m["completada"])
    total_misiones = len(jugador["misiones"])

    # Evitar duplicados del mismo día
    for entrada in jugador["historial"]:
        if entrada["fecha"] == hoy:
            entrada["xp"] = jugador["xp"]
            entrada["misiones_completadas"] = misiones_completadas
            entrada["total_misiones"] = total_misiones
            guardar_jugador(jugador)
            return

    jugador["historial"].append({
        "fecha": hoy,
        "xp": jugador["xp"],
        "misiones_completadas": misiones_completadas,
        "total_misiones": total_misiones,
        "nivel": jugador["nivel"],
    })
    guardar_jugador(jugador)

# Países y sus timezones
PAISES_TIMEZONES = {
    "Argentina": "America/Argentina/Buenos_Aires",
    "México": "America/Mexico_City",
    "Colombia": "America/Bogota",
    "Chile": "America/Santiago",
    "Perú": "America/Lima",
    "Venezuela": "America/Caracas",
    "Uruguay": "America/Montevideo",
    "Bolivia": "America/La_Paz",
    "Paraguay": "America/Asuncion",
    "Ecuador": "America/Guayaquil",
    "España": "Europe/Madrid",
    "Estados Unidos (Este)": "America/New_York",
    "Estados Unidos (Oeste)": "America/Los_Angeles",
    "Brasil": "America/Sao_Paulo",
}