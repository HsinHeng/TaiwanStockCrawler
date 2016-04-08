import logging
import logging.config

CONF_FILE_PATH = 'config/stock.conf'


class Logger(object):
    __handler = None
    __logger = None

    @staticmethod
    def get_instance():
        if not Logger.__logger:
            logging.config.fileConfig(CONF_FILE_PATH)
            Logger.__logger = logging.getLogger('root')
            Logger.__hangler = Logger.__logger.parent.handlers[0]
        return Logger.__logger, Logger.__hangler
