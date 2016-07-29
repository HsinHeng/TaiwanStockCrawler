import csv

class ConfigReader(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not ConfigReader.__instance:
            ConfigReader.__instance = object.__new__(cls, *args, **kwargs)
            return ConfigReader.__instance

    def __init__(self, config, path):
        try:
            config.read(path)
            self.tse_stock_list_file = config.get('TW Stock', 'tse_stock_list_file')
            self.otc_stock_list_file = config.get('TW Stock', 'otc_stock_list_file')
            self.interval = int(config.get('TW Stock', 'interval'))
            self.from_date = config.get('TW Stock History', 'from_date')
            self.keywords = config.get('Google News', 'keywords').split(',')
            self.user = config.get('MySQL', 'user')
            self.password = config.get('MySQL', 'password')
            self.host = config.get('MySQL', 'host')
            self.dbname = config.get('MySQL', 'dbname')
        except Exception as e:
            raise e

        self.tse_stock_list = []
        self.otc_stock_list = []

        with open(self.tse_stock_list_file, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            reader.next()
            reader.next()

            for row in reader:

                if not row:
                    continue

                self.tse_stock_list.append(row[0].strip())
        
        with open(self.otc_stock_list_file, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            reader.next()
            reader.next()
            reader.next()

            for row in reader:
                if not row:
                    continue

                self.otc_stock_list.append(row[0].strip())
            
            del self.otc_stock_list[-1]
