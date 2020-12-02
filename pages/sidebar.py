import streamlit as st


def create_sidebar():
    """Function to create sidebar options besides the nav menu"""

    graph_types = ["None", "Bar Chart", "Line Chart", "Scatter Chart"]
    graph_type_chosen = st.sidebar.selectbox("Graph Type", graph_types)

    title = st.sidebar.text_input("Chart Title", "None", max_chars = 50)

    return graph_type_chosen, title
