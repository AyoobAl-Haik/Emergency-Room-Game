from utils.random_generators import random_patient
from patient import Patient

class GameManager:
    def __init__(self, num_bays=4):
        from bay_manager import BayManager
        self.bays = BayManager(num_bays)
        self.waiting_list = []
        self.turn = 0
        self.morgue = []
        self.discharged = []
        self.game_over = False
        self.lose_reason = None
        self._create_initial_patient()

    def _create_initial_patient(self):
        name, base_vitals, affliction_name, aff_matrix = random_patient()
        patient = Patient(name, base_vitals=base_vitals, affliction_matrix=aff_matrix, affliction_name=affliction_name)
        self.waiting_list.append(patient)

    def process_turn(self):
        if self.game_over:
            return
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
        if self.game_over:
            return self.lose_reason or "Game already over."
        patient, error = self._patient_at_bay(bay_index)
        if error:
            return error
        if treatment_name is None:
            return "No treatment specified."
        response = patient.apply_intervention(treatment_name.strip().lower())
        return response or "Treatment completed."

    def send_to_morgue(self, bay_index):
        if self.game_over:
            return self.lose_reason or "Game already over."
        patient, error = self._patient_at_bay(bay_index)
        if error:
            return error
        if not patient.deceased:
            reason = f"Lose condition: attempted to send living patient {patient.name} to the morgue."
            self._lose(reason)
            return reason
        self.morgue.append(patient)
        self.bays.discharge_patient(bay_index)
        return f"{patient.name} transferred to the morgue."

    def discharge_patient(self, bay_index):
        if self.game_over:
            return self.lose_reason or "Game already over."
        patient, error = self._patient_at_bay(bay_index)
        if error:
            return error
        if patient.deceased:
            reason = f"Lose condition: attempted to discharge deceased patient {patient.name}."
            self._lose(reason)
            return reason
        if patient.has_active_affliction():
            reason = f"Lose condition: discharged untreated patient {patient.name}."
            self._lose(reason)
            return reason
        self.discharged.append(patient)
        self.bays.discharge_patient(bay_index)
        return f"{patient.name} successfully discharged."

    def coded_patients(self):
        all_patients = [p for p in self.waiting_list] + [p for p in self.bays.get_patients() if p]
        return [p for p in all_patients if p and (p.coded or p.deceased)]

    def _lose(self, reason):
        if not self.game_over:
            self.game_over = True
            self.lose_reason = reason

    def _patient_at_bay(self, bay_index):
        try:
            patient = self.bays.bays[bay_index]
        except IndexError:
            return None, "Invalid bay index."
        if not patient:
            return None, "No patient assigned to that bay."
        return patient, None
