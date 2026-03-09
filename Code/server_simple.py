"""
Simplified server without WebSocket for troubleshooting

This version uses polling instead of WebSocket for real-time updates.
Use this if you encounter issues with the main server.py
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime
from collections import deque
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Store sensor data (keep last 100 readings)
sensor_data_buffer = deque(maxlen=100)
latest_sensor_data = {
    'soil_moisture': 0,
    'ph_value': 0,
    'temperature': 0,
    'humidity': 0,
    'light_raw': 0,
    'light_percent': 0,
    'light_status': '',
    'pump_status': '',
    'timestamp': ''
}

# Arduino serial connection
arduino = None
serial_thread = None
running = False

# ML Models
irrigation_model = None
crop_model = None

def find_arduino_port():
    """Automatically find Arduino port"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'USB' in port.description or 'ACM' in port.device:
            return port.device
    return None

def load_ml_models():
    """Load ML models if available"""
    global irrigation_model, crop_model
    try:
        irrigation_model = joblib.load('irrigation_model.pkl')
        print("✓ Irrigation model loaded")
    except Exception as e:
        print(f"⚠ Irrigation model not found: {e}")

    try:
        crop_model = joblib.load('crop_model.pkl')
        print("✓ Crop recommendation model loaded")
    except Exception as e:
        print(f"⚠ Crop recommendation model not found: {e}")

def parse_arduino_data(line):
    """Parse Arduino serial output"""
    global latest_sensor_data

    try:
        line = line.strip()

        if "Soil Moisture:" in line:
            latest_sensor_data['soil_moisture'] = int(line.split(":")[1].strip().replace("%", ""))

        elif "pH Value:" in line:
            latest_sensor_data['ph_value'] = float(line.split(":")[1].strip())

        elif "Temperature:" in line:
            latest_sensor_data['temperature'] = float(line.split(":")[1].strip().replace("C", ""))

        elif "Humidity:" in line:
            latest_sensor_data['humidity'] = float(line.split(":")[1].strip().replace("%", ""))

        elif "Light Raw:" in line:
            latest_sensor_data['light_raw'] = int(line.split(":")[1].split()[0].strip())

        elif "Light %:" in line:
            latest_sensor_data['light_percent'] = int(line.split(":")[1].strip())

        elif "Bright Sunlight" in line or "Low Sunlight" in line:
            latest_sensor_data['light_status'] = line.strip()

        elif "Pump ON" in line or "Pump OFF" in line:
            latest_sensor_data['pump_status'] = "ON" if "ON" in line else "OFF"
            latest_sensor_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Complete data point received, store it
            data_point = latest_sensor_data.copy()
            sensor_data_buffer.append(data_point)

    except Exception as e:
        print(f"Error parsing line '{line}': {e}")

def read_from_arduino():
    """Background thread to read from Arduino"""
    global arduino, running

    while running:
        try:
            if arduino and arduino.is_open:
                if arduino.in_waiting > 0:
                    line = arduino.readline().decode('utf-8', errors='ignore')
                    parse_arduino_data(line)
            else:
                time.sleep(1)
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            time.sleep(1)

def start_serial_connection(port=None):
    """Start serial connection with Arduino"""
    global arduino, serial_thread, running

    if port is None:
        port = find_arduino_port()

    if port is None:
        print("⚠ Arduino not found. Please specify port manually.")
        return False

    try:
        arduino = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)
        print(f"✓ Connected to Arduino on {port}")

        running = True
        serial_thread = threading.Thread(target=read_from_arduino, daemon=True)
        serial_thread.start()
        return True
    except Exception as e:
        print(f"✗ Failed to connect to Arduino: {e}")
        return False

# ============= API ROUTES =============

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index_simple.html')

@app.route('/api/sensor/latest')
def get_latest_sensor_data():
    """Get the latest sensor reading"""
    return jsonify(latest_sensor_data)

@app.route('/api/sensor/history')
def get_sensor_history():
    """Get historical sensor data"""
    return jsonify(list(sensor_data_buffer))

@app.route('/api/predict/irrigation', methods=['POST'])
def predict_irrigation():
    """Predict irrigation need"""
    if irrigation_model is None:
        return jsonify({'error': 'Irrigation model not loaded'}), 500

    try:
        data = request.get_json()
        crop_days = data.get('CropDays', 0)
        soil_moisture = data.get('SoilMoisture', latest_sensor_data['soil_moisture'])
        temperature = data.get('temperature', latest_sensor_data['temperature'])
        humidity = data.get('Humidity', latest_sensor_data['humidity'])

        X = np.array([[crop_days, soil_moisture, temperature, humidity]])
        prediction = irrigation_model.predict(X)[0]

        try:
            probability = irrigation_model.predict_proba(X)[0].tolist()
        except:
            probability = None

        return jsonify({
            'prediction': int(prediction),
            'irrigation_needed': bool(prediction),
            'probability': probability,
            'input_data': {
                'CropDays': crop_days,
                'SoilMoisture': soil_moisture,
                'temperature': temperature,
                'Humidity': humidity
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict/crop', methods=['POST'])
def predict_crop():
    """Predict crop recommendation"""
    if crop_model is None:
        return jsonify({'error': 'Crop recommendation model not loaded'}), 500

    try:
        data = request.get_json()
        temperature = data.get('temperature', latest_sensor_data['temperature'])
        humidity = data.get('humidity', latest_sensor_data['humidity'])
        ph = data.get('ph', latest_sensor_data['ph_value'])
        rainfall = data.get('rainfall', 0)

        X = np.array([[temperature, humidity, ph, rainfall]])
        prediction = crop_model.predict(X)[0]

        try:
            probability = crop_model.predict_proba(X)[0]
            top_3_idx = np.argsort(probability)[-3:][::-1]
            top_3_crops = [(crop_model.classes_[i], float(probability[i])) for i in top_3_idx]
        except:
            top_3_crops = None

        return jsonify({
            'prediction': str(prediction),
            'recommended_crop': str(prediction),
            'top_3_recommendations': top_3_crops,
            'input_data': {
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/arduino/status')
def arduino_status():
    """Check Arduino connection status"""
    return jsonify({
        'connected': arduino is not None and arduino.is_open if arduino else False,
        'port': arduino.port if arduino and arduino.is_open else None
    })

# ============= MAIN =============

if __name__ == '__main__':
    print("=" * 50)
    print("🌱 Predictive Soil Monitoring Server (Simple)")
    print("=" * 50)

    load_ml_models()

    print("\n📡 Searching for Arduino...")
    start_serial_connection()

    print("\n🚀 Starting web server on http://localhost:5000")
    print("=" * 50)

    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
