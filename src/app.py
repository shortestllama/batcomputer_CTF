# app.py
from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

DB_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DB_URL)

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # INTENTIONAL SQLi VULNERABILITY
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["user"] = user[1]
            # If in iframe, render directly
            if "iframe" in request.args:
                return render_template("home.html", user=session["user"], flag="gotham{C0mput3r_4n41y5i5}")
            else:
                return redirect("/home")
        else:
            error = "Invalid credentials."

    return render_template("login.html", error=error)

@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("home.html", user=session["user"], flag="gotham{C0mput3r_4n41y5i5}")

if __name__ == '__main__':
    app.run(debug=True)
