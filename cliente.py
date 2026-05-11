"""Clase Cliente con validaciones y encapsulación."""

import re

from entidad import Entidad
from excepciones import ErrorDatosInvalidos
from persistencia import registrar_log


class Cliente(Entidad):
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # los setters validan los datos
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        registrar_log("INFO", f"Cliente creado: {self._nombre} ({self._documento})")

    # nombre
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ErrorDatosInvalidos("El nombre debe tener al menos 3 caracteres")
        self._nombre = valor.strip()

    # documento
    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) < 6:
            raise ErrorDatosInvalidos("Documento debe ser numérico y tener al menos 6 dígitos")
        self._documento = valor

    # correo
    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
        if not isinstance(valor, str) or not re.match(patron, valor):
            raise ErrorDatosInvalidos("Correo electrónico inválido")
        self._correo = valor.strip()

    # telefono
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) < 7:
            raise ErrorDatosInvalidos("Teléfono debe ser numérico y tener al menos 7 dígitos")
        self._telefono = valor

    def describir(self):
        return f"Cliente #{self._id} - {self._nombre} (doc: {self._documento})"

