import numpy as np
from data.afflictions import AFFLICTIONS

def _opposite(affliction_name):
    return np.negative(AFFLICTIONS[affliction_name])

TREATMENTS = {
    "antibiotics": _opposite("sepsis"),
    "defibrillation": _opposite("cardiac arrest"),
    "fluids": _opposite("dehydration"),
    "hemostasis": _opposite("external bleed"),
    "transfusion": _opposite("internal bleed")
}
