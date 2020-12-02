from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, make_response, send_file, Response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from helpers import apology, login_required

from backtesting import backtest, bar_graph


purchases = []

# Configure application
app = Flask(__name__)

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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Requesting the form results with the name 'period'
        period = request.form.get('period')

        # Requesting the form results with the name 'symbols'
        files = request.form.get('symbols')

        # Creating an instance of the class 'backtest'
        #  def __init__(self, test_filenames, period):
        test = backtest(files, period)

        # Running the function 'run_test' from the class 'backtest'
        # def run_test(self, test_filenames, start_sd, end_sd, start_val, end_val):
        results = test.run_test(test.test_filenames, test.start_sd, test.end_sd, test.start_val, test.end_val)

        best_average_increase = results[0]
        best_average_increase_value = "{:.5%}".format(float(best_average_increase[0]))

        best_accuracy = results[1]
        best_accuracy_value = "{}".format(float(best_accuracy[0]))

        best_accuracy_total_change = results[2][0]
        best_accuracy_total_change_value = "{}".format(best_accuracy_total_change)

        purchases = best_accuracy[2]

        return render_template("backtestresults.html", results=results, period=period, best_average_increase_value=best_average_increase_value, best_accuracy_value=best_accuracy_value, best_accuracy_total_change_value=best_accuracy_total_change_value)
    else:
        # Return the home page
        return render_template("backtesting.html")

@app.route('/plot.png')
def plot_png():
    global purchases
    purchases = [2, 3, 4]
    fig = bar_graph(purchases)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')