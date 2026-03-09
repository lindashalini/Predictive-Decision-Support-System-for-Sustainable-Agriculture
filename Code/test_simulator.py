"""
Arduino Data Simulator for Testing

This script simulates Arduino sensor data for testing the web dashboard
without requiring actual hardware.

Usage:
    python test_simulator.py
"""

import time
import random
import sys


def generate_sensor_data():
    """Generate realistic sensor data"""
    # Simulate realistic sensor values
    soil_moisture = random.randint(30, 80)
    ph_value = round(random.uniform(5.5, 7.5), 2)
    temperature = round(random.uniform(20.0, 35.0), 1)
    humidity = round(random.uniform(40.0, 80.0), 1)
    light_raw = random.randint(20, 90)
    light_percent = int((light_raw / 90) * 100)

    return {
        'soil_moisture': soil_moisture,
        'ph_value': ph_value,
        'temperature': temperature,
        'humidity': humidity,
        'light_raw': light_raw,
        'light_percent': light_percent
    }


def simulate_arduino_output():
    """Simulate the exact output format from Arduino"""
    while True:
        data = generate_sensor_data()

        print("------ SENSOR DATA ------")
        print(f"Soil Moisture: {data['soil_moisture']} %")
        print(f"pH Value: {data['ph_value']}")
        print(f"Temperature: {data['temperature']} C")
        print(f"Humidity: {data['humidity']} %")
        print(f"Light Raw: {data['light_raw']}  Light %: {data['light_percent']}")

        if data['light_percent'] > 40:
            print("Bright Sunlight")
        else:
            print("Low Sunlight")

        if data['soil_moisture'] < 40:
            print("Soil Dry -> Pump ON")
        else:
            print("Soil Wet -> Pump OFF")

        print("--------------------------\n")
        sys.stdout.flush()

        time.sleep(3)


if __name__ == "__main__":
    print("=" * 50)
    print("Arduino Sensor Data Simulator")
    print("=" * 50)
    print("\nThis will simulate Arduino sensor output.")
    print("Connect this to server.py by creating a virtual serial port,")
    print("or use it to test the data format.\n")
    print("Press Ctrl+C to stop\n")
    print("=" * 50)
    print()

    try:
        simulate_arduino_output()
    except KeyboardInterrupt:
        print("\n\nSimulator stopped.")
        sys.exit(0)
