import numpy as np

TREATMENTS = {
    "fluids": np.array([
        [+1, 0, +1],
        [0, +1, 0],
        [+1, 0, +1]
    ]),
    "antibiotics": np.array([
        [+2, +1, 0],
        [+1, +2, +1],
        [0, +1, +2]
    ]),
    "defibrillation": np.array([
        [+3, +3, +2],
        [+3, +4, +3],
        [+2, +3, +4]
    ])
}
