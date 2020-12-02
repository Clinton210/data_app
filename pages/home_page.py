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


def home_main(graph_type_chosen, title_loc, group_var):

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
        mod_df = pd.DataFrame()
        # create list of columns from df so that user can select columns
        columns = df.columns 
        group_var_selected = None

    if not df.empty:
        col_num = 0
        if graph_type_chosen != "None":
            with st.beta_expander("Columns"):
                x_axis = st.selectbox(
                    "X Axis", columns
                )
                mod_df.insert(col_num, x_axis, df[x_axis])
                # Remove x axis column selected from column list
                columns = columns.drop([x_axis])
                y_axis = st.selectbox(
                    "Y Axis", columns
                )
                columns = columns.drop([y_axis])
                # Remove y axis column selected from column list
                if group_var == "Yes":
                   group_var_selected = st.selectbox("Grouping Variable", columns)     
                
            if st.button("Generate Graph"):
                """ Depending on type of chart, change the setting of 
                mark to mark_bar, mark_line, mark_circle
                then add other properties selected in sidebar"""

                if graph_type_chosen == "Bar Chart":
                    c = alt.Chart(df).mark_bar().encode(
                        x = x_axis, 
                        y = y_axis,
                        #color = group_var_selected
                    ).properties(
                        title = title_loc
                    )
                elif graph_type_chosen == "Line Chart":
                    c = alt.Chart(df).mark_line().encode(
                        x = x_axis, 
                        y = y_axis,
                        #color = group_var_selected
                    ).properties(
                        title = title_loc
                    )
                elif graph_type_chosen == "Scatter Chart":
                    c = alt.Chart(df).mark_circle().encode(
                        x = x_axis, 
                        y = y_axis,
                        #color = group_var_selected
                    ).properties(
                        title = title_loc
                    )

                st.altair_chart(c, use_container_width = True)