import joblib
import numpy as np

# Load trained model
model = joblib.load("model.pkl")

# Example input:
# Fever + body pain + fatigue
test_input = np.array([[
    1,  # fever
    0,  # headache
    0,  # cough
    1,  # body_pain
    0,  # stomach_pain
    0,  # diarrhea
    0,  # vomiting
    0,  # sore_throat
    0,  # runny_nose
    0,  # chest_pain
    0,  # short_breath
    0,  # skin_rash
    0,  # itching
    0,  # acidity
    0,  # back_pain
    0,  # joint_pain
    0,  # high_bp
    0,  # low_bp
    1   # fatigue
]])

prediction = model.predict(test_input)

print("🩺 Predicted Disease:", prediction[0])
