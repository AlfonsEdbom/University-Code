from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# function for connecting to db
def connectToDB():
    connectionString = 'dbname=northwind user=postgres port=5432 host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")

# first page, "home page"
@app.route("/")
def home():
    return render_template("index.html")

#########################################################
####### display pages for all or individual pages #######
#########################################################

# display all tables in db etc
@app.route("/all_tables")
def all_tables():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM categories')
        results = dict_cur.fetchall()
        dict_cur.execute('SELECT * FROM shippers')
        results1 = dict_cur.fetchall()
        dict_cur.execute('SELECT * FROM us_states')
        results2 = dict_cur.fetchall()
        dict_cur.close()
    except:
        print('could not execute query')
    finally:
        if conn is not None:
            conn.close()
    #results = dict_cur.fetchall()
    return render_template("all_tables.html", categories=results, shippers=results1, us_states=results2)


# display categories table etc
@app.route("/categories")
def categories():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM categories')
        results = dict_cur.fetchall()
        dict_cur.close()
    except:
        print('could not execute query')
    #results = dict_cur.fetchall()
    finally:
        if conn is not None:
            conn.close()
    return render_template("categories.html", categories=results)


@app.route("/shippers")
def shippers():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM shippers')
        results = dict_cur.fetchall()
        dict_cur.close()
    except:
        print('could not execute query')
    finally:
        if conn is not None:
            conn.close()
    return render_template("shippers.html", shippers=results)


@app.route("/us_states")
def us_states():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM us_states')
        results = dict_cur.fetchall()
        dict_cur.close() 
    except:
        print('could not execute query')
    finally:
        if conn is not None:
            conn.close()
    return render_template("us_states.html", us_states=results)

###########################################
####### functions for adding tuples #######
###########################################

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

    return redirect(url_for("/categories"))

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

###########################################
####### functions for adding tuples #######
###########################################

@app.route("/shippers/update", methods=["POST"])
def update_shipper():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        shipper_id = int(request.form['shipper_id'])
        company_name = request.form['company_name']
        phone = request.form['phone']

        dict_cur.execute("UPDATE shippers SET company_name = %s, phone = %s WHERE shipper_id = %s", 
        (company_name, phone, shipper_id))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/shippers")

#############################################
####### functions for deleting tuples #######
#############################################

@app.route("/shippers/delete", methods=["POST"])
def delete_shipper():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        shipper_id = request.form['shipper_id']

        dict_cur.execute("DELETE FROM shippers WHERE shipper_id = %s", 
        (shipper_id,))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/shippers")

#####################################
####### look at state regions #######
#####################################

@app.route("/us_states/query", methods=['POST'])
def query_us_states():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        state_region = request.form['state_region']
        print(state_region)
        if state_region == ('all') or state_region == ('All'):
            print(1)
            dict_cur.execute("SELECT * FROM us_states")
            results = dict_cur.fetchall()
            dict_cur.close()
        else:
            dict_cur.execute("SELECT * FROM us_states WHERE state_region = %s", (state_region,))
            results = dict_cur.fetchall()
            dict_cur.close()
            print(2)
    except:
        print('could not execute query')
    finally:
        if conn is not None:
            conn.close()
            print(3)
    return render_template("us_states.html", us_states=results)


if __name__ == "__main__":
    app.run(debug=True)