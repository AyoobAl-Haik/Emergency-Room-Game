import numpy as np

class Vitals:
    def __init__(self, matrix=None):
        self.matrix = np.array(matrix) if matrix is not None else np.zeros((3,3))

    def apply_affliction(self, affliction_matrix):
        self.matrix = self.matrix + affliction_matrix  # affliction_matrix is negative

    def apply_treatment(self, treatment_matrix):
        self.matrix = self.matrix + treatment_matrix  # treatment_matrix is positive

    def is_critical(self, threshold=-10):
        return np.any(self.matrix < threshold)

    def __str__(self):
        return str(self.matrix)
