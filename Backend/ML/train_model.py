import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("symptoms_dataset.csv")

# Split input and output
X = data.drop("disease", axis=1)
y = data["disease"]

# Create model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train model on FULL dataset
model.fit(X, y)

print("✅ Model trained successfully on full dataset")

# Save model
joblib.dump(model, "model.pkl")
print("💾 Model saved as model.pkl")
