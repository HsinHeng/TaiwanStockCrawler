import requests

from modules.twse_client import TwseClient

class TseStock(TwseClient):
    def __init__(self, numbers):
        super(TseStock, self).__init__(numbers)

    def num2urlqs(self, numbers):
        return ['tse_{}.tw'.format(number) for number in numbers]
