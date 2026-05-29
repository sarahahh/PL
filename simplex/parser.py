import numpy as np


def build_problem(problem_type, objective_coeffs, constraints):

    # Función objetivo

    objective = np.array(objective_coeffs)

    # Lista de restricciones

    parsed_constraints = []

    # =====================================================
    # RECORRER CADA RESTRICCIÓN
    # =====================================================

    for constraint in constraints:

        # Organizar restricción 

        parsed_constraints.append({
            "coefficients": np.array(constraint["coeffs"]),
            "operator": constraint["operator"],
            "rhs": constraint["rhs"]  # Lado derecho de la ecuación
        })

    # =====================================================
    # RETORNAR PROBLEMA COMPLETO
    # =====================================================

    return {
        "type": problem_type,
        "objective": objective,
        "constraints": parsed_constraints
    }