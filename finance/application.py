import os
import hashlib

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    # Establish userID.
    userID = session["user_id"]
    # Isolate all results from portfolio table for the current user.
    portfolio = db.execute("SELECT * FROM portfolio WHERE id=:userID", userID=session["user_id"])
    # Cash for current user (first row, cash column)
    cash = db.execute("SELECT cash FROM users WHERE id=:userID", userID=userID)[0]["cash"]
    # Empty list to store stock data as iterating through rows.
    stockData = []
    # Set total for combined stoc value to 0.
    totalAllStocks = 0

    # Iterate over rows from portfolio and allocate a row for each stock that has more than 0 owned.
    for row in portfolio:
       if row["numOwned"] != 0:
           stockData.append(row)

    # Iterate over rows in stock data and provide value for each column. Other values for use in html are already in list from previous loop.
    # Had to play around with usd, once in usd is a str rather than float so usd always has to be post calculations.
    for row in stockData:
        stock = lookup(row["symbol"])
        row["name"] = stock["name"]
        row["currentPrice"] = usd(stock["price"])
        row["total"] = usd(row["numOwned"] * stock["price"])
        totalAllStocks += row["numOwned"] * stock["price"]
    # Grand Total is combined stock values and cash value.
    grandTotal = totalAllStocks + cash
    # Return index.html input sources.
    return render_template("index.html", stockData=stockData, cash=usd(cash), totalAllStocks = usd(totalAllStocks), grandTotal=usd(grandTotal))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))

        # This took a while for check to confirm. First check that user input is digit.
        if not request.form.get("shares").isdigit():
            return apology("Inavalid number of shares")
        numOfShares = request.form.get("shares")

        # If request is POST firstly check if anything has been submitted.
        if not request.form.get("symbol"):
            return apology("You haven't typed a symbol")
        # if stock lookup request is None or if the numOfShares is not a number of 1 or higher return apologies.
        if stock is None:
            return apology("This doesn't seem to be a valid symbol, try again")
        # userID and user serparate in case both are required.
        userID = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id = :id", id=userID)
        #funds is a float and can be multiplied by number of shares
        funds = float(user[0]["cash"])
        purchasePrice = stock["price"] * int(numOfShares)

        date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')


        if funds < purchasePrice:
            return apology("You don't have sufficient funds to make this purchase")
        else:
            # Take price off total cash for current user.
            db.execute("UPDATE users SET cash = cash - :purchasePrice WHERE id = :userID", purchasePrice=purchasePrice, userID=userID)
            # Insert into transactions table the id, symbol, number of share bought, price per share, the time,date and the BUY order.
            db.execute("INSERT INTO transactions (id, symbol, num_shares, price_ps, date_time, buy_or_sell) VALUES (:id, :symbol, :num_shares, :price_ps, :date_time, :buy_or_sell)",
                id=userID, symbol=stock["symbol"], num_shares=numOfShares, price_ps=stock["price"], date_time=date_time, buy_or_sell="BUY")
        # stockowned allows search of portfolio table for results that have userID and the bought stock.
        stockOwned = db.execute("SELECT * FROM portfolio WHERE symbol=:symbol AND id=:userID", symbol=stock["symbol"], userID=userID)
        # If there are nor results (not stockowned) then insert into portfolio
        if not stockOwned:
            db.execute("INSERT INTO portfolio (id, symbol, numOwned, pricePerShare, totalValue) VALUES (:userID, :symbol, :numOwned, :pricePerShare, :totalValue)",
                userID=userID, symbol=stock["symbol"], numOwned=numOfShares, pricePerShare=stock["price"], totalValue=purchasePrice)
        # Other wise update the current results. Had to ensuer numOf Share was floas was sotred as a str. Using indexes of stockowned for values.
        else:
            newNumOwned = stockOwned[0]["numOwned"] + float(numOfShares)
            newTotalValue = stockOwned[0]["totalValue"] + purchasePrice
            newPPS = "%.2f"%(newTotalValue / newNumOwned)
            db.execute("UPDATE portfolio SET numOwned = :newNumOwned, totalValue = :newTotalValue, pricePerShare = :newPPS WHERE symbol=:symbol AND id=:userID",
                newNumOwned=newNumOwned, newTotalValue=newTotalValue, newPPS=newPPS, symbol=stock["symbol"], userID=userID)

        return redirect("/")

    # If a GET request, return the buy.html template.
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    userID = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE id=:userID", userID=userID)

    for row in transactions:
        stock = lookup(row["symbol"])
        row["name"] = stock["name"]
        row["total"] = usd(row["num_shares"] * row["price_ps"])

    return render_template("history.html", transactions=transactions)



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
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


