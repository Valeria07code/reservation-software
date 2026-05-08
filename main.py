from __future__ import annotations

from pathlib import Path
import logging

from simulador import ejecutar_simulaciones
from menu import mostrar_menu

def _configurar_logger_fallback() -> None:
    """Configura logging local si aun no existe logger_config del equipo."""
    ruta_logs = Path("logs")
    ruta_logs.mkdir(exist_ok=True)
    ruta_archivo = ruta_logs / "eventos.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(ruta_archivo, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def iniciar_aplicacion() -> None:
    try:
        from logger_config import configurar_logger  # type: ignore

        configurar_logger()
    except Exception:
        _configurar_logger_fallback()
        logging.getLogger(__name__).warning(
            "Se usa configuracion de logger temporal por falta de logger_config definitivo"
        )

    logger = logging.getLogger(__name__)
    logger.info("Inicio del sistema integral de gestion de reservas")

    print("")
    print("Software FJ - Sistema integral de clientes, servicios y reservas (simulacion)")
    print("Los eventos y errores detallados se guardan en: logs/eventos.log")
    print("")

    try:
        mostrar_menu()
    except Exception:
        logger.exception("Ocurrio un error no controlado en la ejecucion principal")
        print("")
        print("Error grave no controlado en la ejecucion principal. Revise logs/eventos.log.")
        print("")
    finally:
        logger.info("Fin de ejecucion del sistema")
        print("Fin de la simulacion. Consulte logs/eventos.log para trazabilidad completa.")
        print("")


if __name__ == "__main__":
    iniciar_aplicacion()
