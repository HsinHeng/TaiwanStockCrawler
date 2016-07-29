# pip install MySQL-python sqlalchemy
import sys
import time
import ConfigParser

from modules.config_reader import ConfigReader
from modules.stock import Stock
from modules.mysqlclient import MySQLClient
from modules.logger import Logger

CONF_FILE_PATH = 'config/stock.conf'

if __name__ == '__main__':
    log = Logger.get_instance()
    log.info('------------------ START TO FETCH STOCK HISTORY ------------------')

    try:
        conf = ConfigReader(ConfigParser.ConfigParser(), CONF_FILE_PATH)
    except Exception as e:
        print e
        log.error('Failed to read config file: %s', e)
        sys.exit(1)

    db = MySQLClient(conf.user, conf.password, conf.host, conf.dbname)
    db.create_tables()
    Stock(None, from_date=conf.from_date, db=db, log=log)
