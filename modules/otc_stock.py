import requests

from modules.twse_client import TwseClient

class OtcStock(TwseClient):
    def __init__(self, numbers):
        super(OtcStock, self).__init__(numbers)

    def num2urlqs(self, numbers):
        return ['otc_{}.tw'.format(number) for number in numbers]
