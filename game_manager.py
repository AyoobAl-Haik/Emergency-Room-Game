from utils.random_generators import random_patient
from patient import Patient

class GameManager:
    def __init__(self, num_bays=4):
        from bay_manager import BayManager
        self.bays = BayManager(num_bays)
        self.waiting_list = []
        self.turn = 0
        self._create_initial_patient()

    def _create_initial_patient(self):
        name, base_vitals, affliction_name, aff_matrix = random_patient()
        patient = Patient(name, base_vitals=base_vitals, affliction_matrix=aff_matrix, affliction_name=affliction_name)
        self.waiting_list.append(patient)

    def process_turn(self):
        self.turn += 1

        # worsen all patients and check for codes
        for patient in self.waiting_list:
            patient.worsen()
            patient.check_code_status()
        for patient in self.bays.get_patients():
            if patient:
                patient.worsen()
                patient.check_code_status()

    def apply_treatment(self, bay_index, treatment_name):
        try:
            patient = self.bays.bays[bay_index]
        except IndexError:
            return "Invalid bay index."
        if not patient:
            return "No patient assigned to that bay."
        if treatment_name is None:
            return "No treatment specified."
        response = patient.apply_intervention(treatment_name.strip().lower())
        return response or "Treatment completed."

    def coded_patients(self):
        all_patients = [p for p in self.waiting_list] + [p for p in self.bays.get_patients() if p]
        return [p for p in all_patients if p and (p.coded or p.deceased)]
