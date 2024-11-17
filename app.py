from flask import Flask, request, jsonify
from config import Config

app = Flask(__name__)

# Endpoint untuk mendapatkan semua data
@app.route('/data', methods=['GET'])
def get_data():
    try:
        connection = Config.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sensor_data")
        result = cursor.fetchall()
        data = [{'id': row[0], 'name': row[1], 'value': row[2]} for row in result]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint untuk menambahkan data
@app.route('/data', methods=['POST'])
def add_data():
    try:
        name = request.json.get('name')
        value = request.json.get('value')
        connection = Config.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO sensor_data (name, value) VALUES (%s, %s)", (name, value))
        connection.commit()
        return jsonify({"message": "Data added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Endpoint untuk mengupdate data
@app.route('/data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    try:
        name = request.json.get('name')
        value = request.json.get('value')
        connection = Config.get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE sensor_data SET name=%s, value=%s WHERE id=%s", (name, value, data_id))
        connection.commit()
        return jsonify({"message": "Data updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
