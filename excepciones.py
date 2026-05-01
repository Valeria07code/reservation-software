class ValidacionClienteError(Exception):
    """Error lanzado cuando los datos del cliente no son validos."""


class ServicioNoDisponibleError(Exception):
    """Error lanzado cuando un servicio no esta disponible."""


class ReservaError(Exception):
    """Error general para fallos durante la gestion de reservas."""
