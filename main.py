from keras.models import load_model
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import os

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_updated.keras")

trained_model = load_model(MODEL_PATH)

@app.route("/upload", methods=["POST"])
def handle_upload():
    file_key = None
    if "imageFile" in request.files:
        file_key = "imageFile"
    elif "image" in request.files:
        file_key = "image"
    else:
        return jsonify({"error": "no file in request"}), 400

    file = request.files[file_key]
    if file.filename == "":
        return jsonify({"error": "no file attached"}), 400
    
    if file:
        try:
            image = Image.open(file.stream)
            new_size = (180, 180)
            image = image.convert('RGB')
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            image_array = np.array(image).astype(np.float32)
            image_array = np.expand_dims(image_array, axis=0)

            prediction = predict(image_array)
            print(f"Predicted probabilities: cats={prediction[0][0]:.4f}, dogs={prediction[0][1]:.4f}, other={prediction[0][2]:.4f}")
            return jsonify({"cat": float(prediction[0][0]),
                            "dog": float(prediction[0][1]),
                            "other": float(prediction[0][2])})

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def predict(processed_image_array):
    ans = trained_model.predict(processed_image_array)
    return ans

if __name__ == "__main__":
    app.run(host="0.0.0.0")