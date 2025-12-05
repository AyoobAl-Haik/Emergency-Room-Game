from utils.random_generators import random_patient
from patient import Patient
from data.treatments import TREATMENTS

class GameManager:
    def __init__(self, num_bays=4):
        from bay_manager import BayManager
        self.bays = BayManager(num_bays)
        self.waiting_list = []
        self.turn = 0

    def new_patient_arrival(self):
        name, aff_matrix = random_patient()
        p = Patient(name, base_vitals=None, affliction_matrix=aff_matrix)
        self.waiting_list.append(p)

    def process_turn(self):
        self.turn += 1
        self.new_patient_arrival()

        # worsen all patients
        for patient in self.waiting_list:
            patient.worsen()
        for patient in self.bays.get_patients():
            if patient:
                patient.worsen()

    def apply_treatment(self, bay_index, treatment_name):
        patient = self.bays.bays[bay_index]
        if patient:
            patient.treat(TREATMENTS[treatment_name])

    def check_for_critical(self):
        all_patients = [p for p in self.waiting_list] + [p for p in self.bays.get_patients() if p]
        return [p for p in all_patients if p.is_critical()]
