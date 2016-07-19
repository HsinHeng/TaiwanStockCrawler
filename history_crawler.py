# pip install MySQL-python sqlalchemy
import sys
import time
import ConfigParser
from datetime import date

from modules.config_reader import ConfigReader
from modules.tse_stock import TseStock
from modules.otc_stock import OtcStock
from modules.mysqlclient import MySQLClient
from modules.logger import Logger

CONF_FILE_PATH = 'config/stock.conf'

if __name__ == '__main__':
    logger = Logger.get_instance()
    logger.info('------------------ START TO FETCH STOCK HISTORY ------------------')

    try:
        conf = ConfigReader(ConfigParser.ConfigParser(), CONF_FILE_PATH)
    except Exception as e:
        print e
        logger.error('Failed to read config file: %s', e)
        sys.exit(1)

    dbclient = MySQLClient(conf.user, conf.password, conf.host, conf.dbname)
    dbclient.create_tables()
    
    d = date(2016, 7, 18)
    tse_stock = TseStock(conf.tse_stock_list, d, dbclient)
    otc_stock = OtcStock(conf.otc_stock_list, d, dbclient)
