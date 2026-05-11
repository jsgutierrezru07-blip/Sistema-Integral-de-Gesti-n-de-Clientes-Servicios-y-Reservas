"""Clase abstracta base para todas las entidades del sistema."""

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    # contador global para asignar ids únicos
    _contador = 0

    def __init__(self):
        Entidad._contador += 1
        self._id = Entidad._contador
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        # cada entidad debe saber describirse
        pass

