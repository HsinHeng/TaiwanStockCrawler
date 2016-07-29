#sudo pip install feedparser
import feedparser
import json
import time
import urllib
import logging

class GoogleNews(object):
    default_log_path = '/tmp/google_news.log'
    api_entry = 'http://news.google.com'
    required_fields = ['title', 'summary', 'link', 'published']

    def __init__(self, keyword, **kwargs):
        self.log = kwargs.get('log') if kwargs.get('log') is not None else self._get_default_logging()

        try:
            query_params = urllib.urlencode({'output': 'rss', 'q': keyword})
            r = feedparser.parse(self.api_entry + '?' + query_params)
            self.log.info('fetch data from %s', self.api_entry + '?' + query_params)
        except Exception as e:
            self.log.warning('failed to get data from %s', self.api_entry + '?' + query_params)
            raise e

        self.raw = r
        self.data = self._raw2data(self.raw)

    def _get_default_logging(self):
        logging.basicConfig(filename=self.default_log_path, level=logging.DEBUG)
        return logging

    def _raw2data(self, raw): 
        data = []
        required_fields = {field: True for field in self.required_fields}
        updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        for entry in raw.get('entries'):
            row = {'updated_at': updated_at, 'count': 0}
               
            for key, value in entry.items():   
                if required_fields.get(key) is None:
                    continue
                
                row.setdefault(key, value.strip())
            
            data.append(row)

        return data


