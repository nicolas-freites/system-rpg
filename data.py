# ============================================================
# data.py — Archivo de lógica y datos del jugador
# Acá separamos toda la lógica del juego (XP, niveles, misiones,
# penalizaciones) para mantener app.py limpio y ordenado.
# Esta separación se llama "separación de responsabilidades" y
# es una práctica profesional fundamental.
# ============================================================

import json                          # Para leer y escribir archivos JSON
import os                            # Para verificar si un archivo existe en el sistema
from datetime import datetime        # Para trabajar con fechas y horas
import pytz                          # Para manejar zonas horarias
import random                        # Para elegir penalizaciones al azar

# Nombre del archivo donde se guardan los datos del jugador
# Usamos JSON porque es un formato simple, legible y fácil de trabajar en Python
ARCHIVO = "jugador.json"


# ════════════════════════════════════════
# FUNCIÓN: calcular_rango
# Devuelve el rango del jugador según su nivel actual
# Los rangos van de E (más bajo) a S (más alto), igual que en Solo Leveling
# ════════════════════════════════════════
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


# ════════════════════════════════════════
# FUNCIÓN: dias_para_subir_nivel
# Devuelve cuántos días consecutivos necesita el jugador para subir al siguiente nivel.
# La dificultad escala con el nivel: a mayor nivel, más días se requieren.
# Ej: para pasar de nivel 1 a 2 se necesita 1 día, de nivel 5 a 6 se necesitan 5 días.
# ════════════════════════════════════════
def dias_para_subir_nivel(nivel):
    return nivel  # El número de días requeridos es igual al nivel actual


# ════════════════════════════════════════
# FUNCIÓN: obtener_hora_local
# Devuelve la hora actual en la zona horaria del jugador.
# Recibe un string de timezone (ej: "America/Argentina/Buenos_Aires")
# ════════════════════════════════════════
def obtener_hora_local(timezone_str):
    tz = pytz.timezone(timezone_str)
    return datetime.now(tz)


