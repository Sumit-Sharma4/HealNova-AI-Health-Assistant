from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator

import joblib
import numpy as np
import pandas as pd
import os
import json

from werkzeug.security import generate_password_hash, check_password_hash
from utils.ai_gemini import ask_ai_doctor

# ==============================
# APP INITIALIZATION
# ==============================

app = Flask(__name__)
CORS(app)   # ⭐ MUST come immediately after app creation

translator = Translator()

# ==============================
# TRANSLATE ROUTE
# ==============================

@app.route("/translate", methods=["POST"])
def translate_text():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"translated": ""})

        translated = translator.translate(text, dest="hi")

        return jsonify({"translated": translated.text})

    except Exception as e:
        print("Translation error:", e)
        return jsonify({"translated": text})
        

# ==============================
# USERS FILE
# ==============================

USERS_FILE = "users.json"

# -------------------------------
# LOAD ML MODEL
# -------------------------------
model = joblib.load("ML/model.pkl")

# -------------------------------
# SYMPTOM ORDER
# -------------------------------
SYMPTOM_KEYS = [
    "fever","headache","cough","body_pain","stomach_pain",
    "diarrhea","vomiting","sore_throat","runny_nose",
    "chest_pain","short_breath","skin_rash","itching",
    "acidity","back_pain","joint_pain","high_bp","low_bp","fatigue"
]

# -------------------------------
# GEMINI API KEY
# -------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Gemini key loaded:", bool(GEMINI_API_KEY))

# -------------------------------
# UTIL: LOAD & SAVE USERS
# -------------------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    return "HeaLNova Backend API Running"

# -------------------------------
# 🔐 SIGNUP
# -------------------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    users = load_users()

    if any(u["email"] == email for u in users):
        return jsonify({"error": "Email already registered"}), 400

    user = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password)
    }

    users.append(user)
    save_users(users)

    return jsonify({"message": "Signup successful"}), 201

# -------------------------------
# 🔐 LOGIN
# -------------------------------
@app.route("/login", methods=["POST"])
def login():
    print("🔥 LOGIN API HIT")

    data = request.json or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    users = load_users()

    for user in users:
        if user["email"] == email and check_password_hash(user["password"], password):
            return jsonify({
                "user": {
                    "name": user["name"],
                    "email": user["email"]
                }
            })

    return jsonify({"error": "Invalid email or password"}), 401

# -------------------------------
# 1️⃣ DISEASE PREDICTION
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict_disease():
    data = request.json or {}

    selected_symptoms = sum(data.get(k, 0) for k in SYMPTOM_KEYS)

    if selected_symptoms == 1:
        rules = {
            "fatigue": ("Possible Dehydration or Weakness", "General Physician"),
            "skin_rash": ("Possible Acne or Skin Allergy", "Dermatologist"),
            "cough": ("Mild Cough or Throat Irritation", "General Physician"),
            "headache": ("General Headache", "General Physician"),
        }

        for symptom, (disease, doctor) in rules.items():
            if data.get(symptom) == 1:
                return jsonify({
                    "predicted_disease": disease,
                    "disease_type": "single_symptom",
                    "specialist": doctor,
                    "disclaimer": "This is not a medical diagnosis."
                })

        return jsonify({"error": "Select at least two symptoms"})

    input_features = np.array([[data.get(k, 0) for k in SYMPTOM_KEYS]])
    ml_prediction = model.predict(input_features)[0]

    final_disease = ml_prediction
    disease_type = "ml"

    if ml_prediction in ["Eczema", "Fungal Infection"] and data.get("itching"):
        final_disease = "Skin Condition (Eczema / Fungal Infection)"
        disease_type = "overlap"

    if ml_prediction in ["Asthma", "Bronchitis"] and data.get("short_breath"):
        final_disease = "Respiratory Condition (Asthma / Bronchitis)"
        disease_type = "overlap"

    if data.get("fever") and data.get("fatigue") and data.get("body_pain"):
        final_disease = "Heat Stroke"
        disease_type = "rule_based"

    specialist_map = {
        "Heat Stroke": "General Physician",
        "Respiratory Condition (Asthma / Bronchitis)": "Pulmonologist",
        "Skin Condition (Eczema / Fungal Infection)": "Dermatologist"
    }

    return jsonify({
        "predicted_disease": final_disease,
        "ml_prediction": ml_prediction,
        "disease_type": disease_type,
        "specialist": specialist_map.get(final_disease, "General Physician"),
        "disclaimer": "Health guidance only."
    })

# -------------------------------
# 2️⃣ OFFLINE DISEASE INFO
# -------------------------------
@app.route("/disease-info/<disease_name>")
def get_disease_info(disease_name):
    try:
        df = pd.read_csv("ML/disease_info.csv")
        row = df[df["disease"].str.lower() == disease_name.lower()]
        if row.empty:
            return jsonify({"error": "Disease not found"})
        return jsonify(row.iloc[0].to_dict())
    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------------------
# 3️⃣ AI DOCTOR
# -------------------------------
@app.route("/ai-doctor", methods=["POST"])
def ai_doctor():
    data = request.json or {}
    reply = ask_ai_doctor(
        data.get("disease", ""),
        data.get("question", "")
    )
    return jsonify({"reply": reply})

# -------------------------------
# ALL DISEASES
# -------------------------------
@app.route("/all-diseases")
def all_diseases():
    df = pd.read_csv("ML/disease_info.csv")
    return jsonify({"diseases": df["disease"].dropna().tolist()})

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
