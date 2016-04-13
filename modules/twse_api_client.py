import requests
import json
import time

from modules.logger import Logger

logger, _ = Logger.get_instance()


class TWSEAPIClient(object):

    def __init__(self, url, query, timeout=10):
        self.url = url
        self.query = query
        self.timeout = timeout
        self.client = requests.session()

    def get(self):
        try:
            self.client.get(self.url, timeout=self.timeout)
	    logger.debug('fetch data from %s', self.url + self.query)
            res = self.client.get(self.url + self.query, timeout=self.timeout)
        except Exception as e:
            logger.warning('(X) Timeout %s', self.url + self.query)
            return False, None

        if res.status_code != 200:
            logger.warning('(X) Status code %s from %s', res.status_code, self.url + self.query)
            return False, None
        
        msgArray = json.loads(res.content).get('msgArray')

        if msgArray is None:
            logger.warning('(X) Retrieve %s stock information from %s', len(msgArray), self.url + self.query)
            return False, None

        logger.info('Retrieve %s stock information', len(msgArray))
        return True, msgArray
