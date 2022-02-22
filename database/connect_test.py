import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def connect_to_database(host, user, password):
   con = psycopg2.connect(host=host, user=user, password=password, database="lab2")
   con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

   return con

def create_database(db_name):
   sqlCommand = f"CREATE DATABASE {db_name};"

   return sqlCommand


def create_table(table_name):

   sqlCommand = f"""CREATE TABLE {table_name} (
      name TEXT PRIMARY KEY,
      amount INTEGER,
      cost INTEGER);"""
   return sqlCommand






if __name__ == "__main__":
   con = connect_to_database("localhost", "postgres", "biotek18")
   cur = con.cursor()

   #db_command = create_database("lab2")
   #cur.execute(db_command)

   #table_command = create_table("Snacks")
   #cur.execute(table_command)

   

   cur.close()
   con.close()

   print("No longer connected to the database")