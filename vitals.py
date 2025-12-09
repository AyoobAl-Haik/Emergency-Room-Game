import numpy as np

class Vitals:
    MATRIX_SHAPE = (4, 3)
    _HEALTH_INDEX = (3, 0)
    _HEART_RATE_INDEX = (1, 0)
    _TEMPERATURE_INDEX = (1, 1)
    _PAIN_SCORE_INDEX = (2, 2)
    CODE_HEALTH_THRESHOLD = 30
    MAX_HEALTH = 120
    BASE_HEALTH = 100
    HEART_RATE_MAX = 220
    PAIN_MAX = 10
    NATURAL_RECOVERY_STEP = 4
    DEFAULT_BASELINE = np.array([
        [120, 80, 98],
        [78, 37.0, 16],
        [90, 4.5, 1],
        [BASE_HEALTH, 0, 0]
    ], dtype=float)
    _JITTER_SCALE = np.array([
        [5, 3, 1],
        [4, 0.3, 2],
        [5, 0.5, 2]
    ], dtype=float)

    def __init__(self, matrix=None):
        self.deceased = False
        self.matrix = self._coerce_matrix(matrix)
        self.baseline = np.array(self.DEFAULT_BASELINE, copy=True)

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

    _MEASUREMENT_KEYS = {
        "heart_rate": _HEART_RATE_INDEX,
        "temperature": _TEMPERATURE_INDEX,
        "pain_score": _PAIN_SCORE_INDEX,
    }

    def _coerce_matrix(self, matrix):
        base = np.array(self.DEFAULT_BASELINE, copy=True)
        if matrix is None:
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
        hr_row, hr_col = self._HEART_RATE_INDEX
        matrix[hr_row, hr_col] = min(matrix[hr_row, hr_col], self.HEART_RATE_MAX)
        ps_row, ps_col = self._PAIN_SCORE_INDEX
        matrix[ps_row, ps_col] = min(matrix[ps_row, ps_col], self.PAIN_MAX)
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
        self._clamp_vitals()

    def recover_vitals_toward_baseline(self, step=3):
        if self.deceased:
            return
        diff = self.baseline[:3, :3] - self.matrix[:3, :3]
        adjustments = np.clip(diff, -step, step)
        self.matrix[:3, :3] = self.matrix[:3, :3] + adjustments
        self._clamp_vitals()

    def jitter_around_baseline(self):
        if self.deceased:
            return
        noise = np.random.uniform(-1.0, 1.0, size=(3, 3)) * self._JITTER_SCALE
        targets = self.baseline[:3, :3] + noise
        self.matrix[:3, :3] = 0.5 * (self.matrix[:3, :3] + targets)
        self._clamp_vitals()

    def stabilize_near_baseline(self, jitter=2.5):
        if self.deceased:
            return
        noise = np.random.uniform(-jitter, jitter, size=(3, 3))
        self.matrix[:3, :3] = self.baseline[:3, :3] + noise
        self._clamp_vitals()

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

    def format(self, show_pain=True):
        if self.deceased:
            return "Vitals unavailable (patient deceased)"

        if self.matrix.shape == self.MATRIX_SHAPE:
            lines = []
            for row_labels, row_vals in zip(self._LABELS, self.matrix):
                for label, value in zip(row_labels, row_vals):
                    if label is None:
                        continue
                    if label == "pain score" and not show_pain:
                        display = "unavailable (patient unconscious)"
                    else:
                        display = self._format_value(label, value)
                    lines.append(f"{label}: {display}")
            return "\n".join(lines)

        # Fallback to raw matrix representation if shape is unexpected.
        return str(self.matrix)

    def __str__(self):
        return self.format(show_pain=True)

    def _format_value(self, label, value):
        numeric = float(value)
        if label == "pain score":
            bounded = min(max(numeric, 0.0), self.PAIN_MAX)
            return str(int(round(bounded)))
        rounded = round(numeric, 1)
        if rounded.is_integer():
            return str(int(rounded))
        return f"{rounded:.1f}"

    def adjust_health(self, delta):
        if self.deceased:
            return
        row, col = self._HEALTH_INDEX
        self.matrix[row, col] = np.clip(self.matrix[row, col] + delta, 0, self.MAX_HEALTH)

    def boost_health(self, amount):
        self.adjust_health(amount)

    def get_measurement(self, key):
        row, col = self._MEASUREMENT_KEYS[key]
        return float(self.matrix[row, col])
