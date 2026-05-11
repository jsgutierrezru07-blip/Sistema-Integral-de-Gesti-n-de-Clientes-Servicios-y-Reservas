"""Excepciones personalizadas del sistema."""


class ErrorSoftwareFJ(Exception):
    # excepción base de toda la app
    pass


class ErrorDatosInvalidos(ErrorSoftwareFJ):
    pass


class ErrorClienteNoEncontrado(ErrorSoftwareFJ):
    pass


class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    pass


class ErrorReservaInvalida(ErrorSoftwareFJ):
    pass


class ErrorCalculoCosto(ErrorSoftwareFJ):
    pass

