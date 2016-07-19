import requests

from modules.twse_client import TwseClient

class TaiexTpexStock(TwseClient):
    def __init__(self, numbers=None, date_from=None, dbclient=None):
        super(TaiexTpexStock, self).__init__(numbers, date_from, dbclient)

    def num2urlqs(self, numbers=None):
        return ['tse_t00.tw', 'otc_o00.tw', 'tse_FRMSA.tw']
