from flask import Flask, request, render_template
import numpy as np
import os
import io
from PIL import Image

app = Flask(__name__)

# ===== Model load (lazy loading to avoid startup timeout) =====
MODEL_PATH = os.path.join(os.path.dirname(__file__), "Final_Model.h5")
model = None
tf = None  # Lazy import TensorFlow

# Image size used during training
IMG_SIZE = 128

def load_model():
    """Lazy load model only when needed - imports TensorFlow on first call"""
    global model, tf
    if model is None:
        try:
            # Check if model file exists first
            if not os.path.exists(MODEL_PATH):
                print(f"ERROR: Model file not found at {MODEL_PATH}")
                print(f"Current working directory: {os.getcwd()}")
                print(f"App file directory: {os.path.dirname(__file__)}")
                print(f"Files in directory: {os.listdir(os.path.dirname(__file__))}")
                model = None
                return None
            
            # Lazy import TensorFlow only when needed
            if tf is None:
                print("Importing TensorFlow...")
                import tensorflow as tf
                print("TensorFlow imported successfully")
            
            print(f"Loading model from {MODEL_PATH}...")
            model = tf.keras.models.load_model(MODEL_PATH)
            print(f"Model loaded successfully from {MODEL_PATH}")
        except FileNotFoundError as e:
            print(f"ERROR: Model file not found: {e}")
            print(f"Expected path: {MODEL_PATH}")
            print(f"Current directory: {os.getcwd()}")
            model = None
        except Exception as e:
            print(f"Error loading model: {e}")
            print(f"Model path attempted: {MODEL_PATH}")
            print("Please ensure Final_Model.h5 is in the same directory as app.py")
            model = None
    return model

def get_tf_image():
    """Lazy import tensorflow.keras.preprocessing.image"""
    global tf
    if tf is None:
        import tensorflow as tf
    from tensorflow.keras.preprocessing import image
    return image


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Lazy load model on first prediction
    model_instance = load_model()
    if model_instance is None:
        error_msg = (
            "Model file (Final_Model.h5) not found. "
            "Please ensure the model file is in the same directory as app.py. "
            "Check server logs for detailed error information."
        )
        return render_template("index.html", prediction=error_msg, error=True)
    
    if "file" not in request.files:
        return render_template("index.html", prediction="Please upload an MRI image.")

    file = request.files["file"]

    if file.filename == "":
        return render_template("index.html", prediction="No file selected.")

    # Read uploaded image into PIL
    img = Image.open(io.BytesIO(file.read()))
    img = img.resize((IMG_SIZE, IMG_SIZE))  # 128 x 128

    # Convert to array (lazy import)
    image_module = get_tf_image()
    img_array = image_module.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    print("DEBUG img_array.shape:", img_array.shape)

    # ----- MULTI-CLASS PREDICTION -----
    preds = model_instance.predict(img_array)
    class_index = np.argmax(preds[0])
    confidence = round(np.max(preds[0]) * 100, 2)

    class_labels = ["Glioma", "Meningioma", "Pituitary", "No Tumor"]
    label = class_labels[class_index]

    # ===== EXTRA INFO: Tumor name & simple "size" category =====
    if label == "No Tumor":
        tumor_name = "No Tumor Detected"
        tumor_size = "To be Fetched"
    else:
        tumor_name = f"{label} Tumor"

        # NOTE: This is NOT a real medical size calculation.
        # It’s just a rough, demo-style category based on model confidence.
        if confidence >= 85:
            tumor_size = "Large (high confidence)"
        elif confidence >= 60:
            tumor_size = "Medium"
        else:
            tumor_size = "Small / Early-stage (low confidence)"

    return render_template(
        "index.html",
        prediction=label,
        confidence=confidence,
        tumor_name=tumor_name,
        tumor_size=tumor_size,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
