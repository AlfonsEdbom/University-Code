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
        results = dict_cur.fetchall()
        dict_cur.execute('SELECT * FROM shippers')
        results1 = dict_cur.fetchall()
    except:
        print('could not execute query')
    #results = dict_cur.fetchall()
    conn.close()
    dict_cur.close() 
    return render_template("categories.html", categories=results, shippers=results1)


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

# insert into categories
@app.route("/cateogries/add", methods=["POST"])
def add_category():
    conn = connectToDB()
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    category_id = int(request.form['category_id'])
    category_name = request.form['category_name']
    description = request.form['description']
    picture = request.form['picture']

    dict_cur.execute("INSERT INTO categories (category_id, category_name, description) VALUES (%s, %s, %s)",
    (category_id, category_name, description))
        
    conn.commit()
    conn.close()
    dict_cur.close()
    print('123')
    return redirect(url_for("/categories"))

# insert into shippers
@app.route("/shippers/add", methods=["POST"])
def add_shipper():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        shipper_id = int(request.form['shipper_id'])
        company_name = request.form['company_name']
        phone = request.form['phone']

        dict_cur.execute("INSERT INTO shippers (shipper_id, company_name, phone) VALUES (%s, %s, %s)",
        (shipper_id, company_name, phone))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/shippers")

if __name__ == "__main__":
    app.run(debug=True)