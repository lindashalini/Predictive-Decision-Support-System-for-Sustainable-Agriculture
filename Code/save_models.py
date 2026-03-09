"""
Helper script to save your trained ML models in the correct format.

Usage:
1. Train your models using your existing code
2. Use this script to save them in the format expected by the server

Example:
    # After training your irrigation model
    save_irrigation_model(trained_model)

    # After training your crop model
    save_crop_model(trained_model)
"""

import joblib
import os


def save_irrigation_model(model, filename='irrigation_model.pkl'):
    """
    Save the irrigation prediction model.

    Expected model input features:
        - CropDays: Number of days since crop was planted
        - SoilMoisture: Soil moisture percentage (0-100)
        - temperature: Temperature in Celsius
        - Humidity: Humidity percentage (0-100)

    Expected output:
        - Binary classification (0 = No irrigation, 1 = Irrigation needed)

    Args:
        model: Trained sklearn model
        filename: Output filename (default: 'irrigation_model.pkl')
    """
    try:
        joblib.dump(model, filename)
        print(f"✓ Irrigation model saved to {filename}")
        print(f"  Model type: {type(model).__name__}")
        print(f"  File size: {os.path.getsize(filename)} bytes")

        # Verify model can be loaded
        loaded_model = joblib.load(filename)
        print(f"✓ Model verified - successfully loaded")

        return True
    except Exception as e:
        print(f"✗ Error saving irrigation model: {e}")
        return False


def save_crop_model(model, filename='crop_model.pkl'):
    """
    Save the crop recommendation model.

    Expected model input features:
        - temperature: Temperature in Celsius
        - humidity: Humidity percentage (0-100)
        - ph: Soil pH value (typically 0-14)
        - rainfall: Rainfall in mm

    Expected output:
        - Multi-class classification (crop name)

    Args:
        model: Trained sklearn model with classes_ attribute
        filename: Output filename (default: 'crop_model.pkl')
    """
    try:
        joblib.dump(model, filename)
        print(f"✓ Crop recommendation model saved to {filename}")
        print(f"  Model type: {type(model).__name__}")
        print(f"  File size: {os.path.getsize(filename)} bytes")

        # Check if model has classes attribute
        if hasattr(model, 'classes_'):
            print(f"  Number of crop classes: {len(model.classes_)}")
            print(f"  Crop classes: {list(model.classes_)[:5]}..." if len(model.classes_) > 5 else f"  Crop classes: {list(model.classes_)}")

        # Verify model can be loaded
        loaded_model = joblib.load(filename)
        print(f"✓ Model verified - successfully loaded")

        return True
    except Exception as e:
        print(f"✗ Error saving crop model: {e}")
        return False


def verify_models():
    """
    Verify that both models exist and can be loaded.
    """
    print("\n" + "=" * 50)
    print("Verifying ML Models")
    print("=" * 50)

    irrigation_exists = os.path.exists('irrigation_model.pkl')
    crop_exists = os.path.exists('crop_model.pkl')

    if irrigation_exists:
        try:
            model = joblib.load('irrigation_model.pkl')
            print("✓ irrigation_model.pkl found and loadable")
            print(f"  Type: {type(model).__name__}")
        except Exception as e:
            print(f"✗ irrigation_model.pkl exists but cannot be loaded: {e}")
    else:
        print("✗ irrigation_model.pkl not found")

    if crop_exists:
        try:
            model = joblib.load('crop_model.pkl')
            print("✓ crop_model.pkl found and loadable")
            print(f"  Type: {type(model).__name__}")
            if hasattr(model, 'classes_'):
                print(f"  Classes: {len(model.classes_)} crops")
        except Exception as e:
            print(f"✗ crop_model.pkl exists but cannot be loaded: {e}")
    else:
        print("✗ crop_model.pkl not found")

    print("=" * 50 + "\n")

    return irrigation_exists and crop_exists


# Example usage template
if __name__ == "__main__":
    print("=" * 50)
    print("ML Model Saver for Predictive Soil System")
    print("=" * 50)
    print("\nThis is a helper script. To use it:")
    print("\n1. Train your models in your notebook/script")
    print("2. Import this module:")
    print("   from save_models import save_irrigation_model, save_crop_model")
    print("\n3. Save your models:")
    print("   save_irrigation_model(your_irrigation_model)")
    print("   save_crop_model(your_crop_model)")
    print("\nExample:")
    print("-" * 50)
    print("""
from save_models import save_irrigation_model, save_crop_model
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Train irrigation model
df = pd.read_csv('irrigation_data.csv')
X = df[['CropDays','SoilMoisture','temperature','Humidity']]
y = df['Irrigation']

irrigation_model = RandomForestClassifier(n_estimators=100)
irrigation_model.fit(X, y)

# Save it
save_irrigation_model(irrigation_model)

# Train crop model
df = pd.read_csv('crop_data.csv')
X = df[['temperature','humidity','ph','rainfall']]
y = df['label']

crop_model = RandomForestClassifier(n_estimators=100)
crop_model.fit(X, y)

# Save it
save_crop_model(crop_model)
    """)
    print("-" * 50)

    print("\nCurrently checking for existing models...\n")
    verify_models()
