from flask import Flask, render_template, request, redirect, url_for, session
from db import get_db_connection
from decimal import Decimal
import sqlite3
import os


app = Flask(__name__)
app.secret_key = "atm_secret_key"

# LOGIN

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        account = request.form["account"]
        pin = request.form["pin"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE account_no=? AND pin=?",
            (account, pin)
    )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Account or PIN"

    return render_template("login.html")


# DASHBOARD

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, balance FROM users WHERE id=%s",
        (session["user_id"],)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        name=user["name"],
        balance=user["balance"]
    )


# WITHDRAW
@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "user_id" not in session:
        return redirect(url_for("login"))

    amount = Decimal(request.form["amount"])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE id=%s",
        (session["user_id"],)
    )
    user = cursor.fetchone()

    if user["balance"] < amount:
        cursor.close()
        conn.close()
        return "Insufficient Balance"

    new_balance = user["balance"] - amount

    cursor.execute(
        "UPDATE users SET balance=%s WHERE id=%s",
        (new_balance, session["user_id"])
    )

    cursor.execute(
        "INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
        (session["user_id"], "withdraw", amount)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("dashboard"))


#  DEPOSIT

@app.route("/deposit", methods=["POST"])
def deposit():
    if "user_id" not in session:
        return redirect(url_for("login"))

    amount = Decimal(request.form["amount"])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET balance = balance + %s WHERE id=%s",
        (amount, session["user_id"])
    )

    cursor.execute(
        "INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
        (session["user_id"], "deposit", amount)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("dashboard"))


# TRANSACTIONS
@app.route("/transactions")
def transactions():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT type, amount, transaction_date FROM transactions WHERE user_id=%s ORDER BY transaction_date DESC",
        (session["user_id"],)
    )
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("transactions.html", transactions=data)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



def get_db_connection():
    conn = sqlite3.connect("atm.db")
    conn.row_factory = sqlite3.Row
    return conn