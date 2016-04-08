import ConfigParser
import csv

CONF_FILE_PATH = 'config/stock.conf'


def getConfig():
    data = dict()
    config = ConfigParser.ConfigParser()

    try:
        config.read(CONF_FILE_PATH)
        conf = {
            'url': config.get('TW Stock', 'url'),
            'file': config.get('TW Stock', 'file'),
            'interval': int(config.get('TW Stock', 'interval')),
            'user': config.get('MySQL', 'user'),
            'password': config.get('MySQL', 'password'),
            'host': config.get('MySQL', 'host'),
            'dbname': config.get('MySQL', 'dbname'),
        }
    except Exception as e:
        return False, conf
    else:
        return True, conf


def getStockList(path):
    stocks = list()

    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        reader.next()
        reader.next()

        for row in reader:

            if not row:
                continue

            stocks.append('tse_{}.tw'.format(row[0].strip()))

    #stocks = ['otc_o00.tw']
    #stocks = ['tse_0050.tw', 'tse_0051.tw']
    return stocks
