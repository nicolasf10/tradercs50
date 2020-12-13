import bot
from globals import min_transactions
import numpy as np
from marketdata import get_data
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import tempfile
from PIL import Image
from io import BytesIO
from flask import Flask, send_file
import numpy as np
from skimage.io import imsave

def find_lines(data):
    return len(data)


def deviation_gatherer(sd_data):
    return bot.gather_sd(sd_data)


# Class back_test

class backtest():
    def __init__(self, test_filenames, period):
        # Name of the bot
        self.test_filenames = test_filenames
        # How many days that it will hang on to
        self.period = period

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

    def run_test(self, filename, start_sd, end_sd, start_val, end_val):
        best_average_increase = [0, '', []]
        best_accuracy = [0, '', []]
        best_total_change = [0, '', []]

        # Going over all files to store their data in a dictionary
        market_data = {}

        val_data = get_data(filename, start_val, end_val)
        sd_data = get_data(filename, start_sd, end_sd)
        market_data[filename] = {'val_data': val_data, 'sd_data': sd_data}

        # Going over all files to store their SD in a dictionary
        dict_deviations = {}

        sd_data = get_data(filename, start_sd, end_sd)
        dict_deviations[filename] = deviation_gatherer(market_data[filename]['sd_data'])

        # Min standard deviations
        for j in np.arange(0.5, 5.5, 0.5):
            # Max standard deviations
            for n in np.arange(j + 0.5, j + 5.5, 0.5):
                # Days I hold on to the stock
                for x in range(1, 5):
                    # Create a system that records the results
                    sum_avg_return = 0
                    sum_total_change = 0
                    sum_accuracy = 0
                    sum_transactions = 0

                    # Creating instance of the class 'trader'
                    # def __init__(self, name, holding_days, sd, min_deviations, max_deviations):
                    bot1 = bot.trader('bot1', x, dict_deviations[filename], j, n)

                    # def validate(self, sd, holding_on, val_data, lines, max_deviations, min_deviations, start, end, symbol):
                    results = bot1.validate(bot1.sd, bot1.holding_days, market_data[filename]['val_data'],
                                                find_lines(market_data[filename]['val_data']), bot1.max_deviations,
                                                bot1.min_deviations, start_val, end_val, filename)

                    sum_avg_return += float(results['Average Return'])
                    sum_total_change += float(results['Total Change'])
                    sum_accuracy += float(results['Accuracy'])
                    sum_transactions += float(results['Transactions'])

                    # Best return per transaction
                    if sum_avg_return > float(best_average_increase[0]) and sum_transactions > min_transactions:
                        best_average_increase[0] = '{}'.format(sum_avg_return)
                        best_average_increase[
                            1] = 'Best Total Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(
                            results['Total Change'], results['Accuracy'], results['Holding Days'],
                            results['Max Deviations'], results['Min Deviations'], results['Transactions'])
                        best_average_increase[2] = results['Purchases']

                    # Best total change
                    if float(results['Total Change']) > float(
                            best_total_change[0]) and sum_transactions > min_transactions:
                        best_total_change[0] = '{}'.format(sum_total_change)
                        best_total_change[
                            1] = 'Best Total Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(
                            results['Total Change'], results['Accuracy'], results['Holding Days'],
                            results['Max Deviations'], results['Min Deviations'], results['Transactions'])
                        best_total_change[2] = results['Purchases']

                    # Best accuracy
                    if float(results['Accuracy']) > float(best_accuracy[0]) and sum_transactions > min_transactions:
                        best_accuracy[0] = '{}'.format(sum_accuracy)
                        best_accuracy[
                            1] = 'Best Total Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max ' \
                                 'Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(
                            results['Total Change'], results['Accuracy'], results['Holding Days'],
                            results['Max Deviations'], results['Min Deviations'], results['Transactions'])
                        best_accuracy[2] = results['Purchases']

        # stock_change will store how much the stock changed on its own from start to end of backtest
        stock_change = (val_data[-1] - val_data[0]) / val_data[0]

        return [best_average_increase, best_accuracy, best_total_change, market_data, stock_change]

def bar_graph(purchases):
    # Positive transactions
    tran_zero_to_point_five_p = 0
    tran_point_five_to_one_p = 0
    tran_more_one_p = 0
    # Neutral Transactions
    tran_neutral = 0
    # Negative Transactions
    tran_zero_to_point_five_n = 0
    tran_point_five_to_one_n = 0
    tran_less_one_n = 0

    for percent in purchases:
        # Adding a count to its correspondent variable to graph bar chart
        # Positive trades
        if percent > 0 and percent < 0.005:
            tran_zero_to_point_five_p += 1
        elif percent > 0.005 and percent < 0.01:
            tran_point_five_to_one_p += 1
        elif percent > 0.01:
            tran_more_one_p += 1
        # Neutral trade
        elif percent == 0:
            tran_neutral += 1
        # Negative trades
        elif percent < 0 and percent > -0.005:
            tran_zero_to_point_five_n += 1
        elif percent < -0.005 and percent > -0.01:
            tran_point_five_to_one_n += 1
        elif percent < -0.01:
            tran_less_one_n += 1

    # Plotting the bar chart
    """
    # Positive transactions
    tran_zero_to_point_five_p = 0
    tran_point_five_to_one_p = 0
    tran_more_one_p = 0
    # Neutral Transactions
    tran_neutral = 0
    # Negative Transactions
    tran_zero_to_point_five_n = 0
    tran_point_five_to_one_n = 0
    tran_less_one_n = 0
    """
    bar_x = ["|<-1|", "|-0.5 : -1|", "|-0.0 : -0.5|", "|0|", "|0.0 : 0.5|", "|0.5 : 1|", "|>1|"]
    bar_y = [tran_less_one_n, tran_point_five_to_one_n, tran_zero_to_point_five_n, tran_neutral,
             tran_zero_to_point_five_p, tran_point_five_to_one_p, tran_more_one_p]
    
    fig = plt.figure()

    plt.style.use("ggplot")

    # Creating the title and labeling of the chart
    plt.title("Spreading of individual transactions")
    plt.xlabel("Percentage (%) of a single transaction")
    plt.ylabel("Number of transactions in group")

    plt.bar(bar_x, bar_y)
    return fig

def scatter_graph(purchases):
    # Setting up the scatter graph using matplotlib
    plt.use("ggplot")
    graph_x = []
    graph_y = []
    graph_transactions = 0

    for j in range(len(purchases)):
        # Appending the variables to x and y (matplotlib)
        graph_x.append(j)
        graph_y.append(purchases[j])

    # Plotting the matplotlib scatter plot
    plt.figure(1)
    plt.title("Scatter (All transactions)")
    plt.scatter(graph_x, graph_y, s=5)