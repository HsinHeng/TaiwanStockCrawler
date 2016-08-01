# Taiwan Stock Crawler

This Application is used to fetch the TSE(上市), OTC(上櫃) and TAIEX, TPEX(上市,上櫃指數), I will keep implement the ne feature and performance in the future.
Let's Start.

# module/stock.py
## Simply Interface to fectch tse, otc, taiex and tpex
    stock = Stock()

## Fectch specfic numbers of tse, otc, taiex and tpex
    stock = Stock(['0050', '1258', 'taiex', 'tpex'])

## Fectch stock history from date
    stock = Stock(['0050'], from_date='2016-08-02')
    stock = Stock(None, from_date='2016-08-02')


## var to store retrieve data
   stock = Stock(['0050'])
   # print a list of stock numbers you want 
   print stock.numbers
   # print a list of raw data
   print stock.raw
   # print a list of readable data
   print stock.data


# Google News Crawler

This Application is used to fetch the RSS service of google news api, I will keep implement the ne feature and performance in the future.
Let's Start.

# module/google_news.py
## Simply Interface to fectch tse, otc, taiex and tpex
    google_news = GoogleNews('台股')
  
## var to store retrieve data
    news = GoogleNews('台股')
    # print a list of raw data
    print news.raw
    # print a list of readable data
    print news.data
