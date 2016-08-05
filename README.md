# Taiwan Stock Crawler

This application is used to fetch the TSE(上市), OTC(上櫃) and TAIEX, TPEX(上市,上櫃指數), I will keep implement the new features and performance. Let's Start.

# Feature
1. High performance, fetch 1556 data during 1 sec. (implemented by multi-thread and queue)
2. Enable to fetch TSE, OTC, TAIEX and TPEX data.
3. Enable to fetch history data.

## Simple interface to fectch TSE, OTC, TAIEX and TPEX data
    # module/stock.py
    # fetch all data
    stock = Stock()

    # fetch specfic data
    stock = Stock(['0050', '1258', 'taiex', 'tpex'])
    
    # fetch history data between dates
    stock = Stock(['0050'], from_date='2016-08-02')
    stock = Stock(['0050'], from_date='2016-08-02', to_date='2016-08-20')
    stock = Stock(None, from_date='2016-08-02')

## Simple interfaces
    # print supported stock list
    print Stock.list('tse') (上市) 
    print Stock.list('otc') (上櫃)
    print Stock.list('index') (大權指數)
    
    # print a list of fectching raw data
    stock = Stock(['0050'])
    print stock.raw
    
    [{
      "nu": "http://www.yuantaetfs.com/#/RtNav/Index",
      "ts": "0",
      "fv": "0",
      "tk0": "0050.tw_tse_20160804_B_9999220779",
      "tk1": "0050.tw_tse_20160804_B_9999199393",
      "oa": "68.90",
      "ob": "68.85",
      "tlong": "1470292200000",
      "f": "398_826_606_421_404_",
      "ot": "14:30:00",
      "ex": "tse",
      "g": "365_404_78_310_436_",
      "ov": "5699",
      "d": "20160804",
      "it": "02",
      "b": "68.90_68.85_68.80_68.75_68.70_",
      "c": "0050",
      "mt": "000000",
      "a": "68.95_69.00_69.05_69.10_69.15_",
      "n": "元大台灣50",
      "o": "68.85",
      "l": "68.35",
      "oz": "68.90",
      "h": "68.95",
      "ip": "0",
      "w": "61.90",
      "v": "10669",
      "u": "75.60",
      "t": "13:30:00",
      "s": "62",
      "pz": "68.90",
      "tv": "62",
      "p": "0",
      "nf": "元大寶來台灣卓越50證券投資信託基金",
      "ch": "0050.tw",
      "z": "68.90",
      "y": "68.75",
      "ps": "62"
    }]
    
    # print a list of fectching readable data
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
