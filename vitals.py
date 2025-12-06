import numpy as np

class Vitals:
    MATRIX_SHAPE = (4, 3)
    _HEALTH_INDEX = (3, 0)
    CODE_HEALTH_THRESHOLD = 30
    MAX_HEALTH = 120
    BASE_HEALTH = 100
    NATURAL_RECOVERY_STEP = 4

    def __init__(self, matrix=None):
        self.deceased = False
        self.matrix = self._coerce_matrix(matrix)

    # Label grid corresponds to the vitals matrix positions. Health row is hidden.
    _LABELS = [
        ["blood pressure systolic", "blood pressure diastolic", "oxygen saturation"],
        ["heart rate", "temperature", "respiratory rate"],
        ["mean arterial pressure", "perfusion index", "pain score"],
        [None, None, None]
    ]

    _MIN_VALUES = np.array([
        [0, 0, 0],          # BP systolic/diastolic, oxygen saturation
        [0, 25, 0],         # heart rate, temperature (C), respiratory rate
        [0, 0, 0],          # mean arterial pressure, perfusion index, pain score
        [0, 0, 0]
    ], dtype=float)

    def _coerce_matrix(self, matrix):
        base = np.zeros(self.MATRIX_SHAPE, dtype=float)
        if matrix is None:
            base[self._HEALTH_INDEX] = self.BASE_HEALTH
            return base
        incoming = np.array(matrix, dtype=float)
        rows = min(incoming.shape[0], self.MATRIX_SHAPE[0])
        cols = min(incoming.shape[1], self.MATRIX_SHAPE[1])
        base[:rows, :cols] = incoming[:rows, :cols]
        self._clamp_vitals(base)
        return base

    def _clamp_health(self, target=None):
        matrix = target if target is not None else self.matrix
        health = matrix[self._HEALTH_INDEX]
        matrix[self._HEALTH_INDEX] = np.clip(health, 0, self.MAX_HEALTH)

    def _clamp_vitals(self, target=None):
        matrix = target if target is not None else self.matrix
        np.maximum(matrix, self._MIN_VALUES, out=matrix)
        self._clamp_health(matrix)

    def apply_affliction(self, affliction_matrix):
        if self.deceased:
            return
        self.matrix = self.matrix + affliction_matrix
        self._clamp_vitals()

    def apply_treatment(self, treatment_matrix):
        if self.deceased:
            return
        self.matrix = self.matrix + treatment_matrix
        self._clamp_vitals()

    def mark_deceased(self):
        self.deceased = True
        self.matrix = np.zeros(self.MATRIX_SHAPE, dtype=float)

    def health_value(self):
        return float(self.matrix[self._HEALTH_INDEX])

    def natural_recovery(self, amount=NATURAL_RECOVERY_STEP):
        if self.deceased:
            return
        row, col = self._HEALTH_INDEX
        target = min(self.BASE_HEALTH, self.matrix[row, col] + amount)
        self.matrix[row, col] = min(self.MAX_HEALTH, target)

    def is_critical(self, threshold=-10):
        return np.any(self.matrix[:3, :3] < threshold)

    def coding_flags(self):
        if self.deceased:
            return ["health depleted"]
        health = self.health_value()
        if health <= 0:
            return ["health at 0"]
        if health <= self.CODE_HEALTH_THRESHOLD:
            return [f"health below {self.CODE_HEALTH_THRESHOLD}"]
        return []

    def is_coding(self):
        return bool(self.coding_flags())

    def __str__(self):
        if self.deceased:
            return "Vitals unavailable (patient deceased)"

        if self.matrix.shape == self.MATRIX_SHAPE:
            lines = []
            for row_labels, row_vals in zip(self._LABELS, self.matrix):
                for label, value in zip(row_labels, row_vals):
                    if label is None:
                        continue
                    lines.append(f"{label}: {value}")
            return "\n".join(lines)

        # Fallback to raw matrix representation if shape is unexpected.
        return str(self.matrix)
