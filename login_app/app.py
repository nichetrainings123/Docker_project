from flask import Flask, render_template, request, redirect
import psycopg2
import os
import time

app = Flask(__name__)

# -------------------------------
# PostgreSQL Connection for Docker
# -------------------------------

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "companydb")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")
DB_PORT = os.getenv("DB_PORT", "5432")

conn = None

# Retry until PostgreSQL container is ready
while conn is None:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("✅ Connected to PostgreSQL")
    except Exception as e:
        print("⏳ Waiting for PostgreSQL...", e)
        time.sleep(5)

# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    return redirect("/register")


# -------------------------------
# Registration Page
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        email = request.form["email"]
        password = request.form["password"]
        mobile = request.form["mobile"]
        address = request.form["address"]

        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO emp
                (emp_name, age, gender, email, password, mobile, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, age, gender, email, password, mobile, address))

            conn.commit()
            cur.close()

            return redirect("/login")

        except Exception as e:
            conn.rollback()
            return f"Registration Error: {e}"

    return render_template("register.html")


# -------------------------------
# Login Page
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT * FROM emp
                WHERE email = %s AND password = %s
            """, (email, password))

            user = cur.fetchone()
            cur.close()

            if user:
                return render_template("success.html", name=user[1])
            else:
                return "❌ Invalid Email or Password"

        except Exception as e:
            return f"Login Error: {e}"

    return render_template("login.html")


# -------------------------------
# Run Flask App
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)