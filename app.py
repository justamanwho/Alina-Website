from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from dotenv import load_dotenv
import requests
import json
import os


app = Flask(__name__)
load_dotenv('.env')
app.secret_key = os.getenv('SECRET_KEY')


LANGUAGE_OPTIONS = {
    'en': {'name': 'English'},
    'pl': {'name': 'Polski'},
    'ukr': {'name': 'Українська'},
    'ru': {'name': 'Русский'}
}


def load_translations(lang_code):
    file_path = f"translations/{lang_code}.json"
    if not os.path.exists(file_path):
        file_path = "translations/ukr.json"  # Default Language
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    if 'lang' not in session:
        session['lang'] = 'ukr' # Defaul Language

    translations = load_translations(session['lang'])
    max_length = max(len(option['name']) for option in LANGUAGE_OPTIONS.values())
    return render_template('index.html',
                           translations=translations,
                           lang=session['lang'],
                           language_options=LANGUAGE_OPTIONS,
                           max_length=max_length)

@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    if lang_code in LANGUAGE_OPTIONS:
        session['lang'] = lang_code
    return redirect(url_for('index'))


# References for website

@app.route('/jolyne', methods=['GET'])
def jojo_reference_jolyne():
    return '<img src="../static/jolyne.png" alt="Jolyne">'


@app.route('/avdol', methods=['GET'])
@app.route('/jojo-reference', methods=['GET'])
def jojo_reference_avdol():
    return '<img src="../static/avdol.png" alt="Avdol">'


# Webhooks for telegram bots

JOJO_BOT_URL = "https:127.0.0.1:8443/jojo-webhook"
CHESS_BOT_URL = "https:127.0.0.1:8444/chess-webhook"
THE_WORLD_BOT_URL = "https:127.0.0.1:8445/the-world-webhook"

@app.route("/jojo-webhook", methods=["POST"])
def jojo_webhook():
    try:
        update = request.get_json()
        response = requests.post(JOJO_BOT_URL, json=update, timeout=5)

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chess-webhook", methods=["POST"])
def chess_webhook():
    try:
        update = request.get_json()
        response = requests.post(CHESS_BOT_URL, json=update, timeout=5)

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/the-world-webhook", methods=["POST"])
def the_world_webhook():
    try:
        update = request.get_json()
        response = requests.post(THE_WORLD_BOT_URL, json=update, timeout=5)

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()
