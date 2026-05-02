import logging
import os

def configurar_logger():
    # Creamos la carpeta 'logs' si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Configuramos cómo se guardarán los eventos y errores
    logging.basicConfig(
        filename='logs/eventos.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger()

# Variable global que usaremos en todo el sistema para registrar errores
logger = configurar_logger()