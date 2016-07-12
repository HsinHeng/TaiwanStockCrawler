import logging
import logging.config

CONF_FILE_PATH = 'config/stock.conf'

class Logger(object):
    __instance = None

    @staticmethod
    def get_instance():
        if not Logger.__instance:
            Logger()
        return Logger.__instance


    def __init__(self):
        logging.config.fileConfig(CONF_FILE_PATH)
        Logger.__instance = logging.getLogger('root')
