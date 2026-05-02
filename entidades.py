from abc import ABC, abstractmethod

class Servicio(ABC):
    def __init__(self, id_servicio, nombre, precio_base):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo_final(self, *args):
        """Método abstracto que deben implementar las clases hijas"""
        pass
    
    @abstractmethod
    def describir_servicio(self):
        """Método abstracto para detallar el servicio"""
        pass