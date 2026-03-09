# 🌱 Predictive Soil Monitoring System

A real-time IoT soil monitoring system that integrates Arduino sensors with Machine Learning predictions for smart agriculture.

## Features

- **Real-time Sensor Monitoring**: Live data from Arduino sensors
  - Soil Moisture
  - pH Value
  - Temperature & Humidity (DHT11)
  - Light Intensity (LDR)
  - Pump Status

- **Interactive Dashboard**: Beautiful web interface with:
  - Real-time sensor value displays
  - Dynamic charts showing sensor trends over time
  - Responsive design with Bootstrap

- **Machine Learning Predictions**:
  - **Irrigation Prediction**: Determines if irrigation is needed
  - **Crop Recommendation**: Suggests best crops for current conditions

- **Live Updates**: WebSocket-based real-time data streaming

## System Architecture

```
Arduino (Sensors) → USB Serial → Python Server → WebSocket → Web Dashboard
                                      ↓
                                  ML Models
```

## Installation

### 1. Hardware Setup

Upload the Arduino code to your board with the following sensors:
- Soil Moisture Sensor (A1)
- pH Sensor (A0)
- DHT11 Temperature/Humidity (Pin 2)
- LDR Light Sensor (A2)
- Relay Module for Pump (Pin 7)

### 2. Python Environment Setup

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Prepare ML Models

You need to save your trained ML models as `.pkl` files in the project directory:

#### Irrigation Model
```python
import joblib
from sklearn.ensemble import RandomForestClassifier

# Train your model
# X = df[['CropDays','SoilMoisture','temperature','Humidity']]
# y = df['Irrigation']
# model = RandomForestClassifier()
# model.fit(X, y)

# Save model
joblib.dump(model, 'irrigation_model.pkl')
```

#### Crop Recommendation Model
```python
import joblib
from sklearn.ensemble import RandomForestClassifier

# Train your model
# X = df[['temperature','humidity','ph','rainfall']]
# y = df['label']
# model = RandomForestClassifier()
# model.fit(X, y)

# Save model
joblib.dump(model, 'crop_model.pkl')
```

### 4. Connect Arduino

- Connect your Arduino via USB
- The server will automatically detect the Arduino port
- If auto-detection fails, you can manually specify the port in the code

## Running the System

### Start the Server

```bash
python server.py
```

The server will:
1. Load ML models (if available)
2. Scan for and connect to Arduino
3. Start the web server on `http://localhost:5000`

### Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

You should see:
- Real-time sensor readings updating every 3 seconds
- Live charts showing data trends
- ML prediction forms

## API Endpoints

### Sensor Data

- `GET /api/sensor/latest` - Get the latest sensor reading
- `GET /api/sensor/history` - Get historical sensor data (last 100 readings)

### ML Predictions

#### Irrigation Prediction
```bash
POST /api/predict/irrigation
Content-Type: application/json

{
  "CropDays": 30,
  "SoilMoisture": 45,
  "temperature": 28.5,
  "Humidity": 65
}
```

#### Crop Recommendation
```bash
POST /api/predict/crop
Content-Type: application/json

{
  "temperature": 28.5,
  "humidity": 65,
  "ph": 6.8,
  "rainfall": 100
}
```

### Arduino Connection

- `GET /api/arduino/status` - Check Arduino connection status
- `POST /api/arduino/connect` - Manually connect to Arduino port

## WebSocket Events

The server uses Socket.IO for real-time updates:

- **Client → Server**:
  - `connect` - Client connected
  - `request_data` - Request latest sensor data

- **Server → Client**:
  - `sensor_update` - New sensor data available (auto-sent every reading)

## Project Structure

```
predictive-soil/
├── server.py              # Main Flask server with serial & ML integration
├── templates/
│   └── index.html         # Web dashboard frontend
├── requirements.txt       # Python dependencies
├── irrigation_model.pkl   # Irrigation prediction model (you need to add this)
├── crop_model.pkl         # Crop recommendation model (you need to add this)
└── README.md             # This file
```

## Troubleshooting

### Arduino Not Detected

1. Check USB connection
2. Verify Arduino is running the correct sketch
3. Check serial port permissions (Linux):
   ```bash
   sudo usermod -a -G dialout $USER
   # Log out and back in
   ```
4. Manually specify port in server code or via API

### ML Models Not Loading

- Ensure `.pkl` files are in the same directory as `server.py`
- Verify models were trained with scikit-learn
- Check model compatibility with installed scikit-learn version

### No Data Updates

- Check Arduino serial monitor to verify data output
- Ensure Arduino baud rate is 9600
- Check browser console for WebSocket errors

## Customization

### Adjust Chart Data Points

In `templates/index.html`, modify:
```javascript
const maxDataPoints = 20; // Change this value
```

### Change Update Frequency

In Arduino code:
```cpp
delay(3000); // Change delay (milliseconds)
```

### Modify Sensor Thresholds

In Arduino code, adjust calibration values:
```cpp
int DRY_SOIL = 900;
int WET_SOIL = 300;
float PH_NEUTRAL_VOLTAGE = 2.5;
```

## Future Enhancements

- [ ] Database integration for long-term data storage
- [ ] Email/SMS alerts for critical conditions
- [ ] Weather API integration
- [ ] Mobile app version
- [ ] Multi-farm support
- [ ] Historical data analysis and reporting

## License

MIT License - Feel free to use and modify for your projects!

## Support

For issues or questions, please open an issue on the project repository.

---

**Happy Farming! 🌾**
