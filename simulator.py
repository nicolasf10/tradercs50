import bot
from globals import min_transactions
from marketdata import get_data

def deviation_gatherer(sd_data):
    return bot.gather_sd(sd_data)

def find_lines(data):
    return len(data)

class simulate():
    def __init__(self, symbol, period, holding_days, cash_invested):
        # Name of the bot
        self.test_filenames = symbol
        # How long this simulation will take
        self.period = period
        # How many days that stock will be held on to
        self.holding_days = holding_days
        # How much money will be invested in each transaction
        self.cash_invested = cash_invested

        if period == 10:
            self.start_sd = '2000-01-01'
            self.end_sd = '2010-01-01'

            self.start_val = '2010-01-02'
            self.end_val = '2020-01-02'
        else:
            self.start_sd = '2010-01-01'
            self.end_sd = '2015-01-01'

            self.start_val = '2015-01-02'
            self.end_val = '2020-01-02'

    def run_simulation(self, symbol, start_sd, end_sd, start_val, end_val, min_sd, max_sd):
        # Going over all data to store their data in a dictionary
        market_data = {}

        val_data = get_data(symbol, start_val, end_val)
        sd_data = get_data(symbol, start_sd, end_sd)
        market_data[symbol] = {'val_data': val_data, 'sd_data': sd_data}

        # Going over all files to store their SD in a dictionary
        dict_deviations = {}

        dict_deviations[symbol] = deviation_gatherer(market_data[symbol]['sd_data'])

        j = min_sd
        n = max_sd
        x = self.holding_days
        purchases = []

        # Creating instance of the class 'trader'
        # def __init__(self, name, holding_days, sd, min_deviations, max_deviations):
        bot1 = bot.trader('bot1', x, dict_deviations[symbol], j, n)

        print(end_val)
        # def validate(self, sd, holding_on, val_data, lines, max_deviations, min_deviations, start, end, symbol):
        results = bot1.validate(bot1.sd, int(bot1.holding_days), market_data[symbol]['val_data'],
                                find_lines(market_data[symbol]['val_data']), float(bot1.max_deviations),
                                float(bot1.min_deviations), start_val, end_val, symbol)

        print(results)

        # Storing different results in variables
        avg_return = float(results['Average Return'])
        total_change = float(results['Total Change'])
        accuracy = float(results['Accuracy'])
        transactions = float(results['Transactions'])

        # Appending to purchases all the purchases made
        for i in results['Purchases']:
            purchases.append(i)

        money_made = float(self.cash_invested) * float(avg_return) * float(transactions)

        return (money_made, avg_return, total_change, accuracy, transactions, purchases)