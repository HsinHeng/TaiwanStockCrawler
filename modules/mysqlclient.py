from sqlalchemy import create_engine
from sqlalchemy.sql import select
from tables import *

from modules.logger import Logger

logger, _ = Logger.get_instance()


class MySQLClient(object):
    def __init__(self, user, password, host, dbname):
        conn_str = 'mysql://{0}:{1}@{2}/{3}?charset=utf8'.format(
            user, password, host, dbname)
        self.engine = create_engine(conn_str)

    def create_tables(self):
        metadata.create_all(self.engine)

    def commit(self, stocks):
        conn = self.engine.connect()

        for number, stock in stocks.items():
            if not stock.get('record_time'):
                continue

            stmt = select([latest_stock_info]).where(latest_stock_info.c.number
                                                     == number)

            if conn.execute(stmt).fetchone():
                stmt = latest_stock_info.update()\
             .where(latest_stock_info.c.number == number)\
             .values(latest_price=stock.get('latest_price'),\
          highest_price=stock.get('highest_price'),\
          lowest_price=stock.get('lowest_price'),\
          opening_price=stock.get('opening_price'),\
          limit_up=stock.get('limit_up'),\
          limit_down=stock.get('limit_down'),\
          yesterday_price=stock.get('yesterday_price'),\
          temporal_volume=stock.get('temporal_volume'),\
          volume=stock.get('volume'),\
          top5_sold_prices=stock.get('top5_sold_prices'),\
          top5_sold_count=stock.get('top5_sold_count'),\
          top5_buy_prices=stock.get('top5_buy_prices'),\
          top5_buy_count=stock.get('top5_buy_count'),\
          record_time=stock.get('record_time'),\
          updated_at=stock.get('updated_at'))
                try:
                    conn.execute(stmt)
                except Exception as e:
                    logger.error('Failed to update stock info: %s, %s', e,
                                 stock)

            else:
                try:
                    conn.execute(latest_stock_info.insert(), [stock])
                except Exception as e:
                    logger.error('Failed to insert stock info: %s, %s', e,
                                 stock)

        conn.close()
