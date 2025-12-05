import numpy as np
from vitals import Vitals

class Patient:
    _id_counter = 1

    def __init__(self, name, base_vitals, affliction_matrix):
        self.id = Patient._id_counter
        Patient._id_counter += 1

        self.name = name
        self.vitals = Vitals(base_vitals)
        self.affliction_matrix = np.array(affliction_matrix)

    def worsen(self):
        """Apply affliction each turn."""
        self.vitals.apply_affliction(self.affliction_matrix)

    def treat(self, treatment_matrix):
        self.vitals.apply_treatment(treatment_matrix)

    def is_critical(self):
        return self.vitals.is_critical()

    def __str__(self):
        return f"Patient {self.id}: {self.name}\nVitals:\n{self.vitals}"
