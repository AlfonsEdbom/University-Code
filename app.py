from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

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

# display categories table etc
@app.route("/categories", methods=["GET", "POST"])
def categories():
    conn = connectToDB()
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        dict_cur.execute('SELECT * FROM categories')
    except:
        print('could not execute query')
    results = dict_cur.fetchall()
    conn.close()
    dict_cur.close() 
    return render_template("categories.html", categories=results)

@app.route("/shippers", methods=["GET", "POST"])
def shippers():
    conn = connectToDB()
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        dict_cur.execute('SELECT * FROM shippers')
    except:
        print('could not execute query')
    results = dict_cur.fetchall()
    conn.close()
    dict_cur.close() 
    return render_template("shippers.html", shippers=results)

@app.route("/us_states", methods=["GET", "POST"])
def us_states():
    conn = connectToDB()
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        dict_cur.execute('SELECT * FROM us_states')
    except:
        print('could not execute query')
    results = dict_cur.fetchall()
    conn.close()
    dict_cur.close() 
    return render_template("us_states.html", us_states=results)

if __name__ == "__main__":
    app.run(debug=True)