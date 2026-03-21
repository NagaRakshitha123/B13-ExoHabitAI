import numpy as np

REQUIRED_FIELDS = [
    "radius",
    "mass",
    "temperature",
    "distance"
]

def validate_input(data):

    if not data:
        return False, None

    for field in REQUIRED_FIELDS:
        if field not in data:
            return False, None

    try:
        features = np.array([[
            float(data["radius"]),
            float(data["mass"]),
            float(data["temperature"]),
            float(data["distance"])
        ]])

        return True, features

    except:
        return False, None