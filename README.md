# Lab 2 - Python

This is a CRUD application using the Python package Flask as the web backend, the database backend used was PostgreSQL and teh database connector used was psycopg2. 

## Setup
Make sure you have `pip` installed before
proceeding: [Pip installation](https://pip.pypa.io/en/stable/installing/).

Download the this git repository to your computer locally. 

## Installing Dependencies
From this directory, run the command:
```bash
python3 -m pip install -r requirements.txt
```
If successful, the following command should start the Flask web-server: 
```bash
flask run
```

If all went well, you should now be able to test the application by
visiting [http://localhost:5000/](http://localhost:5000/) 
(or the URL output by Flask).

### Error: `flask: command not found`
If you still cannot run Flask after the installation, you might have to
add your local bin folder to the PATH. To do this, you can run:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```
and then restart your terminal. If the problem persists, check the output of the
`python3 -m pip install -r requirements.txt` command for additional information.

## Application structure

The application contains a couple of directories and files, briefly described below.

* `app.py` Contains the actual application, with the routes that the user can
  visit, as well as the logic.
* `templates/` Contains templates that flask can render.
    * `templates/base.html` Contains the base template that all other templates
    can
      be derived from.
    * `templates/index.html` The first page that the user sees when opening the
    application.
    * `templates/snacks.html` The snack interface. The interface shows all
    available snacks, as well as controls that allows a user to add or remove
    snacks.

## Links
* [Flask quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
* [Psycopg2 documentation](https://www.psycopg.org/docs/)
