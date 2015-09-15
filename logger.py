import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("decipher")
handler = logging.FileHandler('hello.log')
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

