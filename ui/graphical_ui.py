import streamlit as st

def show_graphical_solution(graphical_result, problem_data):

    st.subheader("Método gráfico")

    st.dataframe(graphical_result["vertices_table"])

    st.pyplot(graphical_result["figure"])