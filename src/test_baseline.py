import numpy as np

from baseline import (
    persistence_prediction,
    mean_absolute_error,
    critical_success_index
)


# ============================================================
# CREATE A SIMPLE CURRENT WEATHER FIELD
# ============================================================

current_field = np.array([
    [0.1, 0.2, 0.3, 0.1],
    [0.2, 0.8, 0.9, 0.2],
    [0.1, 0.7, 0.8, 0.1],
    [0.1, 0.2, 0.3, 0.1]
])


# ============================================================
# ACTUAL FUTURE FIELD
# ============================================================

actual_future = np.array([
    [0.1, 0.2, 0.3, 0.2],
    [0.1, 0.4, 0.7, 0.3],
    [0.1, 0.5, 0.9, 0.5],
    [0.1, 0.2, 0.4, 0.2]
])


# ============================================================
# PERSISTENCE PREDICTION
# ============================================================

prediction = persistence_prediction(
    current_field
)


# ============================================================
# CALCULATE METRICS
# ============================================================

mae = mean_absolute_error(
    prediction,
    actual_future
)


csi = critical_success_index(
    prediction,
    actual_future
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("===================================")
print(" VajraNow Persistence Baseline")
print("===================================")

print(
    f"MAE : {mae:.4f}"
)

print(
    f"CSI : {csi:.4f}"
)

print("===================================")