import io
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import tflite_runtime.interpreter as tflite
from PIL import Image
import os

app = Flask(__name__)

# --- Enable CORS for your frontend ---
from flask_cors import CORS

CORS(app, resources={r"/*": {
    "origins": [
        "https://image-analyzer-xi.vercel.app",
        "https://image-analyzer-b0ii40yu0-ramans-projects-207e5212.vercel.app",
        "http://localhost:3000"  # for local testing
    ],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})


# --- Load your trained TFLite model ---
MODEL_PATH = "freshness_model.tflite"
print("🧾 Using model file at:", os.path.abspath(MODEL_PATH))
print("📦 Model file size:", os.path.getsize(MODEL_PATH), "bytes")


try:
    interpreter = tflite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(f"✅ Model '{MODEL_PATH}' loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "AI Freshness Analyzer backend is live 🚀",
        "routes": ["/", "/analyze-freshness (POST)"]
    })

@app.route("/analyze-freshness", methods=["POST"])
def analyze_freshness():
    try:
        # --- 1️⃣ Read uploaded image ---
        file = request.files['image']
        img_bytes = file.read()

        # --- 2️⃣ Preprocess for the model ---
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
        x = np.array(img, dtype=np.float32) / 255.0
        x = np.expand_dims(x, axis=0)

        # --- 3️⃣ Run inference ---
        interpreter.set_tensor(input_details[0]['index'], x)
        interpreter.invoke()
        preds = interpreter.get_tensor(output_details[0]['index'])[0]
        bias = np.array([1.0, 1.0, 1.15])  # Fresh, Aging, Spoiled
        preds = preds * bias
        preds = preds / np.sum(preds)

        # --- 4️⃣ Interpret predictions ---
        classes = ["Fresh", "Slightly Aging", "Spoiled"]
        predicted_index = int(np.argmax(preds))
        confidence = float(preds[predicted_index])
        status = classes[predicted_index]

        # --- 5️⃣ Build response ---
        return jsonify({
            "status": status,
            "confidence": round(confidence * 100, 2),
            "predictions": {
                "Fresh": round(float(preds[0]) * 100, 2),
                "Slightly Aging": round(float(preds[1]) * 100, 2),
                "Spoiled": round(float(preds[2]) * 100, 2)
            }
        })

    except Exception as e:
        print("❌ Error during inference:", e)
        return jsonify({"error": "Failed to analyze image", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)