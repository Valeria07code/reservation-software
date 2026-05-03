from __future__ import annotations

from collections.abc import Callable

"""
Demostracion automatica del sistema: operaciones validas e invalidas en secuencia.

Los listados en memoria (clientes, servicios, reservas) simulan un registro sin base de datos.
El archivo logs/eventos.log conserva la trazabilidad completa; aqui solo se resume en consola.
"""

import logging

from entidades import Cliente, Reserva, Servicio
from excepciones import ReservaError, ValidacionClienteError
from servicios_especializados import AlquilerEquipo, AsesoriaEspecializada, ServicioSala

LOGGER = logging.getLogger(__name__)


def _texto_motivo_error(exc: BaseException) -> str:
    """Mensaje principal y, si hay cadena raise ... from ..., la causa mas especifica al final."""
    base = str(exc).strip()
    raiz = exc
    while raiz.__cause__ is not None:
        raiz = raiz.__cause__
    if raiz is not exc:
        return f"{base} (causa especifica: {raiz})"
    return base


def ejecutar_simulaciones() -> None:
    """
    Recorre una lista de operaciones de prueba. Cada una se aísla: si falla, se registra
    y el programa sigue con la siguiente.
    """
    LOGGER.info("Inicio de simulaciones del sistema de reservas")

    clientes: list[Cliente] = []
    servicios: list[Servicio] = []
    reservas: list[Reserva] = []

    def paso(
        numero: int,
        detalle_consola: str,
        titulo_log: str,
        operacion,
        mensaje_exito: str | Callable[[], str],
    ) -> None:
        """Escribe en consola el paso numerado con datos; ejecuta y muestra resultado o motivo del fallo."""
        LOGGER.info("Operacion: %s", titulo_log)
        print(f"{numero}. {detalle_consola}")
        try:
            operacion()
            texto_exito = mensaje_exito() if callable(mensaje_exito) else mensaje_exito
            print(f"   Resultado: {texto_exito}")
        except Exception as exc:
            LOGGER.exception("Fallo controlado en operacion: %s", titulo_log)
            print("   Resultado: fallo.")
            print(f"   Motivo: {_texto_motivo_error(exc)}")
        finally:
            LOGGER.info("Fin de operacion: %s", titulo_log)
        print("")

    print("")
    print("Operaciones de prueba (detalle tecnico en logs/eventos.log):")
    print("")

    paso(
        1,
        "Crear cliente: id=C-001, nombre=Ana Perez, email=ana@correo.com, telefono=+573001112233",
        "crear cliente valido 1",
        lambda: clientes.append(Cliente("C-001", "Ana Perez", "ana@correo.com", "+573001112233")),
        "Creacion valida. Cliente registrado con datos correctos.",
    )

    paso(
        2,
        "Crear cliente: id=C-002, nombre=Luis Rojas, email=luis@correo.com, telefono=+573004445566",
        "crear cliente valido 2",
        lambda: clientes.append(Cliente("C-002", "Luis Rojas", "luis@correo.com", "+573004445566")),
        "Creacion valida. Cliente registrado con datos correctos.",
    )

    paso(
        3,
        "Crear cliente: id=C-003, nombre=Error Mail, email=correo-invalido, telefono=+573001112233",
        "crear cliente con email invalido",
        lambda: clientes.append(Cliente("C-003", "Error Mail", "correo-invalido", "+573001112233")),
        "Creacion valida.",
    )

    paso(
        4,
        "Crear cliente: id=C-004, nombre=Error Telefono, email=ok@correo.com, telefono=123",
        "crear cliente con telefono invalido",
        lambda: clientes.append(Cliente("C-004", "Error Telefono", "ok@correo.com", "123")),
        "Creacion valida.",
    )

    paso(
        5,
        "Crear servicio sala: id=S-001, nombre=Sala de juntas, precio_base=95000 (pesos por hora), capacidad_personas=12",
        "crear servicio sala",
        lambda: servicios.append(ServicioSala("S-001", "Sala de juntas", 95000.0, 12)),
        "Servicio creado correctamente (reserva de sala).",
    )

    paso(
        6,
        "Crear servicio alquiler de equipo: id=S-002, nombre=Video beam, precio_base=48000 (pesos por dia), requiere_deposito=True",
        "crear servicio equipo",
        lambda: servicios.append(AlquilerEquipo("S-002", "Video beam", 48000.0, True)),
        "Servicio creado correctamente (alquiler de equipo).",
    )

    paso(
        7,
        "Crear servicio asesoria: id=S-003, nombre=Mentoria tecnica, precio_base=175000 (pesos por sesion), area_experta=Desarrollo software",
        "crear servicio asesoria",
        lambda: servicios.append(
            AsesoriaEspecializada("S-003", "Mentoria tecnica", 175000.0, "Desarrollo software")
        ),
        "Servicio creado correctamente (asesoria especializada).",
    )

    paso(
        8,
        "Crear reserva: id=R-001, cliente=C-001 (Ana Perez), servicio=S-001 (Sala de juntas), duracion_horas=2.0",
        "crear reserva valida",
        lambda: reservas.append(Reserva("R-001", clientes[0], servicios[0], 2.0)),
        "Reserva creada en estado pendiente.",
    )

    total_procesado: dict[str, float] = {}

    def _operacion_procesar_r001() -> None:
        total_procesado["valor"] = reservas[0].procesar(impuesto=0.19, descuento=0.05)

    def _mensaje_procesar_r001() -> str:
        t = total_procesado.get("valor", 0.0)
        return (
            f"Procesamiento valido. Reserva confirmada. Total de la operacion: {t:.0f} pesos "
            "(coincide con el registro en logs/eventos.log)."
        )

    paso(
        9,
        "Procesar reserva R-001: impuesto=0.19 (19%), descuento=0.05 (5%)",
        "procesar reserva valida",
        _operacion_procesar_r001,
        _mensaje_procesar_r001,
    )

    paso(
        10,
        "Crear reserva: id=R-002, cliente=C-002 (Luis Rojas), servicio=S-003 (asesoria), duracion_horas=0.5 (sesiones no enteras)",
        "crear reserva con duracion invalida asesoria",
        lambda: reservas.append(Reserva("R-002", clientes[1], servicios[2], 0.5)),
        "Objeto reserva creado en memoria (la validacion de sesiones ocurre al confirmar o procesar).",
    )

    paso(
        11,
        "Procesar reserva R-002 (sesiones invalidas para asesoria)",
        "intentar procesar reserva con sesiones invalidas",
        lambda: reservas[-1].procesar(),
        "Procesamiento completado.",
    )

    paso(
        12,
        "Confirmar reserva R-003 sobre equipo S-002 con servicio marcado como no disponible (3 dias de alquiler)",
        "confirmar reserva con servicio no disponible",
        lambda: _simular_servicio_no_disponible(clientes, servicios, reservas),
        "Confirmacion exitosa.",
    )

    paso(
        13,
        "Crear reserva id=R-004, cliente=C-002, servicio=S-003 (asesoria), duracion=2.0 sesiones; "
        "luego cancelar (motivo: cliente solicito ajuste de agenda) e intentar procesar",
        "cancelar y luego procesar reserva",
        lambda: _simular_cancelacion_y_proceso(clientes, servicios, reservas),
        "Flujo completado.",
    )

    paso(
        14,
        "Acceso a lista de clientes en indice 99 (lista mas corta)",
        "forzar error de indice en lista",
        lambda: LOGGER.info(clientes[99]),
        "Operacion completada.",
    )

    LOGGER.info(
        "Simulaciones finalizadas. Clientes validos: %s, Servicios: %s, Reservas: %s",
        len(clientes),
        len(servicios),
        len(reservas),
    )

    print(
        "Resumen en memoria: "
        f"{len(clientes)} clientes, {len(servicios)} servicios, {len(reservas)} reservas registradas."
    )
    print("")


def _simular_servicio_no_disponible(clientes: list[Cliente], servicios: list[Servicio], reservas: list[Reserva]) -> None:
    if not clientes or not servicios:
        raise ReservaError("No hay datos base para simular reserva no disponible")

    servicio = servicios[1]
    servicio.disponible = False
    try:
        reserva = Reserva("R-003", clientes[0], servicio, 3.0)
        reservas.append(reserva)
        reserva.confirmar()
    finally:
        servicio.disponible = True


def _simular_cancelacion_y_proceso(clientes: list[Cliente], servicios: list[Servicio], reservas: list[Reserva]) -> None:
    if len(clientes) < 2 or len(servicios) < 3:
        raise ValidacionClienteError("No hay informacion suficiente para ejecutar la simulacion")

    reserva = Reserva("R-004", clientes[1], servicios[2], 2.0)
    reservas.append(reserva)
    reserva.cancelar("cliente solicito ajuste de agenda")
    reserva.procesar()
