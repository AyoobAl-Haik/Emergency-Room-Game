import numpy as np
import random
from vitals import Vitals
from data.treatments import TREATMENTS

CPR_MATRIX = np.array([
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [+5, 0, 0]
], dtype=float)
CPR_SHOCKABLE_CHANCE = 0.45

class Patient:
    _id_counter = 1

    def __init__(self, name, base_vitals, affliction_matrix, affliction_name=None):
        self.id = Patient._id_counter
        Patient._id_counter += 1

        self.name = name
        self.affliction_name = affliction_name
        self.vitals = Vitals(base_vitals)
        self.affliction_matrix = np.array(affliction_matrix, dtype=float)
        self.coded = False
        self.deceased = False
        self.coding_reasons = []
        self.shockable = False

    def worsen(self):
        """Apply affliction each turn."""
        if self.deceased:
            return
        self.vitals.apply_affliction(self.affliction_matrix)
        self.check_code_status()

    def treat(self, treatment_matrix):
        if self.deceased:
            return False
        self.vitals.apply_treatment(treatment_matrix)
        self.check_code_status()
        return True

    def apply_intervention(self, name):
        if name == "cpr":
            return self.perform_cpr()
        if name == "defibrillation":
            return self.perform_defibrillation()
        matrix = TREATMENTS.get(name)
        if matrix is None:
            return f"Unknown treatment '{name}'."
        if not self.treat(matrix):
            return "Patient is deceased. Treatment ineffective."
        return f"{name.title()} administered to {self.name}."

    def is_critical(self):
        return self.vitals.is_critical()

    def check_code_status(self):
        if self.deceased:
            self.coded = True
            self.coding_reasons = ["Patient deceased"]
            return True

        health_flags = self.vitals.coding_flags()
        if health_flags:
            health = self.vitals.health_value()
            if health <= 0:
                self.deceased = True
                self.vitals.mark_deceased()
                self.coded = True
                self.coding_reasons = ["Health depleted"]
                return True
            self.coded = True
            self.coding_reasons = health_flags
            return True

        self.coded = False
        self.coding_reasons = []
        self.shockable = False
        return False

    def perform_cpr(self):
        if self.deceased:
            return "Patient is deceased. CPR cannot revive them."
        self.vitals.apply_treatment(CPR_MATRIX)
        made_shockable = False
        if self.coded and not self.shockable and random.random() < CPR_SHOCKABLE_CHANCE:
            self.shockable = True
            made_shockable = True
        self.check_code_status()
        if made_shockable:
            return "CPR performed. Shockable rhythm achieved!"
        if self.coded:
            return "CPR performed but rhythm remains non-shockable."
        return "CPR performed and patient stabilized."

    def perform_defibrillation(self):
        if self.deceased:
            return "Patient is deceased. Defibrillation is futile."
        if not self.coded:
            return "Patient has a pulse. Defibrillation not indicated."
        if not self.shockable:
            return "No shockable rhythm. Perform CPR first."
        self.vitals.apply_treatment(TREATMENTS["defibrillation"])
        self.shockable = False
        self.check_code_status()
        if not self.coded:
            return "Defibrillation successful!"
        return "Defibrillation delivered but patient is still coding."

    def __str__(self):
        status = f"Patient {self.id}: {self.name}"
        if self.affliction_name:
            status += f" (affliction: {self.affliction_name})"
        if self.deceased:
            status += " [DECEASED]"
        elif self.coded:
            suffix = " [CODE - shockable]" if self.shockable else " [CODE]"
            status += suffix
        vitals_text = str(self.vitals)
        if self.coded and self.coding_reasons:
            vitals_text += "\n-- CODE TRIGGERS: " + ", ".join(self.coding_reasons)
        return f"{status}\nVitals:\n{vitals_text}"
