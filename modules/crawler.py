import requests
import json
import time

from modules.twse_api_client import TWSEAPIClient
from modules.logger import Logger

logger, _ = Logger.get_instance()

class Crawler(object):

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

        return self.__convert(msgArrays)

    def __convert(self, msgArrays):
        stocks = dict()
        updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        for row in msgArrays:
            number = row.get('c')

            if not number:
                continue

            stocks.setdefault(number, {
                'number': number,
                'name': row.get('n'),
                'latest_price': row.get('z', -1),
                'highest_price': row.get('h', -1),
                'lowest_price': row.get('l', -1),
                'opening_price': row.get('o', -1),
                'limit_up': row.get('u', -1),
                'limit_down': row.get('w', -1),
                'yesterday_price': row.get('y', -1),
                'temporal_volume': self.__to_number(row.get('tv', -1)),
                'volume': row.get('v', -1),
                'top5_sold_prices': self.__to_json(row.get('a', '')),
                'top5_sold_count': self.__to_json(row.get('f', '')),
                'top5_buy_prices': self.__to_json(row.get('b', '')),
                'top5_buy_count': self.__to_json(row.get('g', '')),
                'record_time': self.__to_datetime(
                    row.get('tlong'), row.get('d'), row.get('t')),
                'updated_at': updated_at,
            })

        return stocks

    def __to_number(self, number):
        return -1 if number == '-' else number

    def __to_json(self, string):
        return json.dumps(string.split('_')[:-1])

    def __to_datetime(self, tlong, d, t):
        datetime = None

        if tlong is not None:
            datetime = time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.localtime(int(tlong) / 1000))
        else:
            datetime = '{0}-{1}-{2} {3}'.format(d[0:4], d[4:6], d[6:], t)

        return datetime
