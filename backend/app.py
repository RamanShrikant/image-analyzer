from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)  # enable CORS for all routes


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "Image Analyzer backend is live 🚀",
        "routes": ["/", "/analyze-freshness (POST)"]
    })


@app.route("/analyze-freshness", methods=["POST"])
def analyze_freshness():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # TEMP: just return dummy result for testing
    return jsonify({
        "freshness_score": 80,
        "status": "Fresh",
        "spots_detected": 0
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
