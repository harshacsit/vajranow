from ai_model import (
    load_model,
    predict_risk
)


# ============================================================
# LOAD MODEL
# ============================================================

model = load_model(
    "models/vajranow_rf.pkl"
)


# ============================================================
# DEMO ATMOSPHERIC INPUT
# ============================================================

weather = {
    "radar_reflectivity": 48,
    "lightning_activity": 17,
    "cloud_development": 72,
    "atmospheric_instability": 81
}


# ============================================================
# PREDICT
# ============================================================

probability = predict_risk(
    model,
    weather
)


risk_percent = probability * 100


# ============================================================
# RISK LEVEL
# ============================================================

if risk_percent >= 70:
    status = "SEVERE"

elif risk_percent >= 50:
    status = "WARNING"

elif risk_percent >= 30:
    status = "WATCH"

else:
    status = "LOW"


# ============================================================
# DISPLAY
# ============================================================

print()
print("===================================")
print(" VajraNow AI Prediction")
print("===================================")

print(
    f"Radar Reflectivity : "
    f"{weather['radar_reflectivity']} dBZ"
)

print(
    f"Lightning Activity : "
    f"{weather['lightning_activity']} strikes/min"
)

print(
    f"Cloud Development  : "
    f"{weather['cloud_development']}%"
)

print(
    f"Atmospheric Instability : "
    f"{weather['atmospheric_instability']}%"
)

print()
print(
    f"Thunderstorm Probability: "
    f"{risk_percent:.1f}%"
)

print(
    f"Risk Status: {status}"
)

print("===================================")