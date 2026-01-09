from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

@app.route('/')
def home():
    return "AgriAssist AI Backend Running Successfully"

@app.route('/add-farmer', methods=['POST'])
def add_farmer():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO farmers_profile(name, location, soil_type) VALUES(%s,%s,%s)",
        (data['name'], data['location'], data['soil_type'])
    )
    mysql.connection.commit()
    return jsonify({"message": "Farmer added successfully"})

if __name__ == "__main__":
    app.run(debug=True)
