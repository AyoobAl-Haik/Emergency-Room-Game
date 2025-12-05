import numpy as np
AFFLICTIONS = {
    "sepsis": np.array([
        [-2, -1, 0],
        [-1, -2, -1],
        [0, -1, -2]
    ]),
    "cardiac arrest": np.array([
        [-3, -3, -2],
        [-3, -4, -3],
        [-2, -3, -4]
    ]),
    "dehydration": np.array([
        [-1, 0, -1],
        [0, -1, 0],
        [-1, 0, -1]
    ])
}
