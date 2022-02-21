from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def connectToDB():
    connectionString = 'dbname=northwind user=postgres port=5432 host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)