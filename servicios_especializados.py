from entidades import Servicio
from logger_config import logger


# --- Servicio: reserva de salas por horas (catering opcional en calcular_costo_final) ---


class ServicioSala(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, capacidad_personas):
        super().__init__(id_servicio, nombre, precio_base)
        if not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            logger.error(f"Error al crear ServicioSala '{nombre}': Capacidad inválida ({capacidad_personas}).")
            raise ValueError("La capacidad de personas debe ser un número entero positivo.")
        self.capacidad_personas = capacidad_personas

    def validar_parametros(self, duracion_horas):
        # Mismas reglas que la validación estricta de horas en calcular_costo_final
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise ValueError("Las horas de reserva deben ser un número mayor a cero.")

    def calcular_costo(self, duracion_horas, impuesto=None, descuento=None):
        # Contrato abstracto: reutiliza la lógica del compañero y aplica impuesto/descuento de la reserva
        self.validar_parametros(duracion_horas)
        subtotal = self.calcular_costo_final(
            float(duracion_horas),
            incluye_catering=False,
            registrar_resumen=False,
        )
        if descuento is not None:
            subtotal *= 1.0 - descuento
        if impuesto is not None:
            subtotal *= 1.0 + impuesto
        total = float(subtotal)
        logger.info(
            f"Total de reserva (sala '{self.nombre}'): {total:.0f} pesos "
            f"(incluye descuento e impuesto de la reserva si se indicaron)."
        )
        return total

    def calcular_costo_final(self, horas, incluye_catering=False, registrar_resumen=True):
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
                costo += 350000
            if registrar_resumen:
                logger.info(f"Cálculo exitoso para sala '{self.nombre}'. Total calculado: {costo:.0f} pesos")
            return costo

        finally:
            # Esto se ejecuta siempre, haya error o no (solo mensaje detallado si se registra resumen)
            if registrar_resumen:
                logger.info(f"Operación de cálculo finalizada para el servicio de sala '{self.nombre}'.")

    def describir_servicio(self):
        return f"Reserva de Sala: {self.nombre} (Capacidad máxima: {self.capacidad_personas} personas)."


# --- Alquiler de equipos: precio por día entero y seguro opcional en calcular_costo_final ---


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, requiere_deposito):
        super().__init__(id_servicio, nombre, precio_base)
        if not isinstance(requiere_deposito, bool):
            logger.error(f"Error en AlquilerEquipo '{nombre}': requiere_deposito debe ser booleano.")
            raise TypeError("El parámetro 'requiere_deposito' debe ser True o False.")
        self.requiere_deposito = requiere_deposito

    def validar_parametros(self, duracion_horas):
        # La reserva usa duracion_horas como número de días (enteros)
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise ValueError("La duración debe ser un número positivo.")
        if float(duracion_horas) != int(duracion_horas):
            raise ValueError("El alquiler se cotiza por días enteros.")
        if int(duracion_horas) <= 0:
            raise ValueError("Los días de alquiler deben ser un número entero positivo.")

    def calcular_costo(self, duracion_horas, impuesto=None, descuento=None):
        self.validar_parametros(duracion_horas)
        dias = int(duracion_horas)
        subtotal = self.calcular_costo_final(dias, aplicar_seguro=True, registrar_resumen=False)
        if descuento is not None:
            subtotal *= 1.0 - descuento
        if impuesto is not None:
            subtotal *= 1.0 + impuesto
        total = float(subtotal)
        logger.info(
            f"Total de reserva (equipo '{self.nombre}'): {total:.0f} pesos "
            f"(incluye descuento e impuesto de la reserva si se indicaron)."
        )
        return total

    def calcular_costo_final(self, dias, aplicar_seguro=True, registrar_resumen=True):
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
            if registrar_resumen:
                logger.info(f"Procesamiento de cálculo de equipo '{self.nombre}' concluido.")

    def describir_servicio(self):
        deposito = "Sí" if self.requiere_deposito else "No"
        return f"Alquiler de Equipo: {self.nombre} (Requiere depósito: {deposito})."


# --- Asesorías: cobro por sesiones; descuento estudiante en porcentaje en calcular_costo_final ---


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, area_experta):
        super().__init__(id_servicio, nombre, precio_base)
        if not isinstance(area_experta, str) or not area_experta.strip():
            logger.error(f"Error en AsesoriaEspecializada '{nombre}': Área experta vacía.")
            raise ValueError("El área experta debe ser un texto válido y no vacío.")
        self.area_experta = area_experta

    def validar_parametros(self, duracion_horas):
        # En reservas, duracion_horas representa cantidad de sesiones (enteras)
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise ValueError("El número de sesiones debe ser positivo.")
        if float(duracion_horas) != int(duracion_horas):
            raise ValueError("Las sesiones deben ser un número entero.")
        if int(duracion_horas) < 1:
            raise ValueError("El número de sesiones debe ser un entero positivo.")

    def calcular_costo(self, duracion_horas, impuesto=None, descuento=None):
        self.validar_parametros(duracion_horas)
        sesiones = int(duracion_horas)
        # Sin descuento estudiante aquí: lo aplica la reserva con descuento (fracción 0-1)
        subtotal = self.calcular_costo_final(
            sesiones,
            descuento_estudiante=0,
            registrar_resumen=False,
        )
        if descuento is not None:
            subtotal *= 1.0 - descuento
        if impuesto is not None:
            subtotal *= 1.0 + impuesto
        total = float(subtotal)
        logger.info(
            f"Total de reserva (asesoría '{self.nombre}'): {total:.0f} pesos "
            f"(incluye descuento e impuesto de la reserva si se indicaron)."
        )
        return total

    def calcular_costo_final(self, sesiones, descuento_estudiante=0, registrar_resumen=True):
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
            if registrar_resumen:
                logger.info(f"Cálculo de asesoría '{self.nombre}' procesado en el sistema.")

    def describir_servicio(self):
        return f"Asesoría Especializada en {self.area_experta}: {self.nombre}."
