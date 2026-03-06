import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np


# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("heavy_metals_data.csv")


# -----------------------------
# HMPI Calculation Function
# -----------------------------
def calculate_hmpi(row):
    return (
        (row["Ni"] / 0.02) +
        (row["Zn"] / 3) +
        (row["Pb"] / 0.01) +
        (row["Cd"] / 0.003) +
        (row["Cr"] / 0.05)
    ) * 100


df["HMPI"] = df.apply(calculate_hmpi, axis=1)


# -----------------------------
# Features and Target
# -----------------------------
X = df[["Ni", "Zn", "Pb", "Cd", "Cr"]]
y = df["HMPI"]


# -----------------------------
# Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -----------------------------
# Train Random Forest Model
# -----------------------------
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# -----------------------------
# Model Accuracy
# -----------------------------
predictions = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("Model RMSE:", rmse)


# -----------------------------
# Prediction Function
# -----------------------------
def predict_hmpi(ni, zn, pb, cd, cr):

    input_data = pd.DataFrame({
        "Ni": [ni],
        "Zn": [zn],
        "Pb": [pb],
        "Cd": [cd],
        "Cr": [cr]
    })

    predicted_hmpi = model.predict(input_data)

    return predicted_hmpi[0]


# -----------------------------
# Risk Prediction Function
# -----------------------------
def predict_risk(hmpi):

    if hmpi < 50:
        return "Safe"
    elif hmpi < 100:
        return "Moderate"
    elif hmpi < 200:
        return "High"
    else:
        return "Critical"