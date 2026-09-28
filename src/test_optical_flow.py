import numpy as np

from optical_flow import optical_flow_prediction


# ============================================================
# CURRENT STORM FIELD
# ============================================================

current_field = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])


# ============================================================
# STORM MOVEMENT
# ============================================================

velocity_y = 0
velocity_x = 1


# ============================================================
# PREDICT FUTURE
# ============================================================

prediction = optical_flow_prediction(
    current_field,
    velocity_y,
    velocity_x,
    steps=2
)


# ============================================================
# DISPLAY
# ============================================================

print()
print("===================================")
print(" VajraNow Optical Flow Baseline")
print("===================================")

print()
print("Current Storm:")
print(current_field)

print()
print("Predicted Storm:")
print(prediction)

print("===================================")