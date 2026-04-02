# =========================================
# ULCM FULL SYSTEM MODEL (HCD + PHASE DATA)
# =========================================

import numpy as np


class ULCMModel:

    def __init__(self, params):
        self.p = params

    # -------------------------------------
    # DOSE RESPONSE (Phase 2 + 3)
    # -------------------------------------
    def dose_effect(self, sessions):
        if sessions == 1:
            return 0.75
        elif sessions == 2:
            return 0.90
        elif sessions <= 4:
            return 1.0
        else:
            return 1.05

    # -------------------------------------
    # ACTIVE INGREDIENT EFFECT
    # -------------------------------------
    def ingredient_effect(self, ingredient):
        return {
            "psychoeducation": 1.2,
            "problem_solving": 1.15,
            "peer_support": 0.8
        }.get(ingredient, 1.0)

    # -------------------------------------
    # HCD ENTRY MODEL (CRITICAL ADDITION)
    # -------------------------------------
    def entry_model(self, population):
        p = self.p

        # No screening → higher reach
        reached = population * p["reach_rate"]

        # Reduced stigma → higher sign-up
        signup = reached * p["signup_rate"]

        # Drop-in attendance
        attend_session1 = signup * p["attendance_rate"]

        return attend_session1

    # -------------------------------------
    # ENGAGEMENT MODEL (HCD)
    # -------------------------------------
    def engagement_model(self, participants):
        p = self.p

        # SMS engagement boosts retention
        retention = participants * (1 - p["dropout_rate"])

        return retention

    # -------------------------------------
    # TRIAGE MODEL (HCD + STEP CARE)
    # -------------------------------------
    def triage_model(self, participants):
        p = self.p

        # Severity split (can be tuned)
        mild = participants * p["mild_share"]
        moderate = participants * p["moderate_share"]
        severe = participants * p["severe_share"]

        return mild, moderate, severe

    # -------------------------------------
    # CORE SIMULATION
    # -------------------------------------
    def simulate(self, population):

        p = self.p

        # -----------------------------
        # 1. ENTRY (HCD)
        # -----------------------------
        session1 = self.entry_model(population)

        # -----------------------------
        # 2. ENGAGEMENT
        # -----------------------------
        retained = self.engagement_model(session1)

        # -----------------------------
        # 3. TRIAGE
        # -----------------------------
        mild, moderate, severe = self.triage_model(retained)

        # -----------------------------
        # 4. FIRST LINE (SSI)
        # -----------------------------
        dose_eff = self.dose_effect(p["sessions"])
        ingredient_eff = self.ingredient_effect(p["ingredient"])

        remission_first = (
            retained *
            p["base_remission"] *
            dose_eff *
            ingredient_eff
        )

        # -----------------------------
        # 5. STEP CARE
        # -----------------------------
        non_responders = retained - remission_first

        escalated = non_responders * p["step_up_rate"]

        remission_step = escalated * p["step_remission"]

        total_remitted = remission_first + remission_step

        # -----------------------------
        # 6. WORKFORCE
        # -----------------------------
        total_sessions = (
            retained * p["sessions"] +
            escalated * p["step_sessions"]
        )

        sessions_per_worker = (
            p["hours_per_week"] *
            p["weeks_per_year"] *
            p["sessions_per_hour"]
        )

        workers_needed = total_sessions / sessions_per_worker

        # -----------------------------
        # 7. COST MODEL (UPDATED WITH HCD)
        # -----------------------------

        # Removed costs
        screening_cost = population * p["screening_cost_per_user"]

        # Added SMS layer
        sms_cost = population * p["sms_cost_per_user"]

        worker_cost = workers_needed * p["cost_per_worker"]
        supervision_cost = workers_needed * p["supervision_cost"]

        total_cost = (
            worker_cost +
            supervision_cost +
            sms_cost
            # NOTE: screening removed → cost saving
        )

        cost_per_user = total_cost / population
        cost_per_remission = total_cost / max(total_remitted, 1)

        # -----------------------------
        # OUTPUT
        # -----------------------------
        return {
            "population": population,
            "entered_system": session1,
            "retained": retained,
            "mild": mild,
            "moderate": moderate,
            "severe": severe,
            "remitted": total_remitted,
            "remission_rate": total_remitted / population,
            "workers_needed": workers_needed,
            "total_cost": total_cost,
            "cost_per_user": cost_per_user,
            "cost_per_remission": cost_per_remission
        }


# =========================================
# PARAMETERS (FULL SYSTEM)
# =========================================

default_params = {

    # HCD ENTRY
    "reach_rate": 0.6,
    "signup_rate": 0.7,
    "attendance_rate": 0.75,

    # Engagement
    "dropout_rate": 0.25,

    # Clinical
    "base_remission": 0.35,
    "step_remission": 0.6,

    # Intervention
    "sessions": 1,
    "step_sessions": 6,
    "ingredient": "problem_solving",

    # Step care
    "step_up_rate": 0.4,

    # Severity split
    "mild_share": 0.5,
    "moderate_share": 0.3,
    "severe_share": 0.2,

    # Workforce
    "hours_per_week": 20,
    "weeks_per_year": 48,
    "sessions_per_hour": 2,

    # Costs
    "cost_per_worker": 1200,
    "supervision_cost": 200,
    "sms_cost_per_user": 0.05,
    "screening_cost_per_user": 1.0  # removed in new model
}


# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    model = ULCMModel(default_params)

    results = model.simulate(population=10000)

    for k, v in results.items():
        print(f"{k}: {round(v, 2)}")
