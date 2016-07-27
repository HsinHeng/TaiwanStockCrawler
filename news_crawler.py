# pip install MySQL-python sqlalchemy
import sys
import time
import json
import ConfigParser

from modules.config_reader import ConfigReader
from modules.google_news import GoogleNews
from modules.mysqlclient import MySQLClient
from modules.logger import Logger

CONF_FILE_PATH = 'config/stock.conf'

if __name__ == '__main__':
    logger = Logger.get_instance()
    logger.info('------------------ START TO FETCH GOOGLE NEWS ------------------')

    try:
        conf = ConfigReader(ConfigParser.ConfigParser(), CONF_FILE_PATH)
    except Exception as e:
        print e
        logger.error('Failed to read config file: %s', e)
        sys.exit(1)

    dbclient = MySQLClient(conf.user, conf.password, conf.host, conf.dbname)
    dbclient.create_tables()
 
    google_news = GoogleNews('%E5%8F%B0%E8%82%A1')
    dbclient.commit_news(google_news.data)
    
