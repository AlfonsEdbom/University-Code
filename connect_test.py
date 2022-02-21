import psycopg2

print("Connecting to database")

connection = psycopg2.connect(host="localhost",
 dbname="postdata",
  user="postgres",
   password="biotek18")

my_cursor = connection.cursor()

my_cursor.execute('SELECT category_name FROM categories;')

records = my_cursor.fetchall()
print(records)


my_cursor.close()

connection.close()

print("No longer connected to database")