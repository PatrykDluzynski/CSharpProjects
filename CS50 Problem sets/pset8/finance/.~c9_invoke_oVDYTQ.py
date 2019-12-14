import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #Update the stock prices
    rows = db.execute("SELECT * FROM stocks WHERE id = :id", id=session["user_id"])
    for i in range(len(rows)):
        quote = lookup(rows[i]["symbol"])
        newprice = quote["price"]
        db.execute("UPDATE stocks SET unit_price = :unit_price WHERE id = :id AND symbol = :symbol", unit_price=newprice, id=session["user_id"], symbol=rows[i]["symbol"])
        db.execute("UPDATE stocks SET total_price = :total_price WHERE id = :id AND symbol = :symbol", total_price=round(rows[i]["amount"] * newprice,2), id=session["user_id"], symbol=rows[i]["symbol"])

    #Retrieve data again after updating
    rows = db.execute("SELECT * FROM stocks WHERE id = :id", id=session["user_id"])
    userdata = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    currcash = userdata[0]["cash"]
    #Calculate total value of account
    total = currcash
    for i in range(len(rows)):
        total += rows[i]["total_price"]

    #Return the template with data
    return render_template("index.html", rows=rows, currcash=round(currcash,2), total=round(total,2), rowlength=len(rows))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("The symbol was not specified")

        elif not request.form.get("amount"):
            return apology("The amount of shares to buy was not specified")

        try:
            value = int(request.form.get("amount"))
        except:
            return apology("The amount has to be a positive integer")

        if value < 0:
            return apology("The amount has to be a positive integer")

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Stock not found, is the symbol correct?")

        price = quote["price"] * int(request.form.get("amount"))
        userdata = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        currcash = userdata[0]["cash"]

        if price > currcash:
            return apology("Your balance is too low to purchase this stock")

        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=currcash - price, id=session["user_id"])
            db.execute("INSERT INTO history(id, symbol, amount, unit_price, total_price) VALUES(:id, :symbol, :amount, :unit_price, :total_price)",
                        id=session["user_id"], symbol=quote["symbol"], amount=int(request.form.get("amount")), unit_price=quote["price"], total_price=price)

            userstocks = db.execute("SELECT * FROM stocks WHERE id = :id AND symbol = :symbol", symbol=quote["symbol"], id=session["user_id"])
            if not userstocks:
                db.execute("INSERT INTO stocks(id, symbol, amount, unit_price, total_price) VALUES(:id, :symbol, :amount, :unit_price, :total_price)",
                        id=session["user_id"], symbol=quote["symbol"], amount=int(request.form.get("amount")), unit_price=quote["price"], total_price=price)
            else:
                curramt = userstocks[0]["amount"]
                currtotprice = userstocks[0]["total_price"]
                db.execute("UPDATE stocks SET amount = :amount, total_price = :total_price WHERE id = :id",
                amount=curramt + int(request.form.get("amount")), total_price=currtotprice + price, id=session["user_id"])

            return redirect("/")




@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    elif request.method == "POST":

        if not request.form.get("symbol"):
            return apology("No symbol specified")

        else:
            quote = lookup(request.form.get("symbol"))
            if not quote:
                return apology("Quote not found, is the symbol correct?")

            else:
                return render_template("quotedisplay.html", name=quote["name"], price=usd(quote["price"]), symbol=quote["symbol"])




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":

        if not request.form.get("username"):
            return apology("Username not provided")

        elif not request.form.get("password"):
            return apology("Password not provided")

        elif not request.form.get("password2"):
            return apology("Password confirmation not provided")

        elif request.form.get("password") != request.form.get("password2"):
            return apology("Passwords did not match")

        result = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if result:
            return apology("Username taken")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
            session["user_id"] = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            return redirect("/quote")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

@app.route("/charge", methods=["GET", "POST"])
@login_required
def charge():
    """Charge account with additional cash"""
    if request.method == "GET":
        return render_template("charge.html")

    if request.method == "POST":
        if not request.form.get("amount") or float(request.form.get("amount")) < 0:
            return apology("Amount to charge not specified or is negative")

        elif not request.form.get("password"):
            return apology("No password provided")

        userdata = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

        if not check_password_hash(userdata[0]["hash"], request.form.get("password")):
            return apology("Password did not match")

        else:
            currcash = userdata[0]["cash"]
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=round(currcash + float(request.form.get("amount")),2), id=session["user_id"])

        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
