from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'alina.kostiuk_webpage1key'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contacts', methods=['GET'])
def contacts():
    return render_template('contacts.html')
