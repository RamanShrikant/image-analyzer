import io
import numpy as np
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS
import tflite_runtime.interpreter as tflite
from PIL import Image
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://image-analyzer-xi.vercel.app"}})

print("📁 Current working directory:", os.getcwd())
print("📂 Files in directory:", os.listdir())

# --- Load the new 4-class model ---
try:
    interpreter = tflite.Interpreter(model_path="freshness_model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("✅ New 4-class model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)

# Class order must match your Colab training order
CLASSES = ["Fresh", "Slightly Aging", "Spoiled", "Non-Food"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "🚀 Image Analyzer backend is live",
        "classes": CLASSES
    })

@app.route("/analyze-freshness", methods=["POST"])
def analyze_freshness():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    img_bytes = file.read()

    # --- Preprocess for MobileNetV2 ---
    pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
    x = np.array(pil_img, dtype=np.float32)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # match training normalization

    # --- Run inference ---
    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_details[0]['index'])[0]

    # --- Map predictions to labels ---
    confidence_scores = {CLASSES[i]: float(preds[i] * 100) for i in range(len(CLASSES))}
    top_class = CLASSES[np.argmax(preds)]
    top_conf = float(np.max(preds) * 100)

    # --- Handle Non-Food gracefully ---
    if top_class == "Non-Food" and top_conf > 50:
        return jsonify({
            "status": "Non-Food 🚫",
            "confidence": round(top_conf, 2),
            "predictions": confidence_scores
        }), 200

    # --- Return AI-based freshness result ---
    return jsonify({
        "status": top_class,
        "confidence": round(top_conf, 2),
        "predictions": confidence_scores
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
