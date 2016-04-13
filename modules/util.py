import time
import json

class Util(object):

    def convert(self, msgArrays):
        stocks = list()
        updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        for row in msgArrays:
            number = row.get('c')

            if not number:
                continue

            stocks.append({
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
                'record_time': self.to_datetime(
                    row.get('tlong'), row.get('d'), row.get('t')),
                'updated_at': updated_at,
            })

        return stocks

    def to_number(self, number):
        return -1 if number == '-' else number

    def to_json(self, string):
        return json.dumps(string.split('_')[:-1])

    def to_datetime(self, tlong, d, t):
        datetime = None

        if tlong is not None:
            datetime = time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.localtime(int(tlong) / 1000))
        else:
            datetime = '{0}-{1}-{2} {3}'.format(d[0:4], d[4:6], d[6:], t)

        return datetime
