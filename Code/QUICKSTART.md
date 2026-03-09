# Quick Start Guide

Get your Predictive Soil Monitoring System up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Prepare Your ML Models

You have two options:

### Option A: Use Your Existing Trained Models

If you already have trained models, save them using the helper script:

```python
from save_models import save_irrigation_model, save_crop_model

# Load or train your models
# irrigation_model = your_trained_irrigation_model
# crop_model = your_trained_crop_model

save_irrigation_model(irrigation_model)
save_crop_model(crop_model)
```

### Option B: Run Without Models (Testing)

You can run the server without ML models - it will still:
- Display real-time sensor data
- Show charts
- The prediction features will just show an error when used

## Step 3: Connect Your Arduino

1. Upload the Arduino sketch to your board
2. Connect via USB
3. The server will auto-detect the Arduino port

**Linux users**: You may need to add yourself to the dialout group:
```bash
sudo usermod -a -G dialout $USER
# Then log out and back in
```

## Step 4: Start the Server

```bash
python server.py
```

You should see:
```
==================================================
🌱 Predictive Soil Monitoring Server
==================================================

✓ Irrigation model loaded
✓ Crop recommendation model loaded

📡 Searching for Arduino...
✓ Connected to Arduino on /dev/ttyUSB0

🚀 Starting web server on http://localhost:5000
==================================================
```

## Step 5: Open the Dashboard

Open your browser and go to:
```
http://localhost:5000
```

You should see:
- Real-time sensor values updating
- Charts showing trends
- Green "Connected" indicator
- ML prediction forms (if models are loaded)

## Testing Without Arduino

If you don't have the Arduino connected yet, you can still test the web interface:

1. Comment out the auto-connect line in `server.py`:
```python
# start_serial_connection()  # Comment this out
```

2. Start the server - the web interface will load without real data

## Common Issues

### "Arduino not found"
- Check USB connection
- Verify Arduino sketch is uploaded
- Check cable (use data cable, not charge-only)
- Try specifying port manually in code

### "Models not loaded"
- Check that `.pkl` files are in the project directory
- Verify file permissions
- Try running `python save_models.py` to verify models

### No data in browser
- Check Arduino Serial Monitor shows data output
- Verify baud rate is 9600
- Clear browser cache and refresh
- Check browser console for errors (F12)

### Permission denied (Linux)
```bash
sudo chmod 666 /dev/ttyUSB0  # Temporary fix
# Or permanently:
sudo usermod -a -G dialout $USER
```

## Next Steps

1. **Calibrate Sensors**: Adjust calibration values in Arduino code for accuracy
2. **Tune Models**: Retrain ML models with your specific soil/crop data
3. **Customize Dashboard**: Modify `templates/index.html` to match your needs
4. **Add Features**: Extend the system with database logging, alerts, etc.

## Need Help?

- Check `README.md` for detailed documentation
- Review the API endpoints in the main README
- Check server console for error messages
- Verify Arduino Serial Monitor shows correct data format

---

**You're all set! 🚀 Happy monitoring!**
