import pickle
import numpy as np


FEATURE_NAMES = [
    "radar_reflectivity",
    "lightning_activity",
    "cloud_development",
    "atmospheric_instability"
]


def create_training_data(
    n_samples=2000,
    random_state=42
):
    """
    Create synthetic prototype training data.

    NOTE:
    This is only for the prototype.
    Real radar/satellite/lightning/NWP data
    will replace this later.
    """

    rng = np.random.default_rng(random_state)

    radar = rng.uniform(0, 80, n_samples)
    lightning = rng.uniform(0, 40, n_samples)
    cloud = rng.uniform(0, 100, n_samples)
    instability = rng.uniform(0, 100, n_samples)

    X = np.column_stack([
        radar,
        lightning,
        cloud,
        instability
    ])

    # Prototype event-generation rule
    score = (
        radar / 80 * 0.30
        + lightning / 40 * 0.25
        + cloud / 100 * 0.20
        + instability / 100 * 0.25
    )

    y = (
        score >= 0.50
    ).astype(int)

    return X, y


def save_model(model, path):
    """
    Save trained model.
    """

    with open(path, "wb") as file:
        pickle.dump(model, file)


def load_model(path):
    """
    Load trained model.
    """

    with open(path, "rb") as file:
        return pickle.load(file)


def predict_risk(model, values):
    """
    Predict thunderstorm probability.
    """

    X = np.array([[
        values["radar_reflectivity"],
        values["lightning_activity"],
        values["cloud_development"],
        values["atmospheric_instability"]
    ]])

    probability = model.predict_proba(X)[0][1]

    return probability