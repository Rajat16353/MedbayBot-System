import warnings
import gc
from flask import Flask, request, jsonify
from flask_cors import CORS
from Chatbot.chatbot import chat
from DiseaseInfo.get_info import get_disease_info
from whitenoise import WhiteNoise
from Exception_check.exception_check import check_fields_disease_info, check_fields_post_message

warnings.simplefilter("ignore")

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
cors = CORS(app)


@app.route('/postMessage', methods=['POST'])
def postMessage():
    request_json = request.json
    if check_fields_post_message(request_json) == True:
        response = chat(request_json)
    else:
        response = check_fields_post_message(request_json)
    gc.collect()
    return jsonify(response)


@app.route('/getDiseaseInfo', methods=['POST'])
def get_info():
    request_json = request.json
    if check_fields_disease_info(request_json) == True:
        response = get_disease_info(request_json)
    else:
        response = check_fields_disease_info(request_json)
    gc.collect()
    return jsonify(response)


@app.route('/', methods=['GET'])
def index_page():
    return "This is the MedBay bot API."
