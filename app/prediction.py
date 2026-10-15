CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry___Powdery_mildew",
    "Cherry___healthy",
    "Corn___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

import tensorflow as tf
import numpy as np

from pathlib import Path
from PIL import Image

# Load trained model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.keras"

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")

def preprocess_image(image):
    """
    Preprocess uploaded image for prediction.
    """

    image = image.convert("RGB")

    # Resize image
    image = image.resize((224, 224))

    # Convert to NumPy array
    image = tf.keras.utils.img_to_array(image)


    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    return image

# Prediction Function

def split_class_name(class_name):
    """
    Split a PlantVillage class name into (plant, disease).
    """

    parts = class_name.split("___")

    return parts[0], parts[1].replace("_", " ").title()


def predict_disease(image, top_k=1):
    """
    Predict plant disease from an uploaded or captured image.

    Returns
    -------
    tuple
        (plant_name, disease_name, confidence, class_name, alternatives)
        where `alternatives` is a list of (plant, disease, confidence)
        for the next best classes, longest first.
    """

    processed_image = preprocess_image(image)

    probabilities = model.predict(processed_image, verbose=0)[0]

    ranked = np.argsort(probabilities)[::-1]

    predicted_class = int(ranked[0])

    confidence = float(probabilities[predicted_class])

    class_name = CLASS_NAMES[predicted_class]

    plant_name, disease_name = split_class_name(class_name)

    alternatives = [
        (*split_class_name(CLASS_NAMES[i]), float(probabilities[i]))
        for i in ranked[1:top_k]
    ]

    return plant_name, disease_name, confidence, class_name, alternatives