# apt-get install python-mysqldb
# pip install python-daemon, sqlalchemy
import sys
import time

from daemon import runner

from modules.reader import getConfig, getStockList
from modules.crawler import Crawler
from modules.mysqlclient import MySQLClient
from modules.logger import Logger

class Worker(object):

    def __init__(self, crawler, dbclient, interval=60):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/stock.pid'
        self.pidfile_timeout = 3
	self.crawler = crawler
	self.dbclient = dbclient
	self.interval = interval

    def run(self):

        while True:
	    start_at = time.time()
            self.dbclient.commit(self.crawler.run())
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
    dbclient = MySQLClient(conf.get('user'), conf.get('password'), conf.get('host'), conf.get('dbname'))
    worker = Worker(crawler, dbclient, interval=conf.get('interval'))
    daemon_runner = runner.DaemonRunner(worker)
    daemon_runner.daemon_context.files_preserve=[handler.stream]
    daemon_runner.do_action()
