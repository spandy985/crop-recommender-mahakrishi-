from flask import Flask, request, jsonify, render_template
import requests
import joblib

# Initialize Flask app
app = Flask(__name__)

# OpenWeather API key
OPENWEATHER_API_KEY = "8309fcb8b95494c5b9bc81eda528ae31"

# Load trained ML model and label encoder
model = joblib.load("crop_model.pkl")
le = joblib.load("label_encoder.pkl")

# Home route: renders the HTML form
@app.route("/")
def home():
    return render_template("index.html")

# Recommendation API route
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json  # Get JSON data sent from frontend

    # Extract soil nutrients and optional pH
    nitrogen = float(data.get("N", 0))
    phosphorus = float(data.get("P", 0))
    potassium = float(data.get("K", 0))
    pH = float(data.get("pH", 6.5))  # default pH if not provided

    # Extract latitude & longitude
    lat = data.get("Latitude")
    lon = data.get("Longitude")

    # Set default weather values
    temperature = 25
    humidity = 50
    rainfall = 0
    city_name = "Unknown"

    # Fetch live weather if geolocation is available
    if lat and lon:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = requests.get(weather_url).json()
        if res.get("main"):
            temperature = res["main"]["temp"]
            humidity = res["main"]["humidity"]
            rainfall = res.get("rain", {}).get("1h", 0)
            city_name = res.get("name", "Unknown")

    # Prepare features in the same order as training
    features = [[nitrogen, phosphorus, potassium, pH, rainfall, temperature]]

    # Predict crop using trained ML model
    pred_index = model.predict(features)[0]
    recommendation = le.inverse_transform([pred_index])[0]

    # Return JSON response to frontend
    return jsonify({
        "inputs": {
            "N": nitrogen,
            "P": phosphorus,
            "K": potassium,
            "pH": pH,
            "Latitude": lat,
            "Longitude": lon
        },
        "location": city_name,
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        },
        "recommendation": recommendation
    })

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
