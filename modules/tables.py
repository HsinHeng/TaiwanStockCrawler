from sqlalchemy import Table, Column, Integer, String, Float, MetaData, ForeignKey, DateTime

metadata = MetaData()
latest_stock_info = Table('latest_stock_info', metadata,
    Column('number', String(16), primary_key=True),
    Column('name', String(64)),
    Column('latest_price', Float),
    Column('highest_price', Float),
    Column('lowest_price', Float),
    Column('opening_price', Float),
    Column('limit_up', Float),
    Column('limit_down', Float),
    Column('yesterday_price', Float),
    Column('temporal_volume', Integer),
    Column('volume', Integer),
    Column('top5_sold_prices', String(1024)),
    Column('top5_sold_count', String(1024)),
    Column('top5_buy_prices', String(1024)),
    Column('top5_buy_count', String(1024)),
    Column('record_time', DateTime),
    Column('updated_at', DateTime),
    mysql_charset='utf8',
)
