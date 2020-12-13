# DQLS Trading - CS50x Final Project

## What is DQLS Trading
DQLS (Discovering Quantitative Long Stock Strategies) Trading is a platform created to test and simulate a quantitative stock trading strategy. The main part of this project is the Flask Web Application, which allows the user to back-test and find the best combination of strategies over a period of either 5 or 10 years. However, my main focus for this project was working on the back-end of this product.

## Tools and laungagues used:
- Python
- HTML & CSS
- Flask
- Matplotlib
- yfinance
- requests
- BeautifulSoup
- csv
- numpy
- cs50
- io
- PIL
- SQLite

## How does the strategy work?
The strategy is based on the hypothesis (which was put to the test in this project)
that the market overreacts, hence, after a drop in the stock price of a certain amount, the market will readjust,
increasing the stock price again. To determine that there is a drop that indicates the time to buy a certain stock,
I used the concept of [standard deviation](https://en.wikipedia.org/wiki/Standard_deviation).

The first step of my program is taking stock data (from a date before I begin testing to ensure my back-test's validity),
which is gathered using `yfinance` and calculating the stock's daily standard deviation. My main tool is back-testing,
which, again, uses `yfinance`, and tries trading with the following algorithm (pseudo code):
```
# The max is there to ensure that the stock is not bought if a massive disaster occurs
if yesterday_price_change < (min_num_of_standard_deviations * -1) and yesterday_price_change > (max_num_of_standard_deviations * -1) {
   buy_stock()
}
sleep(x_days)
sell_stock()
```
As you can see in the program above, there are some variables that are not defined, which is also one of the purposes
of my program, to determine what is the best possible combination of the following:
* How many standard deviations does the stock need to drop?
* What is the maximum amount of standard deviations to prevent the purchase of a stock in the case of a disaster
* What is the optimal number

## How to run the project
Option 1 (with Flask):
 * In the terminal export `FLASK_APP=development`
 * Run `flask run` in the terminal
 Option 2 (command-line program):
 * Run `python main.py` in the terminal