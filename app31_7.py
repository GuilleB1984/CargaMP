import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde cualquier origen

# Ruta a la base de datos SQLite
db_path = os.path.join(os.path.dirname(__file__), 'cargaProduccion.db')

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS production (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 startHour INTEGER NOT NULL,
                 startMinute INTEGER NOT NULL,
                 endHour INTEGER NOT NULL,
                 endMinute INTEGER NOT NULL,
                 event TEXT NOT NULL,
                 quantity INTEGER NOT NULL,
                 boxNumber INTEGER NOT NULL,
                 operator TEXT NOT NULL,
                 article TEXT NOT NULL,
                 material TEXT NOT NULL,
                 color TEXT NOT NULL,
                 observations TEXT NOT NULL,
                 cycle TEXT NOT NULL,
                 mouths TEXT NOT NULL,
                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    start_hour = int(data['startHour'])
    start_minute = int(data['startMinute'])
    end_hour = int(data['endHour'])
    end_minute = int(data['endMinute'])
    event = data['event']
    quantity = int(data['quantity'])
    box_number = int(data['boxNumber'])
    operator = data['operator']
    article = data['article']
    material = data['material']
    color = data['color']
    observations = data['observations']
    cycle = data['cycle']
    mouths = data['mouths']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''INSERT INTO production
                 (startHour, startMinute, endHour, endMinute, event, quantity, boxNumber, operator, article, material, color, observations, cycle, mouths)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (start_hour, start_minute, end_hour, end_minute, event, quantity, box_number, operator, article, material, color, observations, cycle, mouths))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Registro agregado correctamente'}), 200

@app.route('/get_data')
def get_data():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''SELECT * FROM production ORDER BY timestamp DESC''')
    data = c.fetchall()
    conn.close()

    records = []
    for row in data:
        record = {
            'id': row[0],
            'startHour': row[1],
            'startMinute': row[2],
            'endHour': row[3],
            'endMinute': row[4],
            'event': row[5],
            'quantity': row[6],
            'timestamp': row[15],  # Se utiliza el último elemento de la tupla, que es el timestamp.
            'boxNumber': row[7],
            'operator': row[8],
            'article': row[9],
            'material': row[10],
            'color': row[11],
            'observations': row[12],
            'cycle': row[13],
            'mouths': row[14],
        }
        records.append(record)

    return jsonify(records), 200

if __name__ == '__main__':
    app.run()
