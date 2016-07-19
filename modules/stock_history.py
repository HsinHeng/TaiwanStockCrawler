import requests
from datetime import date, timedelta

from modules.twse_client import TwseClient
from modules.logger import Logger

logger = Logger.get_instance()

class StockHistory(TwseClient):
    def __init__():

    '''
    def __init__(self, url, stocks, dbclient, count=100):
        self.url = url
        self.querys = list()
        self.dbclient = dbclient
        querys = list()
        idx = 0
        length = len(stocks)

        while idx < length:
            query = '|'.join(stocks[idx:idx + count])
            querys.append(query)
            idx = idx + count
       
        date_start = date(2016, 4, 1)
        dd = date.today() - timedelta(1) - date_start

        for i in range(dd.days + 1):
            date_string = (date_start + timedelta(days=i)).strftime('%Y%m%d')
            
            for query in querys:
                self.querys.append(query + '&d=' + date_string)

    def run(self):
        for query in self.querys:
            twse_api_client = TWSEAPIClient(self.url, query)
            result, msgArray = twse_api_client.get()
        
            if result:
                self.dbclient.commit_history(self.convert(msgArray))
    '''
