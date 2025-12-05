import numpy as np
import random
from data.afflictions import AFFLICTIONS

NAMES = ["John", "Maria", "Ahmed", "Chen", "Grace", "Alex"]

def random_base_vitals():
    return np.array([
        [120, 80, 98],
        [75,  37,  95],
        [90,  70, 100]
    ]) + np.random.randint(-5, 5, (3,3))

def random_patient():
    name = random.choice(NAMES)
    affliction = random.choice(list(AFFLICTIONS.keys()))
    return name, AFFLICTIONS[affliction]
