class BayManager:
    def __init__(self, num_bays):
        self.bays = [None] * num_bays

    def assign_patient(self, patient, index):
        if self.bays[index] is None:
            self.bays[index] = patient
            return True
        return False

    def discharge_patient(self, index):
        self.bays[index] = None

    def get_patients(self):
        return self.bays
