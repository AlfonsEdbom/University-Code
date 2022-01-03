
from flask import Flask, request, render_template, jsonify
from junior_model import store, load, save
from junior_model import dictionary, get_dictionary

app = Flask(__name__)

@app.route('/')
def home():
    load()
    return render_template('index.html')

@app.route('/add', methods=['GET'])
def add():
    key = request.args['key']
    value = request.args['value']
    store(key,value)
    save()
    return render_template('index.html')

@app.route('/print')
def print():
    return render_template('view.html', name='jinga_junior', dictionary=get_dictionary())

@app.route('/print-failing')
def print_failing():
    return render_template('view.html',name='jinga_junior', dictionary=dictionary)

@app.route('/clear', methods=['GET'])
def clear():
    return "clear"

if __name__ == '__main__':
    app.run(debug=True,  port=8080)
