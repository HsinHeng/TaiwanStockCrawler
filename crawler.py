# pip install MySQL-python sqlalchemy
import sys
import time
import ConfigParser

from modules.logger import Logger
from modules.config_reader import ConfigReader
from modules.mysqlclient import MySQLClient
from modules.tse_stock import TseStock
from modules.otc_stock import OtcStock
from modules.taiex_tpex_stock import TaiexTpexStock

CONF_FILE_PATH = 'config/stock.conf'

if __name__ == '__main__':
    logger = Logger.get_instance()
    logger.info('------------------ STOCK WORKER START ------------------')
 
    try:
        conf = ConfigReader(ConfigParser.ConfigParser(), CONF_FILE_PATH)
    except Exception as e:
        print e
        logger.error('Failed to read config file: %s', e)
        sys.exit(1)

    dbclient = MySQLClient(conf.user, conf.password, conf.host, conf.dbname)
    dbclient.create_tables()

    taiex_tpex_stock = TaiexTpexStock()
    tse_stock = TseStock(conf.tse_stock_list)
    otc_stock = OtcStock(conf.otc_stock_list)
    data = taiex_tpex_stock.data + tse_stock.data + otc_stock.data
    #data = taiex_tpex_stock.data
    dbclient.commit_latest(data)
    dbclient.commit_history(data)

    '''
    while True:
        start_at = time.time()
        logger.info('Start to fetch data at %s', start_at)
        tse_stock = TseStock(conf.tse_stock_list)
        otc_stock = OtcStock(conf.otc_stock_list)
        dbclient.commit_latest(tse_stock.data + otc_stock.data)
        end_at = time.time()
        logger.info('Finish storing data to db at %s, spend %s sec', end_at, end_at - start_at)
        idle = conf.interval - (end_at - start_at)

        if idle > 0:
            time.sleep(idle)

    sys.exit(0)
    '''
