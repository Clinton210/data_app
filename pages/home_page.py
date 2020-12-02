import streamlit as st
import pandas as pd
import altair as alt
import xlrd

# Helper Functions
def load_data_file():
    """Method to load either an excel or csv file
    and return the dataframe"""
    df = pd.DataFrame() # create an empty df to return if none loaded
    data_file = st.file_uploader("Upload CSV", type=["csv", "xlsx"])
    if data_file: # Check if a data file has been uploaded
        # If so, then check to see if it is a csv or xlsx
        # then choose corresponding pandas data reader
        if data_file.name.endswith('csv'): 
            df = pd.read_csv(data_file)
        else:
            df = pd.read_excel(data_file)
        st.dataframe(df)

    return df


def home_main(graph_type_chosen, title_loc):
    axis_type = ["Unkown", "Quantitative", "Ordinal", "Temporal", "Geojson"]

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
        # create list of columns from df so that user can select columns
        columns = list(df.columns)

    if not df.empty:
        if graph_type_chosen != "None":
            c1, c2, c3 = st.beta_columns(3)
            with c1:
                x_axis = st.selectbox(
                    "X Axis", columns
                )
                # Remove x axis column selected from column list
                columns.remove(x_axis)
                x_axis_type = st.selectbox("X axis type", axis_type)

            with c2:
                y_axis = st.selectbox(
                    "Y Axis", columns
                )
                # Remove y axis column selected from column list
                columns.remove(y_axis)
                y_axis_type = st.selectbox("Y axis type", axis_type)

            with c3:
                # Add a None option to the column list since grouping varaible is optional
                columns.insert(0, "None")
                group_var = st.selectbox(
                    "Grouping Variable (optional)", columns
                )
                # Remove group_var column selected from column list
                columns = columns.remove(group_var)
                # Add a None option to the axis type list since grouping varaible is optional
                axis_type.insert(0, "N/A")
                y_axis_type = st.selectbox("Y axis type", axis_type)
                
            if st.button("Generate Graph"):
                """ Depending on type of chart, change the setting of 
                mark to mark_bar, mark_line, mark_circle
                then add other properties selected in sidebar"""

                if graph_type_chosen == "Bar Chart":
                    c = alt.Chart(df).mark_bar().encode(
                        x = x_axis, 
                        y = y_axis,
                    ).properties(
                        title = title_loc
                    )
                elif graph_type_chosen == "Line Chart":
                    c = alt.Chart(df).mark_line().encode(
                        x = x_axis, 
                        y = y_axis,
                    ).properties(
                        title = title_loc
                    )
                elif graph_type_chosen == "Scatter Chart":
                    c = alt.Chart(df).mark_circle().encode(
                        x = x_axis, 
                        y = y_axis,
                    ).properties(
                        title = title_loc
                    )

                st.altair_chart(c, use_container_width = True)