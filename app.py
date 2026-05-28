import streamlit as st

from ui.input_ui import render_input_ui
from ui.simplex_ui import show_simplex_iterations
from ui.graphical_ui import show_graphical_solution

from simplex.parser import build_problem
from simplex.simplex_solver import SimplexSolver
from simplex.graphical_method import solve_graphical_method

# Configuración de la página
st.set_page_config(
    page_title="Progrmación Lineal",
    layout="wide"
)

# Título principal
st.title("Programación Lineal")

st.write("Proyecto de Optimización")
st.write(
    "Ingrese un problema de Programación Lineal"
)

# Mostrar interfaz de entrada
problem_data = render_input_ui()

# ====================================
# PROCESAR MODELO
# ====================================

if problem_data:

    parsed_problem = build_problem(
        problem_data["type"],
        problem_data["objective"],
        problem_data["constraints"]
    )

    solver = SimplexSolver(
        objective=parsed_problem["objective"],
        constraints=parsed_problem["constraints"]
    )

    result = solver.solve()

    show_simplex_iterations(
        result=result,
        problem_data=parsed_problem,
        num_variables=len(problem_data["objective"])
    )

    if len(problem_data["objective"]) == 2:

        graphical_result = solve_graphical_method(
            objective=parsed_problem["objective"],
            constraints=parsed_problem["constraints"],
            problem_type=parsed_problem["type"]
        )

        show_graphical_solution(
            graphical_result,
            parsed_problem
        )