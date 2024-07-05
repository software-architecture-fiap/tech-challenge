import logging
import os
from datetime import datetime

# Criação do diretório de logs se não existir
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuração do nome do arquivo de log baseado na data atual
log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
log_filepath = os.path.join(log_directory, log_filename)

# Configuração do logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Application")
