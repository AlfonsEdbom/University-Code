# Lab 2 - Python

This is a CRUD application using the Python package Flask as the web backend, the database backend used was PostgreSQL and teh database connector used was psycopg2. 

## Setup
Make sure you have the following applications before proceeding:  
- `pip` : [Pip installation](https://pip.pypa.io/en/stable/installing/)
- `PostgreSQL` : [Postgresql installation](https://www.postgresql.org/download/)

Download the this git repository to your computer locally. 

## Installing Dependencies
From this directory, run the command:
```bash
python3 -m pip install -r requirements.txt
```
If the install was successful, go into the `website ` directory and with the following command the Flask web-server should start: 
```bash
flask run
```

### Creating the database
To create the database used by the wensite go into the `database` directory and log into your PostgreSQL user by running the following command in a terminal window:
```bash
psql -U <username>
```
where username is your PostgreSQL. Enter your password.
You should now be in a PostgreSQL command-line interface. To create this database write the following command in the terminal window:
```bash
\i snacks.sql
```
After the command is done make that a database called `snacks` exists in the list of your tables when you write the following command in the POSTGRESQL command-line window:
```bash
\l
```

## Application structure

The application contains a couple of directories and files, briefly described below.

* `database` Contains files that has to do with the setup of database
  * `snacks.sql` Contains the instructions for how to build the database, it also adds some starting tuples to each table 
* `website` Contains files that has to do with the actual web application
  * `app.py` Contains the actual application, with the routes that the user can
  visit, as well as the logic.
  * `templates/` Contains templates that flask can render.
    * `templates/base.html` Contains the base template that all other templates
    can be derived from.
    * `templates/index.html` The first page that the user sees when opening the
    application.
    * `XXX.html` Contains the html that is rendered for the other pages

## Links
* [Flask quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
* [Psycopg2 documentation](https://www.psycopg.org/docs/)
* [Postgresql documentation](https://www.postgresql.org/docs/)
