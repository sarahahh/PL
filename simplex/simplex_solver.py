import numpy as np

class SimplexSolver:

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(
        self,
        tableau,
        variable_names,
        problem_type="maximizar"
    ):
        
        # Guardar datos y numero de restricciones y variables

        self.tableau = tableau
        self.variable_names = variable_names
        self.problem_type = problem_type.lower()

        self.num_constraints = tableau.shape[0] - 1

        self.num_variables = len(
            [v for v in variable_names if v.startswith("X")]
        )

        self.basic_variables = []

        num_rows = self.num_constraints

        for row in range(num_rows):

            basic_var = "?"

            for col in range(self.tableau.shape[1] - 1):

                column = self.tableau[:num_rows, col]

                ones = np.isclose(column, 1)
                zeros = np.isclose(column, 0)

                if (
                    np.sum(ones) == 1
                    and np.sum(zeros) == num_rows - 1
                    and ones[row]
                ):

                    basic_var = self.variable_names[col]
                    break

            self.basic_variables.append(basic_var)

    # =====================================================
    # OBTENER NOMBRE DE VARIABLE
    # =====================================================

    def get_variable_name(self, column_index):

        return self.variable_names[column_index]
    
    # =====================================================
    # VERIFICAR OPTIMALIDAD
    # =====================================================

    def is_optimal(self):

        last_row = self.tableau[-1, :-1]

        # =================================================
        # MAXIMIZACIÓN
        # =================================================

        if self.problem_type == "maximizar":

            return np.all(last_row >= 0)
        
        # =================================================
        # MINIMIZACIÓN
        # =================================================

        else:

            return np.all(last_row <= 0)

    # =====================================================
    # SELECCIONAR VARIABLE ENTRANTE
    # =====================================================

    def get_pivot_column(self):

        last_row = self.tableau[-1, :-1]

        # =================================================
        # MAXIMIZACIÓN
        # =================================================

        if self.problem_type == "maximizar":

            return int(np.argmin(last_row))
        
        # =================================================
        # MINIMIZACIÓN
        # =================================================

        else:

            return int(np.argmax(last_row))
    
    # =====================================================
    # SELECCIONAR VARIABLE SALIENTE
    # =====================================================

    def get_pivot_row(self, pivot_col):

        ratios = []

        for i in range(self.num_constraints):

            element = self.tableau[i, pivot_col]

            if element > 0:
                ratio = self.tableau[i, -1] / element
            else:
                ratio = np.inf

            ratios.append(ratio)

        if all(np.isinf(r) for r in ratios):
            raise Exception(
                "El problema es no acotado."
            )

        return int(np.argmin(ratios))

    # =====================================================
    # CALCULAR TODAS LAS RAZONES
    # =====================================================

    def get_ratios(self, pivot_col):

        ratios = []

        for i in range(self.num_constraints):

            element = self.tableau[i, pivot_col]

            # =============================================
            # CALCULAR RAZÓN
            # =============================================

            if element > 0:
                ratio = self.tableau[i, -1] / element
            else:
                ratio = np.inf

            ratios.append(ratio)

        return ratios

    # =====================================================
    # PIVOTEO
    # =====================================================

    def pivot(self, pivot_row, pivot_col):

        pivot_element = self.tableau[pivot_row, pivot_col]

        # Convertir el pivote en 1

        self.tableau[pivot_row] = (
            self.tableau[pivot_row] / pivot_element
        )

        # Convertir en 0 los demás elementos de la columna pivote

        for i in range(len(self.tableau)):

            if i != pivot_row:

                factor = self.tableau[i, pivot_col]

                self.tableau[i] = (
                    self.tableau[i]
                    - factor * self.tableau[pivot_row]
                )

    # =====================================================
    # EJECUTAR MÉTODO SIMPLEX
    # =====================================================

    def solve(self):

        iterations = []

        # Guardar el tablero inicial

        iterations.append({
            "iteration": 0,
            "tableau": self.tableau.copy(),
            "basic_variables": self.basic_variables.copy(),
            "basic_variables_before": self.basic_variables.copy(),
            "entering_variable": None,
            "leaving_variable": None,
            "pivot_element": None,
            "ratios": None,
            "message": (
                "Tableau inicial. Se revisa la fila Z para buscar coeficientes negativos. "
                "Si existen coeficientes negativos, la solución aún no es óptima."
            )
        })

        # =================================================
        # ITERACIONES SIMPLEX
        # =================================================

        while not self.is_optimal():

            pivot_col = self.get_pivot_column()

            pivot_row = self.get_pivot_row(pivot_col)

            ratios = self.get_ratios(pivot_col)

            entering_variable = self.get_variable_name(pivot_col)
            leaving_variable = self.basic_variables[pivot_row]
            pivot_element = self.tableau[pivot_row, pivot_col]

            basic_variables_before = self.basic_variables.copy()

            self.basic_variables[pivot_row] = entering_variable

            self.pivot(pivot_row, pivot_col)

            # Guardamos cada tablero después del pivoteo

            iterations.append({
                "iteration": len(iterations),
                "tableau": self.tableau.copy(),
                "basic_variables": self.basic_variables.copy(),
                "basic_variables_before": basic_variables_before,
                "entering_variable": entering_variable,
                "leaving_variable": leaving_variable,
                "pivot_element": pivot_element,
                "ratios": ratios,
                "message": (
                    f"Entra {entering_variable}, sale {leaving_variable}. "
                    f"El elemento pivote es {pivot_element:.4f}."
                )
            })

        real_variables = [
            v for v in self.variable_names
            if v.startswith("X")
        ]
        solution = np.zeros(len(real_variables))

        for row_index, variable_name in enumerate(self.basic_variables):

            if variable_name.startswith("X"):

                variable_index = int(variable_name[1:]) - 1

                solution[variable_index] = self.tableau[row_index, -1]

        # =================================================
        # VALOR ÓPTIMO
        # =================================================

        optimal_value = self.tableau[-1, -1]

        if optimal_value < 0:   
            optimal_value *= -1

        # =================================================
        # RETORNAR RESULTADOS
        # =================================================

        return {
            "solution": solution,
            "optimal_value": optimal_value,
            "tableau": self.tableau,
            "iterations": iterations,
            "basic_variables": self.basic_variables,
            "variable_names": self.variable_names
        }