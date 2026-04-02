"""
ULCM Integrated Scaling Model
Combines: clinical + HCD + system levers
"""

import dataclasses
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class Params:
    # Population / system level
    population: int = 10000
    reach_rate: float = 0.6
    signup_rate: float = 0.7
    attendance_rate: float = 0.8
    demand_multiplier: float = 1.0

    # Engagement
    dropout_rate: float = 0.15

    # Clinical design
    sessions: int = 2
    ingredient_effect: float = 1.15

    dose_response: dict = field(default_factory=lambda: {
        1: 0.60,
        2: 0.75,
        4: 0.90,
        6: 0.92,
    })

    # Step-care
    step_up_rate: float = 0.3
    step_effect: float = 0.25

    # Workforce
    sessions_per_hour: float = 2.0
    hours_per_worker_per_year: int = 1200

    # Costs
    cost_per_worker: float = 1500.0
    sms_cost_per_user: float = 0.5

    # System efficiency
    integration_factor: float = 1.0


class ULCMModel:

    def __init__(self, params: Params):
        self.p = params

    def demand(self):
        reachable = self.p.population * self.p.reach_rate * self.p.demand_multiplier
        signup = reachable * self.p.signup_rate
        attend = signup * self.p.attendance_rate
        return attend

    def retention(self, attend):
        return attend * (1 - self.p.dropout_rate)

    def remission_rate(self):
        base = self.p.dose_response.get(self.p.sessions, 0.75)
        adjusted = base * self.p.ingredient_effect
        return min(adjusted, 0.95)

    def first_line_outcomes(self, retained):
        rate = self.remission_rate()
        remitted = retained * rate
        non_remitters = retained - remitted
        return remitted, non_remitters

    def step_care(self, non_remitters):
        stepped = non_remitters * self.p.step_up_rate
        step_remitted = stepped * self.p.step_effect
        return step_remitted

    def workforce(self, total_sessions):
        hours_needed = total_sessions / self.p.sessions_per_hour
        workers = hours_needed / self.p.hours_per_worker_per_year
        return workers

    def cost(self, workers):
        staff_cost = workers * self.p.cost_per_worker
        sms_cost = self.p.population * self.p.sms_cost_per_user
        total_cost = (staff_cost + sms_cost) * self.p.integration_factor
        return total_cost

    def run(self):
        attend = self.demand()
        retained = self.retention(attend)

        first_remit, non_remitters = self.first_line_outcomes(retained)
        step_remit = self.step_care(non_remitters)

        total_remitted = first_remit + step_remit
        total_sessions = retained * self.p.sessions
        workers = self.workforce(total_sessions)
        total_cost = self.cost(workers)

        return {
            "population": self.p.population,
            "entered": round(attend, 1),
            "retained": round(retained, 1),
            "remitted": round(total_remitted, 1),
            "remission_rate": round(total_remitted / self.p.population, 4),
            "cost_total": round(total_cost, 2),
            "cost_per_remission": round(total_cost / max(total_remitted, 1), 2),
            "workers": round(workers, 2),
        }


_VALID_SESSIONS = {1, 2, 4, 6}


def params_from_dict(d: dict) -> Params:
    """Construct Params from a JSON-decoded dict, ignoring unknown keys."""
    valid_fields = {f.name: f for f in dataclasses.fields(Params)
                   if f.name != "dose_response"}
    kwargs = {}
    for name, fld in valid_fields.items():
        if name in d:
            raw = d[name]
            try:
                kwargs[name] = fld.type(raw) if isinstance(fld.type, type) else raw
            except (ValueError, TypeError):
                pass  # fall through to default

    # Cast known numeric types explicitly (dataclass field.type may be a string in 3.10+)
    int_fields = {"population", "sessions", "hours_per_worker_per_year"}
    float_fields = {
        "reach_rate", "signup_rate", "attendance_rate", "demand_multiplier",
        "dropout_rate", "ingredient_effect", "step_up_rate", "step_effect",
        "sessions_per_hour", "cost_per_worker", "sms_cost_per_user",
        "integration_factor",
    }
    for name in int_fields:
        if name in d:
            try:
                kwargs[name] = int(d[name])
            except (ValueError, TypeError):
                pass
    for name in float_fields:
        if name in d:
            try:
                kwargs[name] = float(d[name])
            except (ValueError, TypeError):
                pass

    # Validate sessions — clamp to nearest valid key
    if "sessions" in kwargs:
        s = kwargs["sessions"]
        if s not in _VALID_SESSIONS:
            nearest = min(_VALID_SESSIONS, key=lambda x: abs(x - s))
            kwargs["sessions"] = nearest

    return Params(**kwargs)


def run_scenarios(base: Params, param_name: str, values: list) -> pd.DataFrame:
    """Vary param_name across values with all other params held at base."""
    results = []
    for v in values:
        p = dataclasses.replace(base, **{param_name: v})
        out = ULCMModel(p).run()
        out[param_name] = v
        results.append(out)
    return pd.DataFrame(results)
