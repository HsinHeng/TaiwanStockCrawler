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
    log = Logger.get_instance()
    log.info('------------------ START TO FETCH GOOGLE NEWS ------------------')

    try:
        conf = ConfigReader(ConfigParser.ConfigParser(), CONF_FILE_PATH)
    except Exception as e:
        print e
        log.error('Failed to read config file: %s', e)
        sys.exit(1)

    db = MySQLClient(conf.user, conf.password, conf.host, conf.dbname)
    db.create_tables()
 
    for keyword in conf.keywords:
        google_news = GoogleNews(keyword, log=log)
        db.commit_news(google_news.data)
    
