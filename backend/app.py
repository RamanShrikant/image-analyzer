import io
import numpy as np
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS
import tflite_runtime.interpreter as tflite
from PIL import Image
import os

app = Flask(__name__)

# Debug info for Railway environment
print("📁 Current working directory:", os.getcwd())
print("📂 Files in directory:", os.listdir())

CORS(app, resources={r"/*": {"origins": "https://image-analyzer-xi.vercel.app"}})

# --- Load the MobileNetV2 TFLite model ---
try:
    interpreter = tflite.Interpreter(model_path="mobilenet_v2.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)


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
    img_bytes = file.read()

    # --- 1️⃣ Food classification (MobileNetV2) ---
    pil_img = Image.open(io.BytesIO(img_bytes)).resize((224, 224))
    x = np.array(pil_img, dtype=np.float32)
    x = np.expand_dims(x, axis=0)
    x = (x / 127.5) - 1.0

    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_details[0]['index'])[0]
    top_idx = np.argsort(preds)[::-1][:3]

    try:
        labels = open("label.txt").read().splitlines()
    except Exception as e:
        print("❌ Error reading label file:", e)
        return jsonify({"error": "labels file missing", "details": str(e)}), 500

    top_labels = [labels[i].lower() for i in top_idx]

    FOOD_KEYWORDS = [
        "food", "fruit", "vegetable", "banana", "apple", "orange", "tomato",
        "carrot", "grape", "salad", "pizza", "bread", "meat", "fish", "sandwich"
    ]

    if not any(word in lbl for lbl in top_labels for word in FOOD_KEYWORDS):
        return jsonify({
            "error": "Non-food image detected.",
            "predictions": top_labels
        }), 200

    # --- 2️⃣ OpenCV freshness logic ---
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (300, 300))

    # 🔹 Normalize lighting
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = cv2.equalizeHist(l)
    img_eq = cv2.merge((l_eq, a, b))
    img = cv2.cvtColor(img_eq, cv2.COLOR_LAB2BGR)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])
    saturation = np.mean(hsv[:, :, 1])

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 🔹 Adaptive threshold for spot detection
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    spots = cv2.countNonZero(thresh)
    spot_ratio = spots / (img.shape[0] * img.shape[1])

    # 🔹 New weight ratios (spots matter more)
    freshness_score = int(
        (0.3 * (brightness / 255) +
         0.2 * (saturation / 255) +
         0.5 * (1 - spot_ratio)) * 100
    )

    if freshness_score > 75:
        status = "Fresh"
    elif freshness_score > 50:
        status = "Slightly Aging"
    else:
        status = "Spoiled"

    return jsonify({
        "labels": top_labels,
        "freshness_score": freshness_score,
        "status": status,
        "spots_detected": int(spots),
        "brightness": round(brightness, 2),
        "saturation": round(saturation, 2)
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
