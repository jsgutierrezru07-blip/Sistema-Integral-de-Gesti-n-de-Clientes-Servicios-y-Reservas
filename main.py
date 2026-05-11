"""Punto de entrada de Software FJ."""

from persistencia import registrar_log
from interfaz import iniciar_aplicacion


def main():
    # arranca la app y deja constancia en el log
    registrar_log("INFO", "==== Inicio de la aplicación Software FJ ====")
    try:
        iniciar_aplicacion()
    except Exception as e:
        # cualquier error fatal queda registrado antes de salir
        registrar_log("CRITICO", f"La aplicación terminó con error: {e}")
        raise
    finally:
        registrar_log("INFO", "==== Cierre de la aplicación ====")


if __name__ == "__main__":
    main()

