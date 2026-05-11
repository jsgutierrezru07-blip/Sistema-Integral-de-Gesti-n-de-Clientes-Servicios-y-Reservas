"""Servicio abstracto y sus tres especializaciones."""

from abc import abstractmethod

from entidad import Entidad
from excepciones import ErrorDatosInvalidos, ErrorCalculoCosto, ErrorSoftwareFJ


class Servicio(Entidad):
    def __init__(self, nombre, precio_base, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or len(nombre.strip()) == 0:
            raise ErrorDatosInvalidos("El servicio requiere un nombre válido")
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise ErrorDatosInvalidos("El precio base debe ser mayor a 0")
        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    def marcar_no_disponible(self):
        self._disponible = False

    def marcar_disponible(self):
        self._disponible = True

    @abstractmethod
    def validar_parametros(self, duracion):
        # cada servicio define sus propias reglas
        pass

    # Sobrecarga vía parámetros opcionales:
    # - solo duracion -> costo base
    # - + impuesto    -> aplica iva
    # - + descuento   -> aplica descuento
    # - ambos         -> aplica ambos
    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        try:
            self.validar_parametros(duracion)
            costo = self._precio_base * duracion
            if descuento is not None:
                if descuento < 0 or descuento > 100:
                    raise ErrorCalculoCosto("Descuento fuera de rango (0-100)")
                costo = costo - (costo * descuento / 100)
            if impuesto is not None:
                if impuesto < 0:
                    raise ErrorCalculoCosto("Impuesto no puede ser negativo")
                costo = costo + (costo * impuesto / 100)
            return round(costo, 2)
        except ErrorSoftwareFJ:
            # propagamos los errores de dominio
            raise
        except Exception as e:
            # cualquier otro error queda encadenado
            raise ErrorCalculoCosto("Fallo inesperado al calcular costo") from e

    @abstractmethod
    def describir(self):
        pass


class ReservaSala(Servicio):
    # precio por hora
    def __init__(self, nombre, precio_base, capacidad, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ErrorDatosInvalidos("Capacidad inválida para la sala")
        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorDatosInvalidos("Duración inválida para la sala")
        if duracion > 12:
            raise ErrorDatosInvalidos("Las salas no se reservan por más de 12 horas")

    def describir(self):
        estado = "disponible" if self._disponible else "no disponible"
        return f"Sala '{self._nombre}' cap. {self._capacidad} - ${self._precio_base}/h ({estado})"


class AlquilerEquipo(Servicio):
    # precio por día
    def __init__(self, nombre, precio_base, tipo_equipo, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ErrorDatosInvalidos("Tipo de equipo inválido")
        self._tipo_equipo = tipo_equipo.strip()

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorDatosInvalidos("Días de alquiler inválidos")
        if duracion > 30:
            raise ErrorDatosInvalidos("Alquiler máximo de 30 días")

    def describir(self):
        estado = "disponible" if self._disponible else "no disponible"
        return f"Equipo '{self._nombre}' ({self._tipo_equipo}) - ${self._precio_base}/día ({estado})"


class AsesoriaEspecializada(Servicio):
    # precio por hora
    def __init__(self, nombre, precio_base, area, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        if not isinstance(area, str) or not area.strip():
            raise ErrorDatosInvalidos("Área de asesoría inválida")
        self._area = area.strip()

    @property
    def area(self):
        return self._area

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorDatosInvalidos("Horas de asesoría inválidas")
        if duracion < 1:
            raise ErrorDatosInvalidos("La asesoría mínima es de 1 hora")

    # las asesorías tienen un mínimo de sesión
    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        costo = super().calcular_costo(duracion, impuesto, descuento)
        if costo < 50000:
            costo = 50000
        return costo

    def describir(self):
        estado = "disponible" if self._disponible else "no disponible"
        return f"Asesoría '{self._nombre}' área {self._area} - ${self._precio_base}/h ({estado})"

