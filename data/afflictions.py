import numpy as np
AFFLICTIONS = {
    "sepsis": np.array([
        [-18, -12, -6],
        [+12, +0.8, +4],
        [-12, -1.5, +2],
        [0, 0, 0]
    ], dtype=float),
    "cardiac arrest": np.array([
        [-40, -25, -20],
        [-30, -1.5, -14],
        [-35, -3.0, +8],
        [0, 0, 0]
    ], dtype=float),
    "dehydration": np.array([
        [-12, -6, -3],
        [+8, +0.2, -4],
        [-10, -1.0, +3],
        [0, 0, 0]
    ], dtype=float),
    "external bleed": np.array([
        [-25, -18, -8],
        [+15, -0.1, +6],
        [-22, -2.5, +5],
        [0, 0, 0]
    ], dtype=float),
    "internal bleed": np.array([
        [-28, -20, -10],
        [+18, -0.1, +8],
        [-24, -3.0, +6],
        [0, 0, 0]
    ], dtype=float)
}

AFFLICTION_CURES = {
    "sepsis": "antibiotics",
    "cardiac arrest": "defibrillation",
    "dehydration": "fluids",
    "external bleed": "hemostasis",
    "internal bleed": "transfusion"
}

AFFLICTION_DAMAGE_RULES = {
    "sepsis": {
        "health_loss": 8,
        "thresholds": (
            {"vital": "temperature", "min": 35.0, "max": 39.5},
        )
    },
    "cardiac arrest": {
        "health_loss": 20,
        "thresholds": (
            {"vital": "heart_rate", "min": 60.0, "max": 100.0},
        )
    },
    "dehydration": {
        "health_loss": 5,
        "thresholds": (
            {"vital": "heart_rate", "min": 60.0, "max": 100.0},
        )
    },
    "external bleed": {
        "health_loss": 15,
        "thresholds": (
            {"vital": "heart_rate", "min": 60.0, "max": 100.0},
        )
    },
    "internal bleed": {
        "health_loss": 18,
        "thresholds": (
            {"vital": "heart_rate", "min": 60.0, "max": 100.0},
        )
    }
}
