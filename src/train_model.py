from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from ai_model import (
    create_training_data,
    save_model
)


# ============================================================
# CREATE TRAINING DATA
# ============================================================

X, y = create_training_data(
    n_samples=2000
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# RANDOM FOREST
# ============================================================

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    random_state=42
)


# ============================================================
# TRAIN
# ============================================================

print()
print("Training VajraNow prototype AI...")

model.fit(
    X_train,
    y_train
)


# ============================================================
# EVALUATE
# ============================================================

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)


# ============================================================
# SAVE
# ============================================================

models_directory = Path("models")

models_directory.mkdir(
    exist_ok=True
)

model_path = (
    models_directory
    / "vajranow_rf.pkl"
)

save_model(
    model,
    model_path
)


print()
print("===================================")
print(" VajraNow AI Training Complete")
print("===================================")

print(
    f"Test Accuracy: {accuracy:.4f}"
)

print(
    f"Model saved to: {model_path}"
)

print("===================================")