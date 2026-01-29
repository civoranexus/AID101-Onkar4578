from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import config
import pickle
from ai_models.irrigation_model import recommend_irrigation
from ai_models.fertilizer_model import recommend_fertilizer
from ai_models.market_model import market_advisory




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

@app.route('/fertilizer-advice', methods=['POST'])
def fertilizer_advice():
    data = request.get_json()

    soil_type = data['soil_type']
    crop_stage = data['crop_stage']
    nitrogen = data['nitrogen']
    phosphorus = data['phosphorus']
    potassium = data['potassium']

    result = recommend_fertilizer(
        soil_type,
        crop_stage,
        nitrogen,
        phosphorus,
        potassium
    )

    return jsonify(result)

def generate_alert(task_type, message):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO farm_tasks (task_type, description) VALUES (%s, %s)",
        (task_type, message)
    )
    mysql.connection.commit()
    cur.close()

@app.route('/create-alert', methods=['POST'])
def create_alert():
    data = request.get_json()
    task_type = data['task_type']
    message = data['message']

    generate_alert(task_type, message)

    return jsonify({"status": "Alert created successfully"})

@app.route('/tasks', methods=['GET'])
def view_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM farm_tasks")
    data = cur.fetchall()
    cur.close()

    tasks = []
    for row in data:
        tasks.append({
            "id": row[0],
            "task_type": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": row[4]
        })

    return jsonify(tasks)

@app.route('/update-task/<int:id>', methods=['PUT'])
def update_task(id):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE farm_tasks SET status='COMPLETED' WHERE id=%s",
        [id]
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "Task marked as completed"})

@app.route('/market-insight', methods=['POST'])
def market_insight():
    data = request.get_json()

    current_price = data['current_price']
    avg_price = data['avg_price']
    demand_index = data['demand_index']

    result = market_advisory(
        current_price,
        avg_price,
        demand_index
    )

    return jsonify(result)




# RUN SERVER 
if __name__ == "__main__":
    app.run(debug=True)
