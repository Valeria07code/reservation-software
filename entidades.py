from __future__ import annotations

from abc import ABC, abstractmethod

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

