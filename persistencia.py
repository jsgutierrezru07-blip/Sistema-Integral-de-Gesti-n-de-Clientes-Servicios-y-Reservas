"""Persistencia: registro de eventos en archivo de logs y lectura."""

import os
from datetime import datetime

# el archivo de logs va junto al código
ARCHIVO_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "registro_eventos.log")


def registrar_log(nivel, mensaje):
    # escribe una línea con timestamp en el log
    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{nivel}] {mensaje}\n")
    except Exception:
        # si el log falla, no debe tumbar la app
        pass


def leer_ultimos_logs(cantidad=40):
    # devuelve las últimas N líneas del archivo
    try:
        with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
            return f.readlines()[-cantidad:]
    except FileNotFoundError:
        return []


def ruta_archivo_log():
    return ARCHIVO_LOG

