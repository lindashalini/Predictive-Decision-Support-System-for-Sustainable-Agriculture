"""
Example: How to integrate your existing trained models

This shows how to train and save your models in the correct format
for the Predictive Soil Monitoring System.

Adapt this code to work with your existing datasets.
"""

from save_models import save_irrigation_model, save_crop_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np


def train_and_save_irrigation_model(data_path):
    """
    Train and save the irrigation prediction model

    Your CSV should have columns: CropDays, SoilMoisture, temperature, Humidity, Irrigation
    """
    print("\n" + "=" * 60)
    print("Training Irrigation Model")
    print("=" * 60)

    # Load your data
    df = pd.read_csv(data_path)

    # Features and target
    X = df[['CropDays', 'SoilMoisture', 'temperature', 'Humidity']]
    y = df['Irrigation']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    print(f"\nTraining on {len(X_train)} samples...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Performance:")
    print(f"  Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nFeature Importance:")
    print(feature_importance.to_string(index=False))

    # Save model
    print("\nSaving model...")
    save_irrigation_model(model)

    return model


def train_and_save_crop_model(data_path):
    """
    Train and save the crop recommendation model

    Your CSV should have columns: temperature, humidity, ph, rainfall, label
    """
    print("\n" + "=" * 60)
    print("Training Crop Recommendation Model")
    print("=" * 60)

    # Load your data
    df = pd.read_csv(data_path)

    # Features and target
    X = df[['temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    print(f"\nTraining on {len(X_train)} samples...")
    print(f"Number of crop classes: {len(y.unique())}")

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Performance:")
    print(f"  Accuracy: {accuracy:.2%}")
    print(f"\nTop 10 crops in dataset:")
    print(y.value_counts().head(10))

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nFeature Importance:")
    print(feature_importance.to_string(index=False))

    # Save model
    print("\nSaving model...")
    save_crop_model(model)

    return model


def load_and_test_models():
    """
    Load saved models and test with sample data
    """
    import joblib

    print("\n" + "=" * 60)
    print("Testing Saved Models")
    print("=" * 60)

    try:
        # Load models
        irrigation_model = joblib.load('irrigation_model.pkl')
        crop_model = joblib.load('crop_model.pkl')

        print("✓ Both models loaded successfully\n")

        # Test irrigation model
        print("Testing Irrigation Model:")
        test_irrigation = np.array([[30, 35, 28.5, 65]])  # CropDays, SoilMoisture, temp, humidity
        irrigation_pred = irrigation_model.predict(test_irrigation)
        print(f"  Input: CropDays=30, SoilMoisture=35%, Temp=28.5°C, Humidity=65%")
        print(f"  Prediction: {'Irrigation Needed' if irrigation_pred[0] else 'No Irrigation Needed'}")

        # Test crop model
        print("\nTesting Crop Recommendation Model:")
        test_crop = np.array([[28.5, 65, 6.8, 100]])  # temp, humidity, ph, rainfall
        crop_pred = crop_model.predict(test_crop)
        print(f"  Input: Temp=28.5°C, Humidity=65%, pH=6.8, Rainfall=100mm")
        print(f"  Recommended Crop: {crop_pred[0]}")

        # Get top 3 recommendations if model supports probability
        if hasattr(crop_model, 'predict_proba'):
            proba = crop_model.predict_proba(test_crop)[0]
            top_3_idx = np.argsort(proba)[-3:][::-1]
            print("\n  Top 3 Recommendations:")
            for i, idx in enumerate(top_3_idx, 1):
                print(f"    {i}. {crop_model.classes_[idx]}: {proba[idx]:.1%}")

        print("\n✓ All tests passed!")

    except FileNotFoundError as e:
        print(f"✗ Model file not found: {e}")
    except Exception as e:
        print(f"✗ Error testing models: {e}")


# ============= USAGE EXAMPLES =============

if __name__ == "__main__":
    print("=" * 60)
    print("ML Model Integration Example")
    print("=" * 60)

    print("\n📌 To use this script:")
    print("\n1. Uncomment the training functions below")
    print("2. Replace 'your_irrigation_data.csv' with your actual file path")
    print("3. Replace 'your_crop_data.csv' with your actual file path")
    print("4. Run this script to train and save models")

    print("\n" + "=" * 60)
    print("Option 1: If you have the data files")
    print("=" * 60)
    print("""
# Uncomment these lines and add your file paths:

# irrigation_model = train_and_save_irrigation_model('your_irrigation_data.csv')
# crop_model = train_and_save_crop_model('your_crop_data.csv')
# load_and_test_models()
    """)

    print("\n" + "=" * 60)
    print("Option 2: If you already have trained models")
    print("=" * 60)
    print("""
# If you already trained models in another script:

from save_models import save_irrigation_model, save_crop_model

# Your existing code to load/train models
# irrigation_model = your_existing_irrigation_model
# crop_model = your_existing_crop_model

# Just save them:
save_irrigation_model(irrigation_model)
save_crop_model(crop_model)
    """)

    print("\n" + "=" * 60)
    print("Option 3: Test existing saved models")
    print("=" * 60)

    # This will work if models are already saved
    try:
        load_and_test_models()
    except:
        print("\n⚠ No saved models found. Train and save models first.")
        print("   Follow Option 1 or Option 2 above.")
