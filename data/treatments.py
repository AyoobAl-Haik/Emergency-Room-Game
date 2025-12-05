import numpy as np

TREATMENTS = {
    "fluids": np.array([
        [+20, +12, +4],
        [-10, -0.3, -2],
        [+15, +1.0, -2],
        [+8, 0, 0]
    ], dtype=float),
    "antibiotics": np.array([
        [+12, +8, +6],
        [-6, -0.4, -3],
        [+10, +0.8, -2],
        [+6, 0, 0]
    ], dtype=float),
    "defibrillation": np.array([
        [+35, +24, +18],
        [+30, +0.2, +12],
        [+28, +2.0, -5],
        [+20, 0, 0]
    ], dtype=float),
    "transfusion": np.array([
        [+30, +20, +5],
        [-12, -0.2, -3],
        [+24, +2.5, -2],
        [+15, 0, 0]
    ], dtype=float)
}
