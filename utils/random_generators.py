import numpy as np
import random
from data.afflictions import AFFLICTIONS

NAMES = ["John", "Maria", "Ahmed", "Chen", "Grace", "Alex", "Priya", "Luis", "Aisha", "Noah"]

def random_base_vitals():
    # Generate a realistic baseline for each vital sign plus hidden health.
    return np.array([
        [np.random.randint(110, 131), np.random.randint(70, 86), np.random.randint(96, 100)],  # BP systolic/diastolic, SpO2
        [np.random.randint(70, 101), round(np.random.uniform(36.5, 37.8), 1), np.random.randint(12, 21)],  # HR, temp (C), RR
        [np.random.randint(75, 96), round(np.random.uniform(3.0, 6.5), 1), np.random.randint(0, 4)],  # MAP, perfusion index, pain score
        [100, 0, 0]  # overall health stored but not displayed
    ], dtype=float)

def random_patient():
    name = random.choice(NAMES)
    base_vitals = random_base_vitals()
    affliction = random.choice(list(AFFLICTIONS.keys()))
    return name, base_vitals, affliction, AFFLICTIONS[affliction]
