import numpy as np

from baseline import (
    persistence_prediction,
    mean_absolute_error,
    critical_success_index
)

from optical_flow import (
    optical_flow_prediction
)


def compare_models(
    current_field,
    actual_future,
    velocity_y=0,
    velocity_x=1,
    steps=2
):
    """
    Compare Persistence and Optical Flow
    on the same future weather field.
    """

    # -------------------------------
    # Persistence prediction
    # -------------------------------

    persistence = persistence_prediction(
        current_field
    )

    persistence_mae = mean_absolute_error(
        persistence,
        actual_future
    )

    persistence_csi = critical_success_index(
        persistence,
        actual_future
    )

    # -------------------------------
    # Optical Flow prediction
    # -------------------------------

    optical_flow = optical_flow_prediction(
        current_field,
        velocity_y,
        velocity_x,
        steps
    )

    optical_mae = mean_absolute_error(
        optical_flow,
        actual_future
    )

    optical_csi = critical_success_index(
        optical_flow,
        actual_future
    )

    # -------------------------------
    # Return results
    # -------------------------------

    return {
        "Persistence": {
            "MAE": persistence_mae,
            "CSI": persistence_csi
        },

        "Optical Flow": {
            "MAE": optical_mae,
            "CSI": optical_csi
        }
    }