from tqdm import tqdm
import bs4 as bs
import pickle
import requests
import pandas as pd
import quandl
import datetime
quandl.ApiConfig.api_key = "zV2SPzycFugXvKzD_yZs"



def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers


symb_list=save_sp500_tickers()

 
# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2000,1,1)
end = datetime.date.today()
data_all=[]
# Let's get Apple stock data; Apple's ticker symbol is AAPL
# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
for s in tqdm(symb_list):
	try:
		data = quandl.get("WIKI/" + s, start_date=start, end_date=end)
		data["NAME"]=s
		data_all.append(data)
	except:
		print(s)
 
rez=pd.concat(data_all)
rez.to_csv("sp500_history.csv")
