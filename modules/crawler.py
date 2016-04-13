import requests

from modules.util import Util
from modules.twse_api_client import TWSEAPIClient
from modules.logger import Logger

logger, _ = Logger.get_instance()

class Crawler(Util):

    def __init__(self, url, stocks, count=100):
        self.url = url
        self.querys = list()
        idx = 0
        length = len(stocks)

        while idx < length:
            query = '|'.join(stocks[idx:idx + count])
            self.querys.append(query)
            idx = idx + count

    def run(self):
        msgArrays = list()

        for query in self.querys:
            twse_api_client = TWSEAPIClient(self.url, query)
            result, msgArray = twse_api_client.get()
        
            if result:
                msgArrays.extend(msgArray)

        return self.convert(msgArrays)
