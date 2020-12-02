from marketdata import get_data

# Name of the file (if user wants to change which data to look at there is one variable that allows this)
all_files = ['data/vale3data.csv', 'data/bbdc4data.csv', 'data/ibovespadata.csv', 'data/itub4data.csv', 'data/petr4data.csv']#, 'data/b3data.csv', 'data/abev3data.csv', 'data/brfs3data.csv', 'data/ciel3data.csv', 'data/cogn3data.csv', 'data/ggb4data.csv', 'data/itsa4data.csv', 'data/lren3data.csv', 'data/mglu3data.csv', 'data/usim5data.csv', 'data/vvar3data.csv', 'data/embr3data.csv']

filename = 'main_data/msftdata.csv'
test = ['main_data/aapldata.csv', 'main_data/amgndata.csv', 'main_data/msftdata.csv', 'main_data/amzndata.csv', 'main_data/nflxdata.csv']
filenames = []

test_filenames = ['MSFT']

date_max = 2011
date_min = 2010

#symbol = 'aapl'

entire_increase = 0.0
entire_transactions = 0

min_transactions = 50

start_sd = '2000-01-01'
end_sd = '2010-12-31'

start_val = '2011-01-01'
end_val = '2020-01-01'

# Tickers
filepath_t = 'tickers.csv'