# ════════════════════════════════════════
# FUNCIÓN: datos_iniciales
# Crea y devuelve un diccionario con los datos de un jugador nuevo.
# Se usa solo la primera vez que alguien abre la app.
# Un diccionario en Python es una colección de pares clave:valor
# ════════════════════════════════════════
def datos_iniciales():
    return {
        "nombre": "Hunter",                                # Nombre por defecto
        "nivel": 1,                                        # Todos empiezan en nivel 1
        "rango": "E",                                      # Rango inicial más bajo
        "xp": 0,                                           # Sin XP al inicio
        "dias_consecutivos": 0,                            # Días seguidos completando misiones
        "dias_requeridos": 1,                              # Días necesarios para subir al nivel 2
        "ultima_vez": None,                                # Última fecha en que entró a la app
        "dias_sin_completar": 0,                           # Contador de días fallidos consecutivos
        "timezone": "America/Argentina/Buenos_Aires",      # Zona horaria por defecto
        "penalizacion_activa": [],                         # Lista de misiones de castigo activas
        "misiones": [
            # Cada misión tiene nombre, XP que otorga, y si fue completada hoy
            {"nombre": "100 Flexiones",   "xp": 50, "completada": False},
            {"nombre": "100 Abdominales", "xp": 50, "completada": False},
            {"nombre": "100 Sentadillas", "xp": 50, "completada": False},
            {"nombre": "Correr 10km",     "xp": 80, "completada": False},
            {"nombre": "Estudiar 2hs",    "xp": 60, "completada": False},
            {"nombre": "Leer 30min",      "xp": 30, "completada": False},
        ],
        # Pool de penalizaciones: se eligen al azar cuando el jugador falla
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


# ════════════════════════════════════════
# FUNCIÓN: cargar_jugador
# Lee los datos del jugador desde el archivo JSON.
# Si el archivo no existe (primera vez), crea uno con datos iniciales.
# ════════════════════════════════════════
def cargar_jugador():
    if os.path.exists(ARCHIVO):
        # El archivo existe: lo abrimos y cargamos su contenido
        with open(ARCHIVO, "r") as f:
            return json.load(f)  # json.load convierte el JSON en un diccionario Python
    else:
        # Primera vez: creamos un jugador nuevo y lo guardamos
        jugador = datos_iniciales()
        guardar_jugador(jugador)
        return jugador


# ════════════════════════════════════════
# FUNCIÓN: guardar_jugador
# Escribe los datos del jugador en el archivo JSON.
# Se llama cada vez que algo cambia (completar misión, subir de nivel, etc.)
# ════════════════════════════════════════
def guardar_jugador(jugador):
    with open(ARCHIVO, "w") as f:
        # json.dump convierte el diccionario Python en texto JSON y lo escribe
        # indent=4 hace que el archivo sea legible (con sangría de 4 espacios)
        json.dump(jugador, f, indent=4)


# ════════════════════════════════════════
# FUNCIÓN: resetear_misiones
# Marca todas las misiones como no completadas y resetea el XP del día.
# Se llama al inicio de cada nuevo día.
# ════════════════════════════════════════
def resetear_misiones(jugador):
    for mision in jugador["misiones"]:
        mision["completada"] = False  # Reseteamos cada misión
    jugador["xp"] = 0                # El XP del día vuelve a 0
    return jugador


# ════════════════════════════════════════
# FUNCIÓN: verificar_nuevo_dia
# Esta es la función más importante del juego.
# Verifica si cambió el día desde la última vez que el jugador entró.
# Si cambió el día:
#   - Si completó todas las misiones: suma días consecutivos, evalúa si sube de nivel
#   - Si no las completó: aplica penalización, resta XP, resetea racha
# ════════════════════════════════════════
def verificar_nuevo_dia(jugador):
    # Obtenemos la fecha de hoy en la zona horaria del jugador
    tz = pytz.timezone(jugador.get("timezone", "America/Argentina/Buenos_Aires"))
    hoy = datetime.now(tz).strftime("%Y-%m-%d")  # Formato: "2026-03-13"

    # Diccionario que devolvemos para informar a app.py qué pasó
    resultado = {"nuevo_dia": False, "penalizo": False, "subio_nivel": False}

    # Si es la primera vez que entra, solo guardamos la fecha y salimos
    if jugador["ultima_vez"] is None:
        jugador["ultima_vez"] = hoy
        guardar_jugador(jugador)
        return resultado

    # Si ya entró hoy, no hacemos nada (no cambió el día)
    if jugador["ultima_vez"] == hoy:
        return resultado

    # Llegamos acá solo si es un día nuevo
    resultado["nuevo_dia"] = True

    # Verificamos si todas las misiones del día anterior estaban completadas
    todas_completas = all(m["completada"] for m in jugador["misiones"])

    if todas_completas:
        # ── El jugador completó todas las misiones ──
        jugador["dias_consecutivos"] += 1       # Suma un día a la racha
        jugador["dias_sin_completar"] = 0       # Resetea el contador de fallos
        jugador["penalizacion_activa"] = []     # Limpia penalizaciones anteriores

        # Verificamos si la racha alcanzó los días necesarios para subir de nivel
        if jugador["dias_consecutivos"] >= jugador["dias_requeridos"]:
            jugador["nivel"] += 1
            jugador["rango"] = calcular_rango(jugador["nivel"])
            jugador["dias_consecutivos"] = 0    # Resetea la racha para el nuevo nivel
            jugador["dias_requeridos"] = dias_para_subir_nivel(jugador["nivel"])
            resultado["subio_nivel"] = True
    else:
        # ── El jugador NO completó todas las misiones ──
        jugador["dias_consecutivos"] = 0        # Se pierde la racha
        jugador["dias_sin_completar"] += 1      # Suma un día fallido
        resultado["penalizo"] = True

        # Elegimos penalizaciones al azar del pool
        # min() evita pedir más elementos de los que hay en la lista
        cantidad = min(jugador["dias_sin_completar"], 3)
        jugador["penalizacion_activa"] = random.sample(
            jugador["penalizaciones_pool"], cantidad
        )

        # La pérdida de XP aumenta con los días fallidos consecutivos
        # 1 día fallido = -30 XP, 2 días = -60 XP, 3 o más = -100 XP
        perdida = {1: 30, 2: 60}.get(jugador["dias_sin_completar"], 100)
        jugador["xp"] = max(0, jugador["xp"] - perdida)  # El XP no puede bajar de 0

    # Guardamos el historial antes de resetear las misiones
    guardar_historial(jugador)

    # Reseteamos las misiones para el nuevo día
    jugador = resetear_misiones(jugador)

    # Actualizamos la fecha de última vez
    jugador["ultima_vez"] = hoy
    guardar_jugador(jugador)

    return resultado


# ════════════════════════════════════════
# FUNCIÓN: guardar_historial
# Guarda el registro del día actual en el historial del jugador.
# El historial es una lista de entradas, una por día.
# Evita guardar el mismo día dos veces (duplicados).
# ════════════════════════════════════════
def guardar_historial(jugador):
    tz = pytz.timezone(jugador.get("timezone", "America/Argentina/Buenos_Aires"))
    hoy = datetime.now(tz).strftime("%Y-%m-%d")

    # Si el jugador no tiene historial todavía, creamos la lista vacía
    if "historial" not in jugador:
        jugador["historial"] = []

    # Contamos cuántas misiones completó hoy
    misiones_completadas = sum(1 for m in jugador["misiones"] if m["completada"])
    total_misiones = len(jugador["misiones"])

    # Evitamos duplicados: si ya existe una entrada para hoy, la actualizamos
    for entrada in jugador["historial"]:
        if entrada["fecha"] == hoy:
            entrada["xp"] = jugador["xp"]
            entrada["misiones_completadas"] = misiones_completadas
            entrada["total_misiones"] = total_misiones
            guardar_jugador(jugador)
            return  # Salimos de la función, ya actualizamos

    # Si no existe entrada para hoy, la agregamos
    jugador["historial"].append({
        "fecha": hoy,
        "xp": jugador["xp"],
        "misiones_completadas": misiones_completadas,
        "total_misiones": total_misiones,
        "nivel": jugador["nivel"],
    })
    guardar_jugador(jugador)


# ════════════════════════════════════════
# DICCIONARIO: PAISES_TIMEZONES
# Mapea el nombre legible de cada país con su zona horaria oficial.
# Se usa en la pantalla de registro para que el jugador elija su país.
# Un diccionario es perfecto para esto porque permite buscar por clave.
# ════════════════════════════════════════
PAISES_TIMEZONES = {
    "Argentina":                "America/Argentina/Buenos_Aires",
    "México":                   "America/Mexico_City",
    "Colombia":                 "America/Bogota",
    "Chile":                    "America/Santiago",
    "Perú":                     "America/Lima",
    "Venezuela":                "America/Caracas",
    "Uruguay":                  "America/Montevideo",
    "Bolivia":                  "America/La_Paz",
    "Paraguay":                 "America/Asuncion",
    "Ecuador":                  "America/Guayaquil",
    "España":                   "Europe/Madrid",
    "Estados Unidos (Este)":    "America/New_York",
    "Estados Unidos (Oeste)":   "America/Los_Angeles",
    "Brasil":                   "America/Sao_Paulo",
}