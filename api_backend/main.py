from flask import Flask, jsonify, request
import requests
import xml.etree.ElementTree as ET
import logging
import os

app = Flask(__name__)

BASE_API_URL = "https://economia.awesomeapi.com.br"
API_KEY = os.getenv("API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_api_key():
    if os.getenv("FLASK_ENV") != "development" and os.getenv("API_KEY"):
        api_key = request.headers.get("X-API-KEY")
        if not api_key or api_key != os.getenv("API_KEY"):
            logging.warning("Unauthorized access attempt")
            return False
    return True
    

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/price/available", methods=["GET"])
def get_available_currencies():
    if not validate_api_key():
        return jsonify({"error": "Unauthorized"}), 401
    
    response = requests.get(f"{BASE_API_URL}/xml/available/uniq")
    if response.status_code != 200:
        logging.error(f"Failed to fetch available currencies. Status code: {response.status_code}")
        return jsonify({"error": "Failed to fetch data"}), 500
    
    root = ET.fromstring(response.content)
    currencies = {child.tag: child.text for child in root}
    return jsonify(currencies)

@app.route("/price/stats/<string:currency>", methods=["GET"])
def get_currency_status(currency):
    if not validate_api_key():
        return jsonify({"error": "Unauthorized"}), 401
    
    response = requests.get(f"{BASE_API_URL}/json/last/{currency}")
    if response.status_code != 200:
        logging.error(f"Failed to fetch currency stats for {currency}. Status code: {response.status_code}")
        return jsonify({"error": "Failed to fetch data"}), 500
    
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
