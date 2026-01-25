from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import config
import pickle
from ai_models.irrigation_model import recommend_irrigation


app = Flask(__name__)

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

yield_model = pickle.load(open('ai_models/yield_model.pkl', 'rb'))

@app.route('/')
def home():
    return "AgriAssist AI Backend Running Successfully"

@app.route('/add-farmer', methods=['POST'])
def add_farmer():
    data = request.get_json()

    name = data['name']
    location = data['location']
    soil_type = data['soil_type']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO farmers_profile (name, location, soil_type) VALUES (%s,%s,%s)",
        (name, location, soil_type)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "Farmer Added Successfully"})

@app.route('/farmers', methods=['GET'])
def get_farmers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM farmers_profile")
    rows = cur.fetchall()
    cur.close()

    farmers = []
    for row in rows:
        farmers.append({
            "id": row[0],
            "name": row[1],
            "location": row[2],
            "soil_type": row[3]
        })

    return jsonify(farmers)


@app.route('/delete-farmer/<int:id>', methods=['DELETE'])
def delete_farmer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM farmers_profile WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "Farmer Deleted Successfully"})

# ---------------- YIELD PREDICTION ----------------
@app.route('/predict-yield', methods=['POST'])
def predict_yield():
    data = request.json

    try:
        rainfall = float(data['rainfall'])
        temperature = float(data['temperature'])
        soil_quality = float(data['soil_quality'])
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid or missing input"}), 400

    prediction = yield_model.predict([[rainfall, temperature, soil_quality]])

    return jsonify({
        "predicted_yield_kg_per_acre": round(prediction[0], 2),
        "explanation": "Prediction based on rainfall, temperature, and soil quality"
    })

@app.route('/irrigation-advice', methods=['POST'])
def irrigation_advice():
    data = request.get_json()

    rainfall = data['rainfall']
    temperature = data['temperature']
    soil_moisture = data['soil_moisture']
    crop_stage = data['crop_stage']

    result = recommend_irrigation(
        rainfall,
        temperature,
        soil_moisture,
        crop_stage
    )

    return jsonify(result)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
