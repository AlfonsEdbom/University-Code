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

# display categories
@app.route("/tables", methods=["GET"])
def display_tables():
    conn = connectToDB()
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        dict_cur.execute('SELECT * FROM categories')
    except:
        print('could not execute query')
    results = dict_cur.fetchall()
    conn.close()
    dict_cur.close() 
    return render_template("display.html", categories=results)

@app.route("/add")
def add_tuple():
    pass

if __name__ == "__main__":
    app.run(debug=True)