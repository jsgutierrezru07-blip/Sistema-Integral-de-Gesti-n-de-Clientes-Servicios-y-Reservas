"""Clase Reserva: integra cliente, servicio, duración y estado."""

from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import (
    ErrorReservaInvalida,
    ErrorServicioNoDisponible,
    ErrorSoftwareFJ,
)
from persistencia import registrar_log


class Reserva(Entidad):
    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada", "procesada")

    def __init__(self, cliente, servicio, duracion):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ErrorReservaInvalida("Cliente inválido para la reserva")
        if not isinstance(servicio, Servicio):
            raise ErrorReservaInvalida("Servicio inválido para la reserva")
        if not servicio.disponible:
            raise ErrorServicioNoDisponible(f"El servicio '{servicio.nombre}' no está disponible")

        # esto lanza error si la duración no aplica al servicio
        servicio.validar_parametros(duracion)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "pendiente"
        self._costo_final = None
        registrar_log("INFO", f"Reserva #{self._id} creada para {cliente.nombre} - {servicio.nombre}")

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def costo_final(self):
        return self._costo_final

    def confirmar(self):
        if self._estado != "pendiente":
            raise ErrorReservaInvalida(f"No se puede confirmar una reserva en estado '{self._estado}'")
        self._estado = "confirmada"
        registrar_log("INFO", f"Reserva #{self._id} confirmada")

    def cancelar(self):
        if self._estado in ("cancelada", "procesada"):
            raise ErrorReservaInvalida(f"No se puede cancelar una reserva en estado '{self._estado}'")
        self._estado = "cancelada"
        registrar_log("INFO", f"Reserva #{self._id} cancelada")

    def procesar(self, impuesto=None, descuento=None):
        # try/except/else/finally con encadenamiento
        try:
            if self._estado != "confirmada":
                raise ErrorReservaInvalida("La reserva debe estar confirmada para procesarse")
            costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        except ErrorSoftwareFJ:
            registrar_log("ERROR", f"Reserva #{self._id} falló al procesar")
            raise
        except Exception as e:
            registrar_log("ERROR", f"Error inesperado procesando reserva #{self._id}: {e}")
            raise ErrorReservaInvalida("Fallo inesperado al procesar la reserva") from e
        else:
            self._costo_final = costo
            self._estado = "procesada"
            registrar_log("INFO", f"Reserva #{self._id} procesada por ${costo}")
            return costo
        finally:
            registrar_log("DEBUG", f"Intento de procesamiento de reserva #{self._id} finalizado")

    def describir(self):
        return (f"Reserva #{self._id} - {self._cliente.nombre} -> "
                f"{self._servicio.nombre} ({self._duracion}) [{self._estado}]")

