import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("decipher")
handler = logging.FileHandler('decipher.log')
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

