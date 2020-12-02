import yfinance as yf
import requests
from bs4 import BeautifulSoup

def get_data(symbol, start, end):
    prices = []

    data = yf.Ticker("{}".format(symbol))

    # get historical market data
    hist = data.history(start=start, end=end)

    for i in hist['Open']:
        prices.append(i)

    return prices

def stock_valid(symbol):
    prices = []

    data = yf.Ticker("{}".format(symbol))

    # get historical market data
    hist = data.history(period='1y')

    for i in hist['Open']:
        prices.append(i)

    if len(prices) > 0: return True

    return False

def most_traded():
    # This function will use BeautifulSoup to web scrape the Yahoo! Finance page and find the most active stocks of the day
    # Using request to retrieve webpage / more info: https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
    URL = "https://finance.yahoo.com/most-active"
    r = requests.get(URL)

    # This will gather the raw html content from the page
    soup = BeautifulSoup(r.content, 'html5lib')

    # This will retrieve the table that contains the stock symbols
    table = soup.find('tbody', attrs={'data-reactid': '72'})

    # Store the list of the symbols
    active_stocks = []

    # This will loop over all elements in the table and find all <a> tags since their text value contain the stock symbols
    for tag in table:
        tdTags = tag.find_all("a", {"class": "Fw(600) C($linkColor)"})
        for tag in tdTags:
            active_stocks.append(tag.text)

    return active_stocks[:5]