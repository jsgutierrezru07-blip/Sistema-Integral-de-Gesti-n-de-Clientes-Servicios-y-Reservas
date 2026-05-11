"""Gestor central del sistema: maneja las listas de clientes, servicios y reservas."""

from cliente import Cliente
from servicios import Servicio
from reserva import Reserva
from excepciones import (
    ErrorDatosInvalidos,
    ErrorClienteNoEncontrado,
    ErrorServicioNoDisponible,
    ErrorReservaInvalida,
)
from persistencia import registrar_log


class SistemaSoftwareFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # --- clientes ---
    def registrar_cliente(self, nombre, documento, correo, telefono):
        # documento debe ser único
        for c in self._clientes:
            if c.documento == str(documento).strip():
                raise ErrorDatosInvalidos(f"Ya existe un cliente con documento {documento}")
        cliente = Cliente(nombre, documento, correo, telefono)
        self._clientes.append(cliente)
        return cliente

    def buscar_cliente(self, id_cliente):
        for c in self._clientes:
            if c.id == id_cliente:
                return c
        raise ErrorClienteNoEncontrado(f"Cliente con id {id_cliente} no existe")

    @property
    def clientes(self):
        return list(self._clientes)

    # --- servicios ---
    def agregar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ErrorDatosInvalidos("Objeto no es un servicio válido")
        self._servicios.append(servicio)
        registrar_log("INFO", f"Servicio agregado: {servicio.nombre}")
        return servicio

    def buscar_servicio(self, id_servicio):
        for s in self._servicios:
            if s.id == id_servicio:
                return s
        raise ErrorServicioNoDisponible(f"Servicio con id {id_servicio} no existe")

    @property
    def servicios(self):
        return list(self._servicios)

    # --- reservas ---
    def crear_reserva(self, id_cliente, id_servicio, duracion):
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        reserva = Reserva(cliente, servicio, duracion)
        self._reservas.append(reserva)
        return reserva

    def buscar_reserva(self, id_reserva):
        for r in self._reservas:
            if r.id == id_reserva:
                return r
        raise ErrorReservaInvalida(f"Reserva con id {id_reserva} no existe")

    @property
    def reservas(self):
        return list(self._reservas)

