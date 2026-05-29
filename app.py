import streamlit as st

from ui.input_ui import render_input_ui
from ui.simplex_ui import show_simplex_iterations
from ui.graphical_ui import show_graphical_solution

from simplex.parser import build_problem
from simplex.tableau_builder import build_initial_tableau
from simplex.simplex_solver import SimplexSolver
from simplex.graphical_method import solve_graphical_method

# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Progrmación Lineal",
    layout="wide"
)

# Título principal y descripción

st.title("Programación Lineal")

st.write("Proyecto de Optimización")
st.write(
    "Ingrese un problema de Programación Lineal"
)

# =========================================================
# INTERFAZ DE ENTRADA
# =========================================================

problem_data = render_input_ui()

# ====================================
# PROCESAR EL PROBLEMA
# ====================================

if problem_data:

    # Construir el problema

    parsed_problem = build_problem(
        problem_data["type"],
        problem_data["objective"],
        problem_data["constraints"]
    )

    #====================================================
    # CREAR EL TABULADO SIMPLEX INICIAL
    # =====================================================
    
    tableau_data = build_initial_tableau(parsed_problem)

    # =====================================================
    # CREAR EL SOLUCIONADOR SIMPLEX
    # =====================================================

    solver = SimplexSolver(
        tableau=tableau_data["tableau"],
        variable_names=tableau_data["variable_names"],
        problem_type=parsed_problem["type"]
    )

    result = solver.solve()

    # =====================================================
    # MOSTRAR ITERACIONES DEL SIMPLEX
    # =====================================================

    show_simplex_iterations(
        result=result,
        problem_data=parsed_problem,
        num_variables=len(problem_data["objective"])
    )

    # =====================================================
    # MÉTODO GRÁFICO (SOLO 2 VARIABLES)
    # =====================================================

    if len(problem_data["objective"]) == 2:

        # Resuelve el problema gráficamente

        graphical_result = solve_graphical_method(
            objective=parsed_problem["objective"],
            constraints=parsed_problem["constraints"],
            problem_type=parsed_problem["type"]
        )

        show_graphical_solution(
            graphical_result,
            parsed_problem
        )