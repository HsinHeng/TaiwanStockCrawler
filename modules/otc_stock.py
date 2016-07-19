import requests

from modules.twse_client import TwseClient

class OtcStock(TwseClient):
    def __init__(self, numbers, date_from=None, dbclient=None):
        super(OtcStock, self).__init__(numbers, date_from, dbclient)

    def num2urlqs(self, numbers):
        return ['otc_{}.tw'.format(number) for number in numbers]
