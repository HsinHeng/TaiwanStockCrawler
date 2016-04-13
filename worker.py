# pip install MySQL-python sqlalchemy
import sys
import time

from modules.reader import getConfig, getStockList
from modules.crawler import Crawler
from modules.mysqlclient import MySQLClient
from modules.logger import Logger


class Worker(object):
    def __init__(self, crawler, dbclient, interval=30):
        self.crawler = crawler
        self.dbclient = dbclient
        self.interval = interval

    def run(self):
        while True:
            start_at = time.time()
            self.dbclient.commit_latest(self.crawler.run())
            idle = self.interval - (time.time() - start_at)

            if idle > 0:
                time.sleep(idle)


if __name__ == '__main__':
    global logger
    logger, handler = Logger.get_instance()
    logger.info('------------------ STOCK WORKER START ------------------')

    result, conf = getConfig()

    if not result:
        logger.error('Failed to read config file')
        sys.exit(1)

    stocks = getStockList(conf.get('file'))

    if not stocks:
        logger.error('Failed to read csv file')
        sys.exit(1)

    crawler = Crawler(conf.get('url'), stocks)
    dbclient = MySQLClient(
        conf.get('user'), conf.get('password'), conf.get('host'),
        conf.get('dbname'))
    worker = Worker(crawler, dbclient, interval=conf.get('interval'))
    worker.run()
