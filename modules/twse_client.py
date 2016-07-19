import requests
import json
import time
from datetime import date, timedelta

from modules.logger import Logger

logger = Logger.get_instance()

class TwseClient(object):
    TWSE_API_URL = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch='
    COUNT = 100
    TIMEOUT = 10

    def __init__(self, numbers, date_from=None, dbclient=None):
        if type(numbers) is int:
            numbers = [numbers]

        if date_from is not None:
            # date_from: date(2016, 4, 1)
            dd = date.today() - timedelta(1) - date_from

        self.raw = []
        self.data = []
        self.numbers = numbers
        numbers = self.num2urlqs(numbers)
        length = len(numbers)
        idx = 0

        while idx < length:
            query_base = '|'.join(numbers[idx:idx + self.COUNT])
            idx = idx + self.COUNT

            try:
                if not date_from:
                    raw = self._get(query_base)
                    self.raw.extend(raw)
                else:
                    raws = []

                    for i in range(dd.days + 1):
                        d = (date_from + timedelta(days=i)).strftime('%Y%m%d')
                        query = query_base + '&d=' + d
                        raw = self._get(query)
                        raws.extend(raw)

                    data = self.raw2data(raws)
                    dbclient.commit_history(data)
            except Exception as e:
                print e
                continue

        self.data = self.raw2data(self.raw)
    
    def num2urlqs(self, numbers):
        pass

    def _get(self, query_string):
        client = requests.session()
        url = self.TWSE_API_URL + query_string

        try:
            logger.debug('fetch data from %s', url)
            client.get(self.TWSE_API_URL, timeout=self.TIMEOUT)
            res = client.get(url, timeout=self.TIMEOUT)
        except Exception as e:
            logger.warning('(X) Timeout %s', url)
            raise e

        if res.status_code != 200:
            logger.warning('(X) Status code %s from %s', res.status_code, url)
            raise
        
        try:
            raw = json.loads(res.content).get('msgArray')
        except Exception as e:
            logger.warning('(X) Retrun Data is not JSON', url)
            raise e

        if raw is None:
            logger.warning('(X) Retrieve %s stock information from %s', len(raw), url)
            raise

        logger.info('Retrieve %s stock information', len(raw))
        return raw

    def raw2data(self, raw):
        data = []
        updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        for row in raw:
            number = row.get('c')

            if not number:
                continue

            data.append({
                'number': number,
                'name': row.get('n'),
                'latest_price': row.get('z', -1),
                'highest_price': row.get('h', -1),
                'lowest_price': row.get('l', -1),
                'opening_price': row.get('o', -1),
                'limit_up': row.get('u', -1),
                'limit_down': row.get('w', -1),
                'yesterday_price': row.get('y', -1),
                'temporal_volume': self.to_number(row.get('tv', -1)),
                'volume': row.get('v', -1),
                'top5_sold_prices': self.to_json(row.get('a', '')),
                'top5_sold_count': self.to_json(row.get('f', '')),
                'top5_buy_prices': self.to_json(row.get('b', '')),
                'top5_buy_count': self.to_json(row.get('g', '')),
                'record_time': self.to_datetime(row.get('tlong'), row.get('d'), row.get('t')),
                'updated_at': updated_at,
            })

        return data

    def to_number(self, number):
        return -1 if number == '-' else number

    def to_json(self, string):
        return json.dumps(string.split('_')[:-1])

    def to_datetime(self, tlong, d, t):
        datetime = None

        if tlong is not None:
            datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(tlong) / 1000))
        else:
            datetime = '{0}-{1}-{2} {3}'.format(d[0:4], d[4:6], d[6:], t)

        return datetime
