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
# --- analyze image properties ---
# Resize for consistency
img = cv2.resize(img, (300, 300))

# Convert to HSV (color model)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
brightness = np.mean(hsv[:, :, 2])
saturation = np.mean(hsv[:, :, 1])

# Convert to grayscale for spot detection
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
_, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)
spots = cv2.countNonZero(thresh)
spot_ratio = spots / (img.shape[0] * img.shape[1])

# Calculate composite freshness score
freshness_score = int(
    (0.6 * (brightness / 255) + 0.3 * (saturation / 255) + 0.1 * (1 - spot_ratio)) * 100
)

# Determine freshness status
if freshness_score > 75:
    status = "Fresh"
elif freshness_score > 50:
    status = "Slightly Aging"
else:
    status = "Spoiled"

return jsonify({
    "freshness_score": freshness_score,
    "status": status,
    "spots_detected": int(spots),
    "brightness": round(brightness, 2),
    "saturation": round(saturation, 2)
})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
