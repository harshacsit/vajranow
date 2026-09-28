import numpy as np


def shift_field(field, shift_y, shift_x):
    """
    Move a 2D weather field according to
    estimated motion.

    shift_y = vertical movement
    shift_x = horizontal movement
    """

    result = np.zeros_like(field)

    height, width = field.shape

    for y in range(height):

        for x in range(width):

            new_y = y + shift_y
            new_x = x + shift_x

            if (
                0 <= new_y < height
                and 0 <= new_x < width
            ):
                result[new_y, new_x] = field[y, x]

    return result


def optical_flow_prediction(
    current_field,
    velocity_y,
    velocity_x,
    steps
):
    """
    Predict a future weather field by moving
    the current field according to estimated velocity.
    """

    predicted = current_field.copy()

    total_shift_y = int(
        velocity_y * steps
    )

    total_shift_x = int(
        velocity_x * steps
    )

    predicted = shift_field(
        predicted,
        total_shift_y,
        total_shift_x
    )

    return predicted