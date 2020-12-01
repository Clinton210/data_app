import streamlit as st
import pandas as pd


def load_data_file():
    df = pd.DataFrame()
    data_file = st.file_uploader("Upload CSV", type=["csv"])
    if data_file:
        df = pd.read_csv(data_file)
        st.dataframe(df)

    return df


def home_main():
    modified_df = pd.DataFrame()

    with st.beta_expander("Instructions"):

        st.markdown(
            """
        1. Load a dataset (csv or excel file) using the file uploader below
        2. Expand the options section to choose graph type and columns
        3. Once options are selected, click the generate graph button
        """
        )

    with st.beta_expander("File Uploader"):
        df = load_data_file()
        columns = df.columns

    if not df.empty:
        with st.beta_expander("Options"):

            graph_types = ["None", "Line Chart", "Bar Chart"]
            graph_type_chosen = st.selectbox("Graph Type", graph_types)

            if graph_type_chosen != "None":
                if graph_type_chosen == "Line Chart":
                    num_columns_chosen = st.multiselect(
                        "Numerical Columns", columns, key="line"
                    )
                    modified_df = df[num_columns_chosen]
                if graph_type_chosen == "Bar Chart":
                    num_columns_chosen = st.multiselect(
                        "Numerical Columns", columns, key="bar"
                    )
                    modified_df = df[num_columns_chosen]

    if not modified_df.empty:
        if st.button("Generate Graph"):
            if graph_type_chosen == "Line Chart":
                st.line_chart(modified_df)
            if graph_type_chosen == "Bar Chart":
                st.bar_chart(modified_df)
