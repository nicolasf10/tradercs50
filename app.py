from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, make_response, send_file, Response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


import io

import matplotlib
matplotlib.use('agg')

from helpers import apology, login_required

from backtesting import backtest, bar_graph
from simulator import simulate

# Configure application
app = Flask(__name__)
# Run in terminal: export FLASK_ENV=development

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///dqlss.db")

# Custom filter for formatting as percentage
def percentage(num):
    return "{:.3%}".format(float(num))

app.jinja_env.filters["percentage"] = percentage


@app.route("/")
@login_required
def index():
    # Return the home page
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Making sure the user actually typed in something in the fields
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        # Ensure user provided username
        if not username:
            return apology("Must provide username", 400)

        # Ensure user provided password
        elif not password:
            return apology("Must provide password", 400)

        # Confirming passwords match
        elif not password == password_confirm:
            return apology("Passwords do not match", 400)

        # Hash the password and insert the new user into database
        hashed_password = generate_password_hash(password)

        exists = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(exists) == 0:
            new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed_password)", username=username, hashed_password=hashed_password)
        else:
            return apology("Username taken", 400)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Display a flash message
        flash("Registered!")

        # Redirect user to homepage
        return redirect("/")

    # In case method is GET
    else:
        return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

@app.route("/backtest", methods=["GET", "POST"])
@login_required
def backtesting():
    global purchases
    global period
    global results
    global chart_title
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Requesting the form results with the name 'period'
        period = int(request.form.get('period'))

        # Requesting the form results with the name 'symbols'
        files = request.form.get('symbols')

        # Creating an instance of the class 'backtest'
        #  def __init__(self, test_filenames, period):
        test = backtest(files, period)

        # Running the function 'run_test' from the class 'backtest'
        # def run_test(self, test_filenames, start_sd, end_sd, start_val, end_val):
        results = test.run_test(files, test.start_sd, test.end_sd, test.start_val, test.end_val)

        purchases = results[1][2]

        chart_title = "Best Accuracy"

        return render_template("backtestresults.html", results=results, period=period, best_average_increase=results[0], best_accuracy=results[1], best_total_change=results[2], stock_change=results[4], chart_title=chart_title)
    else:
        # Return the home page
        return render_template("backtesting.html")

@app.route("/charts", methods=["POST"])
@login_required
def charts():
    global purchases
    global results
    global period
    global chart_title
    chart = request.form.get("chart")
    if chart == 'accuracy':
        purchases = results[1][2]
        chart_title = "Best Accuracy"
    elif chart == 'avg_increase':
        purchases = results[0][2]
        chart_title = "Best Average Increase"
    else:
        purchases = results[2][2]
        chart_title = "Best Total Change"

    return render_template("backtestresults.html", results=results, period=period, best_average_increase=results[0], best_accuracy=results[1], best_total_change=results[2], stock_change=results[4], chart_title=chart_title)


@app.route('/simulator', methods=["GET", "POST"])
@login_required
def simulator():
    global purchases
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Requesting the form results with the name 'period'
        period = int(request.form.get('period'))

        # Requesting the form results with the name 'symbol'
        file = request.form.get('symbol')

        # Requesting the form results with the name 'holding_days'
        holding_days = request.form.get('holding_days')

        # Requesting the form results with the name 'cash_invested'
        cash_invested = request.form.get('cash_invested')

        # Requesting the form results with the name 'min_sd'
        min_sd = request.form.get('min_sd')

        # Requesting the form results with the name 'max_sd'
        max_sd = request.form.get('max_sd')

        # Creating an instance of the class 'simulate'
        #def __init__(self, symbol, period, holding_days, cash_invested):
        simulator = simulate(file, period, holding_days, cash_invested)

        # Running the function 'run_test' from the class 'simulate'
        # def run_simulation(self, symbol, start_sd, end_sd, start_val, end_val, min_sd, max_sd):
        results = simulator.run_simulation(simulator.test_filenames, simulator.start_sd, simulator.end_sd, simulator.start_val, simulator.end_val, min_sd, max_sd)

        purchases = results[5]

        return render_template("simulatorresults.html", results=results, period=period, money_made=round(results[0], 2), avg_return="{:.5%}".format(results[1]), transactions=results[4], accuracy=results[3])
    else:
        # Return the home page
        return render_template("simulator.html")

@app.route('/plot.png')
@login_required
def plot_png():
    global purchases
    fig = bar_graph(purchases)
    return nocache(fig_response(fig))

def fig_response(fig):
    """Turn a matplotlib Figure into Flask response"""
    img_bytes = io.BytesIO()
    fig.savefig(img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png')

def nocache(response):
    """Add Cache-Control headers to disable caching a response"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response