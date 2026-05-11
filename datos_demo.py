"""Simulación de las 10+ operaciones iniciales (válidas e inválidas)."""

from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSoftwareFJ
from persistencia import registrar_log


def _intentar(descripcion, funcion, registro):
    # ejecuta una operación y guarda el resultado o error en el registro
    try:
        resultado = funcion()
        registro.append(("OK", f"{descripcion} -> {resultado}"))
        registrar_log("INFO", f"DEMO OK: {descripcion}")
    except ErrorSoftwareFJ as e:
        registro.append(("ERROR", f"{descripcion} -> {e}"))
        registrar_log("ERROR", f"DEMO ERROR ({descripcion}): {e}")
    except Exception as e:
        registro.append(("ERROR", f"{descripcion} -> {e}"))
        registrar_log("ERROR", f"DEMO ERROR INESPERADO ({descripcion}): {e}")


def cargar_datos_demo(sistema):
    # ejecuta 12 operaciones sobre el sistema y devuelve el registro
    registro = []

    # 1
    _intentar("Registrar cliente válido (Ana)",
              lambda: sistema.registrar_cliente("Ana Pérez", "1001234567", "ana@correo.com", "3001234567").describir(),
              registro)

    # 2
    _intentar("Registrar cliente válido (Luis)",
              lambda: sistema.registrar_cliente("Luis Gómez", "1009876543", "luis@correo.com", "3017654321").describir(),
              registro)

    # 3 correo inválido
    _intentar("Registrar cliente con correo inválido",
              lambda: sistema.registrar_cliente("Pedro X", "1112223334", "correo-malo", "3000000000").describir(),
              registro)

    # 4 documento duplicado
    _intentar("Registrar cliente con documento duplicado",
              lambda: sistema.registrar_cliente("Otra Ana", "1001234567", "ana2@correo.com", "3001234567").describir(),
              registro)

    # 5 sala válida
    _intentar("Crear sala de reuniones",
              lambda: sistema.agregar_servicio(ReservaSala("Sala Norte", 50000, 10)).describir(),
              registro)

    # 6 equipo válido
    _intentar("Crear alquiler de equipo",
              lambda: sistema.agregar_servicio(AlquilerEquipo("Proyector Epson", 80000, "Proyector")).describir(),
              registro)

    # 7 asesoría válida
    _intentar("Crear asesoría",
              lambda: sistema.agregar_servicio(AsesoriaEspecializada("Asesoría Tributaria", 120000, "Impuestos")).describir(),
              registro)

    # 8 precio negativo
    _intentar("Crear servicio con precio negativo",
              lambda: sistema.agregar_servicio(ReservaSala("Sala Mala", -1000, 5)).describir(),
              registro)

    # 9 reserva exitosa completa
    def reserva_exitosa():
        r = sistema.crear_reserva(1, 5, 3)
        r.confirmar()
        return f"{r.describir()} costo: ${r.procesar(impuesto=19, descuento=10)}"
    _intentar("Reserva completa con impuesto y descuento", reserva_exitosa, registro)

    # 10 duración inválida
    _intentar("Reserva con duración inválida",
              lambda: sistema.crear_reserva(2, 6, -5).describir(),
              registro)

    # 11 cliente inexistente
    _intentar("Reserva con cliente inexistente",
              lambda: sistema.crear_reserva(999, 5, 2).describir(),
              registro)

    # 12 procesar reserva cancelada (falla controlada)
    def reserva_cancelada():
        r = sistema.crear_reserva(2, 7, 2)
        r.cancelar()
        return r.procesar()
    _intentar("Procesar reserva cancelada", reserva_cancelada, registro)

    return registro

