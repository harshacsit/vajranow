import numpy as np


def persistence_prediction(current_field):
    """
    Persistence baseline.

    Assumption:
    The future weather field remains the same
    as the current weather field.
    """

    return current_field.copy()


def mean_absolute_error(prediction, actual):
    """
    Calculate Mean Absolute Error (MAE).
    """

    return np.mean(
        np.abs(prediction - actual)
    )


def critical_success_index(
    prediction,
    actual,
    threshold=0.5
):
    """
    Calculate Critical Success Index (CSI).

    CSI = Hits / (Hits + False Alarms + Misses)
    """

    prediction_event = prediction >= threshold
    actual_event = actual >= threshold

    hits = np.sum(
        prediction_event & actual_event
    )

    false_alarms = np.sum(
        prediction_event & ~actual_event
    )

    misses = np.sum(
        ~prediction_event & actual_event
    )

    denominator = (
        hits
        + false_alarms
        + misses
    )

    if denominator == 0:
        return 0.0

    return hits / denominator