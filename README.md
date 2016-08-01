# Taiwan Stock Crawler

This application is used to fetch the TSE(上市), OTC(上櫃) and TAIEX, TPEX(上市,上櫃指數), I will keep implement the new features and performance. Let's Start.

# Feature
1. High performance. (implemented by multi-threading and Queue)
2. Enable to fetch TSE, OTC, TAIEX and TPEX data.
3. Enable to fetch history data.


# module/stock.py
## Simple interface to fectch all TSE, OTC, TAIEX and TPEX
    stock = Stock()

## Fectch specfic numbers of stock
    stock = Stock(['0050', '1258', 'taiex', 'tpex'])

## Fectch stock history from date
    stock = Stock(['0050'], from_date='2016-08-02')
    # Fetch all stocks
    stock = Stock(None, from_date='2016-08-02')


## Simple interface to store data
    stock = Stock(['0050'])
    
    # print a list of stock numbers you want 
    print stock.numbers
    
    # print a list of raw data
    print stock.raw
    
    # print a list of readable data
    print stock.data

# Google News Crawler

This application is used to fetch the RSS data of google news api, I will keep implement the new feature and performance in the future. Let's Start.

# module/google_news.py
## Simple interface to fectch data from google news api
    news = GoogleNews('台股')
  
## Simple interface to store data
    news = GoogleNews('台股')
    
    # print a list of raw data
    print news.raw
    
    # print a list of readable data
    print news.data
