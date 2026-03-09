"""
API Testing Script

Test the server API endpoints without using the web interface.
Useful for debugging and automation.

Usage:
    python test_api.py
"""

import requests
import json
import time


BASE_URL = "http://localhost:5000"


def test_arduino_status():
    """Test Arduino connection status"""
    print("\n" + "=" * 50)
    print("Testing Arduino Status")
    print("=" * 50)

    try:
        response = requests.get(f"{BASE_URL}/api/arduino/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_latest_sensor_data():
    """Test getting latest sensor data"""
    print("\n" + "=" * 50)
    print("Testing Latest Sensor Data")
    print("=" * 50)

    try:
        response = requests.get(f"{BASE_URL}/api/sensor/latest")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")

        # Print in readable format
        if data:
            print("\nSensor Readings:")
            print(f"  Soil Moisture: {data.get('soil_moisture', 'N/A')}%")
            print(f"  pH Value: {data.get('ph_value', 'N/A')}")
            print(f"  Temperature: {data.get('temperature', 'N/A')}°C")
            print(f"  Humidity: {data.get('humidity', 'N/A')}%")
            print(f"  Light: {data.get('light_percent', 'N/A')}%")
            print(f"  Pump: {data.get('pump_status', 'N/A')}")

        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_sensor_history():
    """Test getting sensor history"""
    print("\n" + "=" * 50)
    print("Testing Sensor History")
    print("=" * 50)

    try:
        response = requests.get(f"{BASE_URL}/api/sensor/history")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Number of data points: {len(data)}")

        if data:
            print(f"\nLatest reading:")
            print(json.dumps(data[-1], indent=2))

        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_irrigation_prediction():
    """Test irrigation prediction"""
    print("\n" + "=" * 50)
    print("Testing Irrigation Prediction")
    print("=" * 50)

    payload = {
        "CropDays": 30,
        "SoilMoisture": 35,
        "temperature": 28.5,
        "Humidity": 65
    }

    print(f"Input: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(
            f"{BASE_URL}/api/predict/irrigation",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_crop_prediction():
    """Test crop recommendation"""
    print("\n" + "=" * 50)
    print("Testing Crop Recommendation")
    print("=" * 50)

    payload = {
        "temperature": 28.5,
        "humidity": 65,
        "ph": 6.8,
        "rainfall": 100
    }

    print(f"Input: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(
            f"{BASE_URL}/api/predict/crop",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_all_tests():
    """Run all API tests"""
    print("\n" + "=" * 60)
    print(" API Testing Suite - Predictive Soil Monitoring System")
    print("=" * 60)
    print(f"\nServer: {BASE_URL}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Check if server is running
    try:
        requests.get(BASE_URL, timeout=2)
    except:
        print("\n❌ ERROR: Server is not running!")
        print("Please start the server with: python server.py")
        return

    results = {}

    # Run tests
    results['Arduino Status'] = test_arduino_status()
    time.sleep(0.5)

    results['Latest Sensor Data'] = test_latest_sensor_data()
    time.sleep(0.5)

    results['Sensor History'] = test_sensor_history()
    time.sleep(0.5)

    results['Irrigation Prediction'] = test_irrigation_prediction()
    time.sleep(0.5)

    results['Crop Prediction'] = test_crop_prediction()

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")

    passed_count = sum(results.values())
    total_count = len(results)

    print("\n" + "=" * 60)
    print(f"Results: {passed_count}/{total_count} tests passed")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()
