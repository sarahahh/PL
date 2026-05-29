import numpy as np


BIG_M = 1000000

# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def build_initial_tableau(problem_data):

    # Extraer datos del problema

    constraints = problem_data["constraints"]
    objective = problem_data["objective"]
    problem_type = problem_data["type"]

    # Contar variables originales

    num_original_variables = len(objective)

    tableau_rows = []
    variable_names = []

    # Variables originales

    for i in range(num_original_variables):
        variable_names.append(f"X{i + 1}")

    slack_count = 0
    excess_count = 0
    artificial_count = 0

    artificial_variables = []

    # ====================================
    # CONSTRUIR RESTRICCIONES
    # ====================================

    for row_index, constraint in enumerate(constraints):

        # Copiar coeficientes de la restricción

        row = list(constraint["coefficients"])

        # Expandir filas anteriores

        current_size = len(variable_names)

        while len(row) < current_size:
            row.append(0)

        operator = constraint["operator"]

        # =========================
        # RESTRICCIÓN <=
        # =========================

        if operator == "<=":

            slack_count += 1

            variable_names.append(f"S{slack_count}")

            for previous_row in tableau_rows:
                previous_row.append(0)

            row.append(1)

        # =========================
        # RESTRICCIÓN >=
        # =========================

        elif operator == ">=":

            # =============================================
            # VARIABLE DE EXCESO
            # =============================================

            excess_count += 1

            variable_names.append(f"E{excess_count}")

            for previous_row in tableau_rows:
                previous_row.append(0)

            row.append(-1)

            # =============================================
            # VARIABLE ARTIFICIAL
            # =============================================

            artificial_count += 1

            artificial_name = f"A{artificial_count}"

            variable_names.append(artificial_name)

            artificial_variables.append(artificial_name)

            for previous_row in tableau_rows:
                previous_row.append(0)

            row.append(1)

        # =========================
        # RESTRICCIÓN =
        # =========================

        elif operator == "=":

            artificial_count += 1

            artificial_name = f"A{artificial_count}"

            variable_names.append(artificial_name)

            artificial_variables.append(artificial_name)

            for previous_row in tableau_rows:
                previous_row.append(0)

            row.append(1)

        # Completar longitud

        while len(row) < len(variable_names):
            row.append(0)

        # Agregar lado derecho de la restricción

        row.append(constraint["rhs"])

        tableau_rows.append(row)

    # ====================================
    # FUNCIÓN OBJETIVO
    # ====================================

    z_row = []

    for i, variable in enumerate(variable_names):

        # =================================================
        # VARIABLES ORIGINALES
        # =================================================

        if variable.startswith("X"):

            coefficient = objective[i]

            if problem_type.lower() == "maximizar":

                z_row.append(-coefficient)

            else:

                z_row.append(coefficient)

        # =================================================
        # VARIABLES ARTIFICIALES
        # =================================================

        elif variable.startswith("A"):

            # Penalización Big M
            if problem_type.lower() == "maximizar":
                z_row.append(-BIG_M)
            else:
                z_row.append(BIG_M)

        # =================================================
        # VARIABLES HOLGURA / EXCESO
        # =================================================

        else:
            z_row.append(0)

    z_row.append(0)

    tableau_rows.append(z_row)

    tableau = np.array(tableau_rows, dtype=float)

    # ====================================
    # AJUSTE DE GRAN M
    # ====================================

    if len(artificial_variables) > 0:

        for row_index in range(len(constraints)):

            for col_index, variable in enumerate(variable_names):

                if variable in artificial_variables:

                    if tableau[row_index, col_index] == 1:

                        if problem_type.lower() == "maximizar":

                            tableau[-1] -= BIG_M * tableau[row_index]

                        else:

                            tableau[-1] += BIG_M * tableau[row_index]
    
    # =====================================================
    # RETORNAR RESULTADOS
    # =====================================================
    
    return {
        "tableau": tableau,
        "variable_names": variable_names,
        "artificial_variables": artificial_variables
    }