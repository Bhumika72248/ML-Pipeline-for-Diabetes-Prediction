import numpy as np


ZERO_SENSITIVE_COLUMNS = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI"
]


def replace_zero_with_nan(data):

    data = data.copy()

    for column in ZERO_SENSITIVE_COLUMNS:

        if column in data.columns:
            data[column] = data[column].replace(
                0,
                np.nan
            )

    return data