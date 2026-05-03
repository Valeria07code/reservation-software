import logging
import os

_LOG_NAME = "software_fj"


def configurar_logger() -> logging.Logger:
    """Configura registro en logs/eventos.log y devuelve el logger del sistema."""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    raiz = logging.getLogger()
    if not raiz.handlers:
        ruta = os.path.join("logs", "eventos.log")
        manejador = logging.FileHandler(ruta, encoding="utf-8")
        manejador.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        raiz.addHandler(manejador)
        raiz.setLevel(logging.INFO)

    log = logging.getLogger(_LOG_NAME)
    log.setLevel(logging.INFO)
    return log


logger = logging.getLogger(_LOG_NAME)
