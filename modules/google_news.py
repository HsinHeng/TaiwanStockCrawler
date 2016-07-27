#sudo pip install feedparser
import feedparser
import json
import time

from modules.logger import Logger

logger = Logger.get_instance()

class GoogleNews(object):
    GOOGLE_NEWS_URL = 'http://news.google.com?output=rss'
    REQUIRED_FIELDS = ['title', 'summary', 'link', 'published']

    def __init__(self, keyword):
        try:
            res = feedparser.parse(self.GOOGLE_NEWS_URL + '&q=' + keyword)
        except Exception as e:
            raise e

        updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.raw = res
        self.data = []
        required_fields = { field: True for field in self.REQUIRED_FIELDS}


        for entry in res.get('entries'):
            data = {'updated_at': updated_at, 'count': 0}
               
            for key, value in entry.items(): 
   
                if required_fields.get(key) is None:
                    continue
                
                data.setdefault(key, value.strip())
            
            self.data.append(data)

