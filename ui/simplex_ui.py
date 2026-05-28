import streamlit as st
import pandas as pd
import numpy as np

def build_tableau_dataframe(tableau, basic_variables, num_variables, num_constraints):
    column_names = []

    for i in range(num_variables):
        column_names.append(f"X{i + 1}")

    for i in range(num_constraints):
        column_names.append(f"S{i + 1}")

    column_names.append("RHS")

    tableau_df = pd.DataFrame(
        tableau,
        columns=column_names
    )

    row_names = basic_variables + ["Z"]
    tableau_df.index = row_names

    return tableau_df.round(4)

def show_simplex_iterations(result, problem_data, num_variables):
    num_constraints = len(problem_data["constraints"])

    st.subheader("Solución numérica paso a paso - Método Simplex")

    # =========================
    # RESULTADO ÓPTIMO
    # =========================

    st.write("### Resultado óptimo")

    solution_data = []

    for i, value in enumerate(result["solution"]):
        solution_data.append({
            "Variable": f"X{i + 1}",
            "Valor": round(value, 4)
        })

    solution_df = pd.DataFrame(solution_data)
    st.dataframe(solution_df, use_container_width=True)

    st.success(f"Valor óptimo: Z = {result['optimal_value']:.4f}")

    # =========================
    # HOLGURAS
    # =========================

    st.write("### Variables de holgura en la solución final")

    slack_data = []

    for i, variable_name in enumerate(result["basic_variables"]):

        if variable_name.startswith("S"):
            slack_data.append({
                "Variable de holgura": variable_name,
                "Valor": round(result["tableau"][i, -1], 4),
                "Interpretación": "Recurso no utilizado"
            })

    if slack_data:
        slack_df = pd.DataFrame(slack_data)
        st.dataframe(slack_df, use_container_width=True)
    else:
        st.info("No hay variables de holgura positivas en la base final.")

    # =========================
    # ITERACIONES
    # =========================

    st.write("### Iteraciones del método simplex")

    for step in result["iterations"]:

        st.write(f"#### Iteración {step['iteration']}")
        st.info(step["message"])

        if step["entering_variable"] is not None:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Variable que entra", step["entering_variable"])

            with col2:
                st.metric("Variable que sale", step["leaving_variable"])

            with col3:
                st.metric("Elemento pivote", round(step["pivot_element"], 4))

            ratio_data = []

            basic_before = step.get(
                "basic_variables_before",
                step["basic_variables"]
            )

            for i, ratio in enumerate(step["ratios"]):

                if np.isinf(ratio):
                    ratio_value = "-"
                else:
                    ratio_value = round(ratio, 4)

                ratio_data.append({
                    "Fila": basic_before[i],
                    "Razón RHS / columna pivote": ratio_value
                })

            st.write("##### Prueba de razón mínima")
            st.dataframe(
                pd.DataFrame(ratio_data),
                use_container_width=True
            )

        tableau_df = build_tableau_dataframe(
            tableau=step["tableau"],
            basic_variables=step["basic_variables"],
            num_variables=num_variables,
            num_constraints=num_constraints
        )

        st.write("##### Tablero simplex")
        st.dataframe(tableau_df, use_container_width=True)

    # =========================
    # TABLERO SIMPLEX FINAL
    # =========================

    st.write("### Tablero simplex final")

    final_tableau_df = build_tableau_dataframe(
        tableau=result["tableau"],
        basic_variables=result["basic_variables"],
        num_variables=num_variables,
        num_constraints=num_constraints
    )

    st.dataframe(final_tableau_df, use_container_width=True)

    st.info(
        "En el tablero simplex final, las filas indican las variables básicas. "
        "La columna RHS muestra el valor final de cada variable básica. "
        "La última fila corresponde a la función objetivo."
    )