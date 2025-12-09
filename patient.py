import numpy as np
import random
from vitals import Vitals
from data.afflictions import AFFLICTION_CURES, AFFLICTION_DAMAGE_RULES, AFFLICTION_ASSESSMENTS
from data.treatments import TREATMENTS

CPR_MATRIX = np.array([
    [+8, +6, +4],
    [+4, 0, +2],
    [+6, 0, 0],
    [+15, 0, 0]
], dtype=float)
CPR_SHOCKABLE_CHANCE = 0.75
CPR_FORCE_SHOCKABLE_ATTEMPTS = 2
DEFIB_HEALTH_BOOST = 45
DEFIB_BASELINE_JITTER = 3.0

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
        self.cpr_attempts = 0
        self.conscious_state = "Alert"
        self.code_requires_defib = False
        self._update_conscious_state()

    def worsen(self):
        """Apply affliction each turn."""
        if self.deceased:
            return
        if self.has_active_affliction():
            self.vitals.apply_affliction(self.affliction_matrix)
            self._apply_affliction_health_damage()
        else:
            self.vitals.natural_recovery()
            self.vitals.recover_vitals_toward_baseline()
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
        self._maybe_resolve_affliction(name)
        if not self.has_active_affliction():
            self.vitals.jitter_around_baseline()
        return None

    def is_critical(self):
        return self.vitals.is_critical()

    def check_code_status(self):
        if self.deceased:
            self.coded = True
            self.coding_reasons = ["Patient deceased"]
            self.cpr_attempts = 0
            self.code_requires_defib = False
            self._update_conscious_state()
            return True

        health_flags = self.vitals.coding_flags()
        if health_flags:
            health = self.vitals.health_value()
            if health <= 0:
                self.deceased = True
                self.vitals.mark_deceased()
                self.coded = True
                self.coding_reasons = ["Health depleted"]
                self.cpr_attempts = 0
                self.code_requires_defib = False
                self._update_conscious_state()
                return True
            self.coded = True
            self.coding_reasons = health_flags
            self.code_requires_defib = True
            self._update_conscious_state()
            return True

        if self.code_requires_defib:
            self.coded = True
            if self.shockable:
                self.coding_reasons = ["Awaiting defibrillation to terminate code"]
            else:
                self.coding_reasons = ["Continue CPR until shockable rhythm achieved"]
            self._update_conscious_state()
            return True

        self.coded = False
        self.coding_reasons = []
        self.shockable = False
        self.cpr_attempts = 0
        self.code_requires_defib = False
        self._update_conscious_state()
        return False

    def perform_cpr(self):
        if self.deceased:
            return "Patient is deceased. CPR cannot revive them."
        self.vitals.apply_treatment(CPR_MATRIX)
        self.vitals.stabilize_near_baseline(jitter=2.0)
        made_shockable = False
        if self.coded:
            self.cpr_attempts += 1
            if not self.shockable and (random.random() < CPR_SHOCKABLE_CHANCE or self.cpr_attempts >= CPR_FORCE_SHOCKABLE_ATTEMPTS):
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
        self.vitals.boost_health(DEFIB_HEALTH_BOOST)
        self.vitals.stabilize_near_baseline(jitter=DEFIB_BASELINE_JITTER)
        self.shockable = False
        self.cpr_attempts = 0
        self.code_requires_defib = False
        self.check_code_status()
        if self.coded:
            # If for some reason the patient still meets code criteria, treat as failure.
            return "Defibrillation delivered but patient is still coding."
        return "Defibrillation successful! Patient stabilized, underlying cause persists."

    def has_active_affliction(self):
        return not np.allclose(self.affliction_matrix, 0)

    def is_ready_for_discharge(self):
        return (
            not self.deceased
            and not self.coded
            and not self.has_active_affliction()
        )

    def _maybe_resolve_affliction(self, treatment_name):
        if not self.affliction_name:
            return False
        expected = AFFLICTION_CURES.get(self.affliction_name)
        if expected != treatment_name:
            return False
        resolved = self.affliction_name
        self.affliction_matrix = np.zeros_like(self.affliction_matrix)
        self.affliction_name = None
        return True

    def _apply_affliction_health_damage(self):
        if not self.affliction_name:
            return False
        rules = AFFLICTION_DAMAGE_RULES.get(self.affliction_name)
        if not rules:
            return False
        for threshold in rules.get("thresholds", []):
            measurement = self.vitals.get_measurement(threshold["vital"])
            min_ok = threshold.get("min")
            max_ok = threshold.get("max")
            if (min_ok is not None and measurement < min_ok) or (max_ok is not None and measurement > max_ok):
                self.vitals.adjust_health(-rules["health_loss"])
                return True
        return False

    def _assessment_block(self):
        profile = self._assessment_profile()
        lines = ["EMS assessment:", f"  Signs: {profile['signs']}"]
        if self.is_conscious():
            lines.append(f"  Symptoms: {profile['symptoms']}")
        else:
            lines.append("  Symptoms: unavailable (patient unconscious)")
        return "\n".join(lines)

    def _assessment_profile(self):
        if not self.affliction_name:
            return AFFLICTION_ASSESSMENTS["default"]
        return AFFLICTION_ASSESSMENTS.get(self.affliction_name, AFFLICTION_ASSESSMENTS["default"])

    def _update_conscious_state(self):
        if self.deceased:
            self.conscious_state = "Unresponsive"
            return
        if self.coded:
            self.conscious_state = "Unresponsive"
            return
        health = self.vitals.health_value()
        if health >= 80:
            self.conscious_state = "Alert"
        elif health >= 50:
            self.conscious_state = "Verbal"
        else:
            self.conscious_state = "Pain"

    def is_conscious(self):
        return self.conscious_state in ("Alert", "Verbal")

    def __str__(self):
        status = f"Patient {self.id}: {self.name}"
        if self.deceased:
            status += " [DECEASED]"
        elif self.coded:
            suffix = " [CODE - shockable]" if self.shockable else " [CODE]"
            status += suffix
        status += f" | AVPU: {self.conscious_state}"

        assessment_text = self._assessment_block()
        vitals_text = self.vitals.format(show_pain=self.is_conscious())
        if self.coded and self.coding_reasons:
            vitals_text += "\n-- CODE TRIGGERS: " + ", ".join(self.coding_reasons)

        sections = [status, assessment_text, "Vitals:", vitals_text]
        return "\n".join(sections)
