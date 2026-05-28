import streamlit as st


def render_input_ui():

    # =========================
    # TIPO DE PROBLEMA
    # =========================

    problem_type = st.selectbox(
        "Tipo de problema",
        ["Maximizar", "Minimizar"]
    )

    # =========================
    # NÚMERO DE VARIABLES
    # =========================

    num_variables = st.number_input(
        "Número de variables",
        min_value=2,
        max_value=10,
        value=2
    )

    # =========================
    # NÚMERO DE RESTRICCIONES
    # =========================

    num_constraints = st.number_input(
        "Número de restricciones",
        min_value=1,
        max_value=10,
        value=2
    )

    st.divider()

    # =========================
    # FUNCIÓN OBJETIVO
    # =========================

    st.subheader("Función Objetivo")

    objective = []

    cols = st.columns(num_variables)

    for i in range(num_variables):

        value = cols[i].number_input(
            f"Coeficiente X{i+1}",
            value=0.0
        )

        objective.append(value)

    st.divider()

    # =========================
    # RESTRICCIONES
    # =========================

    st.subheader("Restricciones")

    constraints = []

    for r in range(num_constraints):

        st.write(f"### Restricción {r + 1}")

        row = st.columns(num_variables + 2)

        coeffs = []

        # Coeficientes
        for c in range(num_variables):

            value = row[c].number_input(
                f"X{c + 1}",
                value=0.0,
                key=f"r{r}c{c}"
            )

            coeffs.append(value)

        # Operador
        operator = row[num_variables].selectbox(
            "Operador",
            ["<=", ">=", "="],
            key=f"op{r}"
        )

        # RHS
        rhs = row[num_variables + 1].number_input(
            "Resultado",
            value=0.0,
            key=f"rhs{r}"
        )

        constraints.append({
            "coeffs": coeffs,
            "operator": operator,
            "rhs": rhs 
        })

    st.divider()

    # =========================
    # BOTÓN RESOLVER
    # =========================

    if st.button("Resolver problema"):

        return {
            "type": problem_type,
            "objective": objective,
            "constraints": constraints
        }

    return None