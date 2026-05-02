from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
import logging
import re

from excepciones import ReservaError, ServicioNoDisponibleError, ValidacionClienteError

LOGGER = logging.getLogger(__name__)


class EntidadSistema(ABC):
    """
    Clase base abstracta para entidades del dominio (identificador unico y descripcion breve).

    Fuerza a las subclases a definir como se representa la entidad en texto corto.
    """

    def __init__(self, identificador: str) -> None:
        """
        Inicializa la entidad. El identificador debe ser un texto con contenido;
        de lo contrario se lanza un error de validacion.
        """
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador debe ser un texto no vacio")
        self._id = identificador.strip()

    @property
    def id(self) -> str:
        """Identificador unico de la entidad (solo lectura)."""
        return self._id

    @abstractmethod
    def resumen(self) -> str:
        """Devuelve una linea de texto con los datos esenciales de la entidad."""


class Cliente(EntidadSistema):
    """
    Cliente de Software FJ con datos personales encapsulados y validados.

    El email y el telefono se validan al asignar; los datos invalidos lanzan
    ValidacionClienteError.
    """

    _PATRON_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
    _PATRON_TELEFONO = re.compile(r"^\+?\d{7,15}$")

    def __init__(self, identificador: str, nombre: str, email: str, telefono: str) -> None:
        """
        Crea el cliente y aplica de inmediato las reglas de nombre, correo y telefono.
        """
        super().__init__(identificador)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Nombre del cliente (minimo 3 caracteres validos)."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionClienteError("El nombre debe tener al menos 3 caracteres")
        self._nombre = valor.strip()

    @property
    def email(self) -> str:
        """Correo electronico normalizado en minusculas."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        if not isinstance(valor, str) or not self._PATRON_EMAIL.match(valor.strip()):
            raise ValidacionClienteError("El email no tiene un formato valido")
        self._email = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Telefono de contacto segun patron definido en la clase."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str) or not self._PATRON_TELEFONO.match(valor.strip()):
            raise ValidacionClienteError("El telefono debe contener entre 7 y 15 digitos")
        self._telefono = valor.strip()

    def resumen(self) -> str:
        """Linea con id, nombre y email del cliente."""
        return f"Cliente({self.id}) {self.nombre} - {self.email}"


class Servicio(EntidadSistema, ABC):
    """
    Servicio ofrecido por Software FJ (contrato comun para todas las especializaciones).

    Las subclases deben implementar validacion de parametros, calculo de costo y descripcion.
    """

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool = True) -> None:
        """
        Guarda el nombre publico, la tarifa base positiva y si el servicio esta activo
        para nuevas reservas.
        """
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del servicio es obligatorio")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ValueError("La tarifa base debe ser mayor a cero")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        """Nombre del servicio."""
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        """Tarifa base antes de reglas especificas de cada tipo de servicio."""
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        """Indica si el servicio acepta nuevas reservas en este momento."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    @abstractmethod
    def validar_parametros(self, duracion_horas: float) -> None:
        """
        Comprueba que la duracion y demas reglas del servicio concreto se cumplan.
        """

    @abstractmethod
    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float | None = None,
        descuento: float | None = None,
    ) -> float:
        """
        Obtiene el monto total a partir de la duracion y, si aplica, impuesto o descuento.
        """

    @abstractmethod
    def describir_servicio(self) -> str:
        """Texto breve que explica que incluye o cubre el servicio."""

    def resumen(self) -> str:
        """Linea con id, nombre y tarifa base."""
        return f"Servicio({self.id}) {self.nombre} - tarifa base {self.tarifa_base:.2f}"


class Reserva(EntidadSistema):
    """
    Vincula un cliente con un servicio, duracion y estado del ciclo de reserva.

    Estados tipicos: pendiente, confirmada, cancelada, procesada. La confirmacion y el
    procesamiento registran excepciones y eventos en el log del modulo.
    """

    ESTADOS_VALIDOS = {"pendiente", "confirmada", "cancelada", "procesada"}

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion_horas: float) -> None:
        """
        Registra quien reserva, que servicio, cuantas horas y deja el flujo en pendiente
        con la fecha de creacion.
        """
        super().__init__(identificador)
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = float(duracion_horas)
        self._estado = "pendiente"
        self._creada_en = datetime.now()

    @property
    def cliente(self) -> Cliente:
        """Cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        """Servicio contratado."""
        return self._servicio

    @property
    def duracion_horas(self) -> float:
        """Duracion acordada en horas."""
        return self._duracion_horas

    @property
    def estado(self) -> str:
        """Estado actual del flujo de la reserva."""
        return self._estado

    def confirmar(self) -> None:
        """
        Intenta dejar la reserva confirmada solo si el estado lo permite, el servicio
        esta disponible y la duracion cumple las reglas del tipo de servicio.
        """
        try:
            if self._estado != "pendiente":
                raise ReservaError(f"No se puede confirmar una reserva en estado {self._estado}")
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError("El servicio solicitado no esta disponible")
            self.servicio.validar_parametros(self.duracion_horas)
        except (ServicioNoDisponibleError, ValueError) as error:
            LOGGER.exception("Error al confirmar reserva %s", self.id)
            raise ReservaError(f"Fallo la confirmacion de la reserva {self.id}") from error
        else:
            self._estado = "confirmada"
            LOGGER.info("Reserva %s confirmada correctamente", self.id)
        finally:
            LOGGER.debug("Finaliza intento de confirmacion para reserva %s", self.id)

    def cancelar(self, motivo: str | None = None) -> None:
        """
        Anula la reserva cuando aun no esta cerrada como procesada; el motivo opcional
        queda registrado para seguimiento.
        """
        if self._estado == "procesada":
            raise ReservaError("No se puede cancelar una reserva ya procesada")
        self._estado = "cancelada"
        LOGGER.warning("Reserva %s cancelada. Motivo: %s", self.id, motivo or "sin detalle")

    def procesar(self, impuesto: float | None = None, descuento: float | None = None) -> float:
        """
        Calcula el cobro con el servicio (confirmando antes si aun estaba pendiente),
        descarta reservas canceladas y marca el cierre como procesada cuando todo sale bien.
        """
        total = 0.0
        try:
            if self._estado == "cancelada":
                raise ReservaError("No se puede procesar una reserva cancelada")
            if self._estado == "pendiente":
                self.confirmar()

            total = self.servicio.calcular_costo(
                duracion_horas=self.duracion_horas,
                impuesto=impuesto,
                descuento=descuento,
            )
            if total <= 0:
                raise ValueError("El total calculado no es consistente")
        except (ValueError, ReservaError) as error:
            LOGGER.exception("Error al procesar reserva %s", self.id)
            raise ReservaError(f"No fue posible procesar la reserva {self.id}") from error
        else:
            self._estado = "procesada"
            LOGGER.info("Reserva %s procesada con total %.2f", self.id, total)
            return total
        finally:
            LOGGER.debug("Cierre de procesamiento para reserva %s", self.id)

    def resumen(self) -> str:
        """Linea con id de reserva, nombre del cliente, servicio y estado."""
        return (
            f"Reserva({self.id}) cliente={self.cliente.nombre} "
            f"servicio={self.servicio.nombre} estado={self.estado}"
        )