# QUOTE
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # If request is POST firstly check if anyhting has been submitted.
        if not request.form.get("symbol"):
            return apology("You haven't typed a symbol")
        # Lookup will check submitted symbol against api.
        symbolquote = lookup(request.form.get("symbol"))
        # if None (no result from API) then return apology that not a valid symbol.
        if symbolquote is None:
            return apology("This doesn't seem to be a valid symbol, try again")
        # If valid symbol, return quoted.html including the relevant values.
        else:
            return render_template("quoted.html", name=symbolquote["name"], symbol=symbolquote["symbol"], price=usd(symbolquote["price"]))
    # If Get request, present user with quote.html
    else:
        return render_template("quote.html")


#REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Request username from form, if no username is provided return apology.
        username = request.form.get("username")
        if not username:
            return apology("You must provide a Username")
        # Request password from form, if no password is provided return apology.
        password = request.form.get("password")
        if not password:
            return apology("You must provide a Password")
        # Request confirmation password form form, if no confirmaiton is provided return apology.
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("You must confirm your Password.")
        # Password and confiramtion already declared, if they don't match return and apology.
        if password != confirmation:
            return apology("Your passwords must match!")

        # generate_password_hash (from Werkzeug) will hash the password from form.
        hashpassword = generate_password_hash(request.form.get("password"))

        # Check that username is not already taken.
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(rows) == 1:
            return apology("This username is taken please choose another.")

        # Add the new user into the database.
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashpassword)", username=username, hashpassword=hashpassword)

        # Keep new user logged in
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        session["user_id"] = rows[0]["id"]

        # Take back to home back
        return redirect("/")

    # If just a get request then present user with register.html
    else:
        return render_template("register.html")

# SELL
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Moved userID outside of 'if' as could not be accessed in 'else' for html.
    userID = session["user_id"]

    if request.method == "POST":

        user = db.execute("SELECT * FROM users WHERE id = :id", id=userID)
        cash = user[0]["cash"]

        stock = lookup(request.form.get("symbol"))

        numOfShares = float(request.form.get("shares"))
        if not request.form.get("symbol"):
            return apology("You haven't typed a symbol")
        if stock is None:
            return apology("This doesn't seem to be a valid symbol, try again")
        if numOfShares < 0:
            return apology("You must state how many shares you want to sell")

        salePrice = stock["price"] * numOfShares
        date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        stockOwned = db.execute("SELECT * FROM portfolio WHERE id=:userID AND symbol=:symbol", userID=userID, symbol=stock["symbol"])
        if not stockOwned:
            return apology("You don't own any of this stock")
        if stockOwned[0]["numOwned"] < numOfShares:
            return apology("You are trying to sell more shares than you own!")
        else:
            newNumOwned = float(stockOwned[0]["numOwned"]) - numOfShares
            newTotalValue = newNumOwned * stock["price"]
            db.execute("UPDATE users SET cash=cash+:salePrice WHERE id=:userID", salePrice=salePrice, userID=userID)
            db.execute("INSERT INTO transactions (id, symbol, num_shares, price_ps, date_time, buy_or_sell) VALUES (:userID, :symbol, :num_shares, :price_ps, :date_time, :buy_or_sell)",
                userID=userID, symbol=stock["symbol"], num_shares=numOfShares, price_ps=stock["price"], date_time=date_time, buy_or_sell="SELL")
            db.execute("UPDATE portfolio SET numOwned=:newNumOwned, totalValue=:newTotalValue WHERE id=:userID AND symbol=:symbol",
                newNumOwned=newNumOwned, newTotalValue=newTotalValue, userID=userID, symbol=stock["symbol"])

        return redirect("/")
    else:
        symbols = db.execute("SELECT symbol FROM portfolio WHERE id=:userID", userID=userID)
        return render_template("sell.html", symbols=symbols)


# SETTINGS
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change Password"""
    if request.method == "POST":
        userID = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id=:userID", userID=userID)

        password = request.form.get("password")
        newPassword = request.form.get("newPassword")
        confirmation = request.form.get("confirmation")

        if not check_password_hash(user[0]["hash"], password):
            flash("Your current password is incorrect", "warning")
            return redirect("/settings")
        elif not newPassword:
            flash("You haven't entered a new password", "warning")
            return redirect("/settings")
        elif not confirmation:
            flash("You haven't confirmed your new password", "warning")
        elif confirmation != newPassword:
            flash("New passwords do not match!", "warning")
            return redirect("/settings")
        else:
            db.execute("UPDATE users SET hash=:hashpassword WHERE id=:userID", hashpassword=generate_password_hash(newPassword), userID=userID)
            flash("Your password has been updated", "success")
            # Take back to home back
            return redirect("/")

    else:
        return render_template("settings.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
