from flask import Flask, jsonify, request
import json
from services.scraping import search_camera
app = Flask(__name__)


@app.route("/", methods=["GET"])
def is_alive():
    return jsonify({
        "Are you alive?": "Yes",
        "status": 200
    })


@app.route("/search", methods=["POST"])
def search_and_compute_price():
    req: json = request.get_json()
    model: str = req.get("searched_model")
    price = search_camera(model)

    if 'error' in price:
        return jsonify({"error": price.get("error"), "status": 424})

    if len(price):
        price['status'] = 200
    else:
        price['status'] = 404

    return jsonify(price)


@app.after_request
def add_cors_headers(response):
    r = request.referrer[:-1]
    white_list = ['http://localhost:4200', 'https://analog-argus.netlify.app']
    if r in white_list:
        response.headers.add('Access-Control-Allow-Origin', r)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT')
    return response
