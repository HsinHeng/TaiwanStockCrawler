import requests
import json
import time

from modules.logger import Logger

logger, _ = Logger.get_instance()


class Crawler(object):
    def __init__(self, url, stocks, count=100, timeout=10):
        self.url = url
        self.stocks = stocks
        self.client = requests.session()
        self.count = count
        self.timeout = timeout

    def run(self):
        idx = 0
        length = len(self.stocks)
        msgArrays = list()

        while idx < length:
            url = self.url + '|'.join(self.stocks[idx:idx + self.count])
            idx += self.count

            try:
                self.client.get(self.url, timeout=self.timeout)
                res = self.client.get(url, timeout=self.timeout)
            except Exception as e:
                logger.warning('(X) Timeout %s', url)
            else:
                if res.status_code == 200:
                    msgArray = json.loads(res.content).get('msgArray')

                    if msgArray:
                        logger.debug('(V) Retrieve %s/%s from %s',
                                     len(msgArray), self.count, url)
                        msgArrays.extend(msgArray)
                    else:
                        logger.warning('(X) Retrieve %s/%s from %s',
                                       len(msgArray), self.count, url)
                else:
                    logger.warning('(X) Status code %s from %s',
                                   res.status_code, url)

        logger.info('Retrieve stocks %s/%s', len(msgArrays), length)
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
