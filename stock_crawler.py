# pip install MySQL-python sqlalchemy
import sys
import time
import ConfigParser

from modules.logger import Logger
from modules.config_reader import ConfigReader
from modules.mysqlclient import MySQLClient
from modules.stock import Stock

CONF_FILE_PATH = 'config/stock.conf'

if __name__ == '__main__':
    log = Logger.get_instance()
    log.info('------------------ STOCK WORKER START ------------------')
 
    try:
        conf = ConfigReader(ConfigParser.ConfigParser(), CONF_FILE_PATH)
    except Exception as e:
        print e
        log.error('Failed to read config file: %s', e)
        sys.exit(1)

    db = MySQLClient(conf.user, conf.password, conf.host, conf.dbname)
    db.create_tables()

    stock = Stock(log=log)
    db.commit_latest(stock.data)
    db.commit_history(stock.data)

    '''
    while True:
        start_at = time.time()
        logger.info('Start to fetch data at %s', start_at)
        stock = Stock()
        dbclient.commit_latest(stock.data)
        dbclient.commit_history(stock.data)
        end_at = time.time()
        logger.info('Finish storing data to db at %s, spend %s sec', end_at, end_at - start_at)
        idle = conf.interval - (end_at - start_at)

        if idle > 0:
            time.sleep(idle)

    sys.exit(0)
    '''
