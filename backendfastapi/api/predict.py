from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
from .model import load_model_from_gcs
from .firestore import save_to_firestore
import datetime
import traceback
import secrets
import string

# Inisialisasi model secara global
model = load_model_from_gcs()

# Fungsi untuk membuat ID unik
def generate_unique_id(length=20):
    characters = string.ascii_letters + string.digits  # Kombinasi huruf besar, kecil, dan angka
    return ''.join(secrets.choice(characters) for _ in range(length))

# Define input schema
class PredictionInput(BaseModel):
    Exercise: str
    Heart_Disease: str
    Sex: str
    BMI: float
    Smoking_History: str
    Alcohol_Consumption: float
    Fruit_Consumption: float
    Green_Vegetables_Consumption: float
    FriedPotato_Consumption: float

# Inisialisasi router
predict_endpoint = APIRouter()

# Preprocessing input data
def preprocess_input(data: PredictionInput):
    mappings = {
        "Exercise": {"Yes": 1, "No": 0},
        "Heart_Disease": {"Yes": 1, "No": 0},
        "Sex": {"Male": 1, "Female": 0},
        "Smoking_History": {"Yes": 1, "No": 0}
    }

    # Validasi nilai input kategori
    valid_values = {
        "Exercise": ["Yes", "No"],
        "Heart_Disease": ["Yes", "No"],
        "Sex": ["Male", "Female"],
        "Smoking_History": ["Yes", "No"]
    }
    for field, valid in valid_values.items():
        value = getattr(data, field)
        if value not in valid:
            raise HTTPException(status_code=400, detail=f"Invalid value for {field}: {value}")

    # Proses data menjadi array numerik
    try:
        processed_data = [
            mappings["Exercise"][data.Exercise],
            mappings["Heart_Disease"][data.Heart_Disease],
            mappings["Sex"][data.Sex],
            data.BMI,
            mappings["Smoking_History"][data.Smoking_History],
            data.Alcohol_Consumption,
            data.Fruit_Consumption,
            data.Green_Vegetables_Consumption,
            data.FriedPotato_Consumption
        ]
        return np.array([processed_data], dtype=float)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input value: {e}")

# Endpoint prediksi
@predict_endpoint.post("/predict")
async def predict(data: PredictionInput):
    global model  # Akses variabel global model
    if model is None:
        model = load_model_from_gcs()
        if model is None:
            raise HTTPException(status_code=500, detail="Model could not be loaded. Please check the model URL or availability.")

    try:
        # Preprocessing input
        processed_data = preprocess_input(data)
        print("Processed Data:", processed_data)

        # Prediksi menggunakan model
        prediction = model.predict(processed_data)
        print("Model Output:", prediction)

        # Pemetaan hasil prediksi ke label (hanya 3 kelas)
        result_mapping = {0: "Poor", 1: "Fair", 2: "Good"}
        predicted_label = np.argmax(prediction, axis=1)[0]
        result = result_mapping.get(predicted_label, "Unknown")

        if result == "Unknown":
            print(f"Unexpected predicted label: {predicted_label}")

        # Buat ID unik
        document_id = generate_unique_id()

        # Buat saran berdasarkan hasil
        suggestion = generate_suggestion(result)

        # Simpan hasil ke Firestore
        prediction_data = {
            "id": document_id,
            "input": data.dict(),
            "result": result,
            "suggestion": suggestion,
            "createdAt": datetime.datetime.now().isoformat()
        }
        try:
            save_to_firestore("predictions", document_id, prediction_data)
        except Exception as firestore_error:
            print(f"Error saving to Firestore: {firestore_error}")

        # Kembalikan hasil
        return {
            "id": document_id,
            "result": result,
            "suggestion": suggestion
        }
    except Exception as e:
        print("Error Traceback:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

# Fungsi untuk memberikan saran berdasarkan hasil prediksi
def generate_suggestion(result):
    suggestions = {
        "Poor": "Consider consulting a healthcare professional to improve your heart health.",
        "Fair": "Maintain a balanced diet and regular exercise to improve your condition.",
        "Good": "Keep up your healthy lifestyle and focus on consistent exercise."
    }
    return suggestions.get(result, "No suggestion available.")

