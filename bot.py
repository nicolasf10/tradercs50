import numpy as np
from marketdata import get_data

class trader():
    def __init__(self, name, holding_days, sd, min_deviations, max_deviations):
        # Name of the bot
        self.name = name
        # How many days that it will hang on to
        self.holding_days = holding_days
        # How much will the stock have to go down so the buy function is triggered
        self.sd = sd
        # How many deviations will meet the criteria to allow transaction
        self.min_deviations = min_deviations
        # Max. amount of deviations that will authorize the transaction
        self.max_deviations = max_deviations
        # How much the trader has
        total_profit = 0
        self.total_profit = total_profit
        # How much the trader has
        percentage_profit = 0
        self.percentage_profit = percentage_profit

    def validate(self, sd, holding_on, val_data, lines, max_deviations, min_deviations, start, end, symbol):
        '''
        CRITERIA AND MAIN INFO:
        :param holding_on:  This will be for how long we keep each stock
        :param filename: This will be for which file we're working with
        :param lines: This holds how many lines the current file has
        :param max_deviation_criteria: This will be the max standard deviation criteria
        :return: Did it make any transactions, how many, average return, list with
        all transactions, total increase, accuracy
        '''

        # List storing all 'Open' values from the data csv file
        information = val_data

        # Go over all days and check if they are suitable for a transaction (don't go over index)

        # This variable will store the index of the days suitable for a transaction
        days = []

        purchases = []

        accuracy = 0

        percent_sum = 0

        for i in range(len(information)):
            if i > 1 and i <= lines - holding_on + 1:
                previous_percentage = float(information[i - 1]) / float(information[i - 2]) - 1
                if previous_percentage < (sd * -1 * min_deviations) and previous_percentage > (
                        sd * -1 * max_deviations):
                    days.append(i)

        # Iterate over information again, and if that element is in the suitable days list make purchase
        # Calculate individual percentage profit and append to transactions
        for j in range(len(information)):
            if j in days:
                try:
                    percent = float(information[j + holding_on]) / float(information[j]) - 1
                    purchases.append(percent)
                    percent_sum += np.log(percent + 1)

                    # To calculate the accuracy
                    if percent >= -0: accuracy += 1

                except:
                    pass

        # Calculate the average return, total return, yearly return if using this strategy (datetime module?)
        total_change = np.exp(percent_sum) - 1

        try:
            avg_return = np.exp(percent_sum / len(purchases)) - 1
            accuracy = accuracy / len(purchases)
        except:
            avg_return = 0
            accuracy = 0

        # This variable will store how many transactions were made
        transactions = len(days)

        results = {
            'Total Change': total_change,
            'Average Return': avg_return,
            'Accuracy': accuracy,
            'Days': days,
            'Purchases': purchases,
            'Holding Days': holding_on,
            'Min Deviations': min_deviations,
            'Max Deviations': max_deviations,
            'Transactions': transactions,
        }

        return results

# This Function returns the average daily percentage change
def gather_sd(data):
    # TODO use yfinance instead

    # This variable will store the total change, meaning how much has changed from day 1 to the last
    total_change = 0
    first = True

    # This variable will store a list of all percentages to be used to calculate standard deviation
    values = []

    # CALCULATING THE AVERAGE AND TOTAL CHANGE
    for i in data:
        # This statement will only run if line is still the first element. This is because we can't use
        # the first day to calculate change. It will 'continue' this iteration of the for loop
        if first:
            previous_percentage = float(i)
            first = False
            continue

        # This variable will calculate the ln of the change. Formula: ln(price[day] / price[previous_day])
        percentage = np.log(float(i) / previous_percentage)
        values.append(percentage)

        total_change += percentage
        # This will set the current day percentage as the previous day. Needed to calculate the next day's change
        previous_percentage = float(i)

    # CALCULATING STANDARD DEVIATION
    sd = np.exp(np.std(values)) - 1
    return (sd)