from __future__ import annotations

from abc import ABC, abstractmethod

from excepciones import ValidacionClienteError

class EntidadSistema(ABC):
    """Base abstracta de entidades del sistema."""

    def __init__(self, identificador: str) -> None:
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador debe ser un texto no vacio")
        self._id = identificador.strip()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def resumen(self) -> str:
        """Devuelve una representacion corta de la entidad."""

class Cliente(EntidadSistema):
    """Representa un cliente con validaciones robustas."""

    _PATRON_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
    _PATRON_TELEFONO = re.compile(r"^\+?\d{7,15}$")

    def __init__(self, identificador: str, nombre: str, email: str, telefono: str) -> None:
        super().__init__(identificador)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionClienteError("El nombre debe tener al menos 3 caracteres")
        self._nombre = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        if not isinstance(valor, str) or not self._PATRON_EMAIL.match(valor.strip()):
            raise ValidacionClienteError("El email no tiene un formato valido")
        self._email = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str) or not self._PATRON_TELEFONO.match(valor.strip()):
            raise ValidacionClienteError("El telefono debe contener entre 7 y 15 digitos")
        self._telefono = valor.strip()

    def resumen(self) -> str:
        return f"Cliente({self.id}) {self.nombre} - {self.email}"


