from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import config
import pickle

app = Flask(__name__)

# ---------------- DB CONFIG ----------------
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

# ---------------- LOAD AI MODEL (TOP LEVEL) ----------------
yield_model = pickle.load(open('ai_models/yield_model.pkl', 'rb'))

# ---------------- HOME ----------------
@app.route('/')
def home():
    return "AgriAssist AI Backend Running Successfully"

# ---------------- ADD FARMER ----------------
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

# ---------------- VIEW FARMERS ----------------
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

# ---------------- DELETE FARMER ----------------
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

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
