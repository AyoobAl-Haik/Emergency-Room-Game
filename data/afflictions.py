import numpy as np
AFFLICTIONS = {
    "sepsis": np.array([
        [-18, -12, -6],
        [+12, +0.8, +4],
        [-12, -1.5, +2],
        [-8, 0, 0]
    ], dtype=float),
    "cardiac arrest": np.array([
        [-40, -25, -20],
        [-30, -5.0, -14],
        [-35, -3.0, +8],
        [-20, 0, 0]
    ], dtype=float),
    "dehydration": np.array([
        [-12, -6, -3],
        [+8, +0.5, -4],
        [-10, -1.0, +3],
        [-5, 0, 0]
    ], dtype=float),
    "external bleed": np.array([
        [-25, -18, -8],
        [+15, -0.2, +6],
        [-22, -2.5, +5],
        [-15, 0, 0]
    ], dtype=float),
    "internal bleed": np.array([
        [-28, -20, -10],
        [+18, -0.3, +8],
        [-24, -3.0, +6],
        [-18, 0, 0]
    ], dtype=float)
}

AFFLICTION_CURES = {
    "sepsis": "antibiotics",
    "cardiac arrest": "defibrillation",
    "dehydration": "fluids",
    "external bleed": "hemostasis",
    "internal bleed": "transfusion"
}
