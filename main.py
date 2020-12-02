import bot
from globals import min_transactions, filenames, start_val, end_val, start_sd, end_sd, filepath_t
import numpy as np
from marketdata import get_data, most_traded
import csv


print("Fuchs Trading Hub ©\nPlease add as many stocks as you would like. When you're done, type in: END-LIST\n*************************************")
print("Here are the most active stocks of the day: " + str(most_traded()))
end = False

while not end:
    symbol = input('Stock Symbol: ')

    if symbol.upper() == 'END-LIST':
        if len(filenames) > 0:
            end = True
            break
        else:
            print('Current list requires more symbols')
            continue

    with open(filepath_t, "r") as file:
        csvreader = csv.reader(file, delimiter=",")
        present = False
        for line in csvreader:
            if symbol.upper() == line[0]:
                present = True
                break

    if present:
        filenames.append(symbol)
        print('{} added to list'.format(symbol.upper()))
    else:
        print('Invalid symbol')

def find_lines(data):
    return len(data)

def deviation_gatherer(sd_data):
    return bot.gather_sd(sd_data)


best_result = [0, '']
most_transactions = [0, '']
best_accuracy = [0, '']
best_total_change = [0, '']

# Going over all files to store their data in a dictionary
market_data = {}

for l in filenames:
    val_data = get_data(l, start_val, end_val)
    sd_data = get_data(l, start_sd, end_sd)
    market_data[l] = {'val_data' : val_data, 'sd_data' : sd_data}

# Going over all files to store their SD in a dictionary
dict_deviations = {}

for y in filenames:
    sd_data = get_data(y, start_sd, end_sd)
    dict_deviations[y] = deviation_gatherer(market_data[y]['sd_data'])

# Min standard deviations
for j in np.arange(0.5, 5.5 , 0.5):
    # Max standard deviations
    for n in np.arange(j + 0.5, j + 5.5, 0.5):
        # Days I hold on to the stock
        for x in range(1, 5):
            # Create a system that records the results
            sum_avg_return = 0
            sum_total_change = 0
            sum_accuracy = 0
            sum_transactions = 0

            for i in filenames:
                # Creating instance of the class 'trader'
                # def __init__(self, name, holding_days, sd, min_deviations, max_deviations):
                bot1 = bot.trader('bot1', x, dict_deviations[i], j, n)

                # def validate(self, sd, holding_on, val_data, lines, max_deviations, min_deviations, start, end, symbol):
                results = bot1.validate(bot1.sd, bot1.holding_days, market_data[i]['val_data'], find_lines(market_data[i]['val_data']), bot1.max_deviations,
                                    bot1.min_deviations, start_val, end_val, i)

                sum_avg_return += float(results['Average Return'])
                sum_total_change += float(results['Total Change'])
                sum_accuracy += float(results['Accuracy'])
                sum_transactions += float(results['Transactions'])

            sum_avg_return = sum_avg_return / len(filenames)
            sum_total_change = sum_total_change / len(filenames)
            sum_accuracy = sum_accuracy / len(filenames)
            sum_transactions = sum_transactions / len(filenames)

           # Best return per transaction
            if sum_avg_return > float(best_result[0]) and sum_transactions > min_transactions:
                best_result[0] = '{}'.format(sum_avg_return)
                best_result[1] = 'Best Total Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(results['Total Change'], results['Accuracy'], results['Holding Days'], results['Max Deviations'], results['Min Deviations'], results['Transactions'])

            # Best total change
            if float(results['Total Change']) > float(best_total_change[0]) and sum_transactions > min_transactions:
                best_total_change[0] = '{}'.format(sum_total_change)
                best_total_change[1] = 'Best Total Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(results['Total Change'], results['Accuracy'], results['Holding Days'], results['Max Deviations'], results['Min Deviations'], results['Transactions'])

            # Best accuracy
            if float(results['Accuracy']) > float(best_accuracy[0]) and sum_transactions > min_transactions:
                best_accuracy[0] = '{}'.format(sum_accuracy)
                best_accuracy[1] = 'Best Total Return: {:.5%} ----- Accuracy: {} ----- Holding Days: {} ----- Max Deviations: {} ---- Min Deviations: {} ----- Transactions: {}'.format(results['Total Change'], results['Accuracy'], results['Holding Days'], results['Max Deviations'], results['Min Deviations'], results['Transactions'])


# print the best results to determine which is the better combination

print(dict_deviations)
print('Best Result: {:.4%} ----- {}'.format(float(best_result[0]), best_result[1]))
print('Best Total Change: {:.4%} ----- {}'.format(float(best_total_change[0]), best_total_change[1]))
print('Accuracy: {:.4%} ----- {}'.format(float(best_accuracy[0]), best_accuracy[1]))

'''
print('')
print('*' * 30, end='\n\n')

# Testing a strategy out with multiple files
print('Testing a strategy out with multiple files')

# Creating variables to calculate the average accuracy, average return, # transactions, total change
sum_accuracy = 0
sum_average_return = 0
sum_transactions = 0
sum_total_change = 0

# Looping over all files
for i in filenames:
    sd_data = get_data(i, start_sd, end_sd)
    val_data = get_data(i, start_val, end_val)
    print(sd_data)
    # Storing the Standard Deviation of the file
    dict_deviations = deviation_gatherer(i, sd_data)

    # Creating instance of the class 'trader'
    # def __init__(self, name, holding_days, sd, min_deviations, max_deviations):
    bot_test = bot.trader('bot_test', 4, dict_deviations[i], 1, 3)

    # def validate(self, sd, holding_on, filename, lines, max_deviations, min_deviations, start, end, symbol):
    test_results = bot_test.validate(bot_test.sd, bot_test.holding_days, val_data, find_lines(val_data), bot_test.max_deviations, bot_test.min_deviations, start_val, end_val, symbol)

    sum_accuracy += test_results['Accuracy']
    sum_average_return += test_results['Average Return']
    sum_transactions += test_results['Transactions']
    sum_total_change += test_results['Total Change']


test_accuracy = sum_accuracy / len(filenames)
test_average_return = sum_average_return / len(filenames)
test_transactions = sum_transactions / len(filenames)
test_total_change = sum_total_change / len(filenames)

print('ACCURACY: {:.5%}\nAVERAGE RETURN: {:.5%}\nTRANSACTIONS: {}\nTOTAL CHANGE: {:.5%}'.format(test_accuracy, test_average_return, test_transactions, test_total_change))
'''