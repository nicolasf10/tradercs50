import bot
from globals import min_transactions
import numpy as np
from marketdata import get_data
from matplotlib import pyplot as plt

import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

    def run_test(self, test_filenames, start_sd, end_sd, start_val, end_val):
        best_average_increase = [0, '', []]
        most_transactions = [0, '', []]
        best_accuracy = [0, '', []]
        best_total_change = [0, '', []]

        # Going over all files to store their data in a dictionary
        market_data = {}

        for l in test_filenames:
            val_data = get_data(l, start_val, end_val)
            sd_data = get_data(l, start_sd, end_sd)
            market_data[l] = {'val_data': val_data, 'sd_data': sd_data}

        # Going over all files to store their SD in a dictionary
        dict_deviations = {}

        for y in test_filenames:
            sd_data = get_data(y, start_sd, end_sd)
            dict_deviations[y] = deviation_gatherer(market_data[y]['sd_data'])

        # All purchases made with any strategy
        all_purchases = []

        # Min standard deviations
        for j in np.arange(0.5, 5.5, 0.5):
            # Max standard deviations
            for n in np.arange(j + 0.5, j + 5.5, 0.5):
                # Days I hold on to the stock
                for x in range(1, 5):
                    purchases = []

                    # Create a system that records the results
                    sum_avg_return = 0
                    sum_total_change = 0
                    sum_accuracy = 0
                    sum_transactions = 0

                    for i in test_filenames:
                        # Creating instance of the class 'trader'
                        # def __init__(self, name, holding_days, sd, min_deviations, max_deviations):
                        bot1 = bot.trader('bot1', x, dict_deviations[i], j, n)

                        # def validate(self, sd, holding_on, val_data, lines, max_deviations, min_deviations, start, end, symbol):
                        results = bot1.validate(bot1.sd, bot1.holding_days, market_data[i]['val_data'],
                                                find_lines(market_data[i]['val_data']), bot1.max_deviations,
                                                bot1.min_deviations, start_val, end_val, i)

                        sum_avg_return += float(results['Average Return'])
                        sum_total_change += float(results['Total Change'])
                        sum_accuracy += float(results['Accuracy'])
                        sum_transactions += float(results['Transactions'])

                        # Appending to purchases all the purchases made
                        for i in results['Purchases']:
                            purchases.append(i)

                        for i in results['Purchases']:
                            all_purchases.append(i)

                    sum_avg_return = sum_avg_return / len(test_filenames)
                    sum_total_change = sum_total_change / len(test_filenames)
                    sum_accuracy = sum_accuracy / len(test_filenames)
                    sum_transactions = sum_transactions / len(test_filenames)

                    # Best return per transaction
                    if sum_avg_return > float(best_average_increase[0]) and sum_transactions > min_transactions:
                        best_average_increase[0] = '{}'.format(sum_avg_return)
                        best_average_increase[1] = 'Best Average Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(sum_total_change, sum_accuracy, results['Holding Days'], results['Max Deviations'],results['Min Deviations'], results['Transactions'])
                        best_average_increase[2] = purchases

                    # Best total change
                    if float(results['Total Change']) > float(
                            best_total_change[0]) and sum_transactions > min_transactions:
                        best_total_change[0] = '{}'.format(sum_total_change)
                        best_total_change[
                            1] = 'Best Total Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(
                            sum_total_change, sum_accuracy, results['Holding Days'], results['Max Deviations'],
                            results['Min Deviations'], results['Transactions'])
                        best_total_change[2] = purchases

                    # Best accuracy
                    if float(results['Accuracy']) > float(best_accuracy[0]) and sum_transactions > min_transactions:
                        best_accuracy[0] = '{}'.format(sum_accuracy)
                        best_accuracy[
                            1] = 'Best Total Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(
                            sum_total_change, sum_accuracy, results['Holding Days'], results['Max Deviations'],
                            results['Min Deviations'], results['Transactions'])
                        best_accuracy[2] = purchases

        return (best_average_increase, best_accuracy, best_total_change, all_purchases)

def bar_graph(self, purchases):
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
    bar_x = ["<-1", "-0.5 : -1", "-0.0 : -0.5", "0", "0.0 : 0.5", "0.5 : 1", ">1"]
    bar_y = [tran_less_one_n, tran_point_five_to_one_n, tran_zero_to_point_five_n, tran_neutral,
             tran_zero_to_point_five_p, tran_point_five_to_one_p, tran_more_one_p]
    
    fig = plt.figure()
    plt.title("Bar (Spreading of transactions)")
    plt.plot(bar_x, bar_y)
    plt.savefig("out.png", format="'png'")
    return fig

def scatter_graph(purchases):
    # Setting up the scatter graph using matplotlib
    plt.style.use("ggplot")
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

bar_graph([1, 2], [3, 4]).savefig("image.png")