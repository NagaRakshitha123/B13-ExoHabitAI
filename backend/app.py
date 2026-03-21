from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
import os

from utils import validate_input

app = Flask(__name__)

# ===============================
# LOAD ML MODEL
# ===============================
model_path = "../models/random_forest.pkl"
model = joblib.load(model_path)
print("Model loaded successfully")


# ===============================
# HOME ROUTE (FRONTEND)
# ===============================
@app.route("/")
def home():
    return render_template("index.html")


# ===============================
# PREDICTION API
# ===============================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        valid, result = validate_input(data)

        if not valid:
            return jsonify({
                "status": "error",
                "message": "Invalid input data"
            }), 400

        features = result

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        return jsonify({
            "status": "success",
            "prediction": int(prediction),
            "habitability_score": float(probability)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# ===============================
# RANK MULTIPLE PLANETS API
# ===============================
@app.route("/rank", methods=["POST"])
def rank():
    try:
        data = request.json

        if "planets" not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'planets' list"
            }), 400

        planets = data["planets"]
        results = []

        for planet in planets:
            valid, features = validate_input(planet)

            if not valid:
                continue

            score = model.predict_proba(features)[0][1]

            planet_result = planet.copy()
            planet_result["habitability_score"] = float(score)

            results.append(planet_result)

        ranked = sorted(
            results,
            key=lambda x: x["habitability_score"],
            reverse=True
        )

        return jsonify({
            "status": "success",
            "ranked_planets": ranked
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)