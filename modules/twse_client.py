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
        ''' date_from is date(2016, 4, 1)
        '''

        if type(numbers) is int or type(numbers) is str:
            numbers = [numbers]

        self.raw = []
        self.data = []
        self.numbers = numbers
        numbers = self.num2urlqs(numbers)
        length = len(numbers)

        if date_from is None:
            idx = 0
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print "[Info] %s start to fetch latest data at %s" %(self.__class__.__name__, now)

            while idx < length:
                query = '|'.join(numbers[idx:idx + self.COUNT])
                idx = idx + self.COUNT

                try:
                    raw = self._get(query)
                except Exception as e:
                    print "[Warn] %s" %e
                else:
                    self.raw.extend(raw)

            self.data = self.raw2data(self.raw)
        else:
            dd = date.today() - timedelta(1) - date_from
            
            for i in range(dd.days + 1):
                day = date_from + timedelta(days=i)
                
                if day.isoweekday() == 6 or day.isoweekday() == 7:
                    continue

                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print "[Info] %s start to fetch data of %s at %s" %(self.__class__.__name__, day, now)
                idx = 0

                while idx < length:
                    d = day.strftime('%Y%m%d')
                    query = '|'.join(numbers[idx:idx + self.COUNT]) + '&d=' + d
                    idx = idx + self.COUNT

                    try:
                        raw = self._get(query)
                    except Exception as e:
                        print "[Warn] %s" %e
                        continue

                    try:
                        if dbclient is None:
                            self.raw.extend(raw)
                        else:
                            data = self.raw2data(raw)
                            dbclient.commit_history(data)
                    except Exception as e:
                        print "[Warn] %s" %e
                        continue

            if dbclient is None:
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
                'type': row.get('ex'),
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
