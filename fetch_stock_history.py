# pip install MySQL-python sqlalchemy
import sys
import time

from modules.reader import getConfig, getStockList
from modules.history_crawler import HistoryCrawler
from modules.mysqlclient import MySQLClient
from modules.logger import Logger

if __name__ == '__main__':
    logger, handler = Logger.get_instance()
    logger.info('------------------ START TO FETCH STOCK HISTORY ------------------')

    result, conf = getConfig()

    if not result:
        logger.error('Failed to read config file')
        sys.exit(1)

    stocks = getStockList(conf.get('file'))

    if not stocks:
        logger.error('Failed to read csv file')
        sys.exit(1)

    dbclient = MySQLClient(
        conf.get('user'), conf.get('password'), conf.get('host'),
        conf.get('dbname'))
    crawler = HistoryCrawler(conf.get('url'), stocks, dbclient)
    crawler.run()
