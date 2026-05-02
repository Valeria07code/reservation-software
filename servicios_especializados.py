from entidades import Servicio
from logger_config import logger

class ServicioSala(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, capacidad_personas):
        super().__init__(id_servicio, nombre, precio_base)
        if not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            logger.error(f"Error al crear ServicioSala '{nombre}': Capacidad inválida ({capacidad_personas}).")
            raise ValueError("La capacidad de personas debe ser un número entero positivo.")
        self.capacidad_personas = capacidad_personas

    def calcular_costo_final(self, horas, incluye_catering=False):
        try:
            # Validación estricta de parámetros
            if not isinstance(horas, (int, float)) or horas <= 0:
                raise ValueError("Las horas de reserva deben ser un número mayor a cero.")
            
            costo = self.precio_base * horas
            
        except ValueError as e:
            # Capturamos el error específico y lo mandamos al archivo log
            logger.warning(f"Intento de cálculo fallido en sala '{self.nombre}': {e}")
            raise  # Relanzamos el error para que el simulador lo maneje
            
        except Exception as e:
            # Captura de cualquier otro error inesperado
            logger.critical(f"Error crítico e inesperado al calcular costo de sala: {e}")
            raise
            
        else:
            # Si el try fue exitoso, aplicamos la sobrecarga del catering
            if incluye_catering:
                costo += 50000 
            logger.info(f"Cálculo exitoso para sala '{self.nombre}'. Total calculado: ${costo}")
            return costo
            
        finally:
            # Esto se ejecuta siempre, haya error o no
            logger.info(f"Operación de cálculo finalizada para el servicio de sala '{self.nombre}'.")

    def describir_servicio(self):
        return f"Reserva de Sala: {self.nombre} (Capacidad máxima: {self.capacidad_personas} personas)."


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, requiere_deposito):
        super().__init__(id_servicio, nombre, precio_base)
        if not isinstance(requiere_deposito, bool):
            logger.error(f"Error en AlquilerEquipo '{nombre}': requiere_deposito debe ser booleano.")
            raise TypeError("El parámetro 'requiere_deposito' debe ser True o False.")
        self.requiere_deposito = requiere_deposito

    def calcular_costo_final(self, dias, aplicar_seguro=True):
        try:
            if not isinstance(dias, int) or dias <= 0:
                raise ValueError("Los días de alquiler deben ser un número entero positivo.")
            costo = self.precio_base * dias
        except Exception as e:
            logger.error(f"Fallo al calcular costo de equipo '{self.nombre}': {e}")
            raise
        else:
            if aplicar_seguro:
                costo *= 1.10  # 10% adicional de seguro
            return costo
        finally:
            logger.info(f"Procesamiento de cálculo de equipo '{self.nombre}' concluido.")

    def describir_servicio(self):
        deposito = "Sí" if self.requiere_deposito else "No"
        return f"Alquiler de Equipo: {self.nombre} (Requiere depósito: {deposito})."


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, area_experta):
        super().__init__(id_servicio, nombre, precio_base)
        if not isinstance(area_experta, str) or not area_experta.strip():
            logger.error(f"Error en AsesoriaEspecializada '{nombre}': Área experta vacía.")
            raise ValueError("El área experta debe ser un texto válido y no vacío.")
        self.area_experta = area_experta

    def calcular_costo_final(self, sesiones, descuento_estudiante=0):
        try:
            if not isinstance(sesiones, int) or sesiones <= 0:
                raise ValueError("El número de sesiones debe ser un entero positivo.")
            if not (0 <= descuento_estudiante <= 100):
                raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
            
            costo = self.precio_base * sesiones
            
        except ValueError as e:
            logger.warning(f"Validación fallida en asesoría '{self.nombre}': {e}")
            raise
        else:
            if descuento_estudiante > 0:
                costo -= (costo * descuento_estudiante / 100)
            return costo
        finally:
            logger.info(f"Cálculo de asesoría '{self.nombre}' procesado en el sistema.")

    def describir_servicio(self):
        return f"Asesoría Especializada en {self.area_experta}: {self.nombre}."