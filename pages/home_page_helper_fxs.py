import streamlit as st
import pandas as pd
import altair as alt

# Helper Functions for the home page
def load_data_file():
    """Method to load either an excel or csv file
    and return the dataframe"""
    df = pd.DataFrame()  # create an empty df to return if none loaded
    data_file = st.file_uploader("Upload CSV", type=["csv", "xlsx"])
    if data_file:  
        """ Check if a data file has been uploaded
        If so, then check to see if it is a csv or xlsx
        then choose corresponding pandas data reader"""
        if data_file.name.endswith("csv"):
            df = pd.read_csv(data_file)
        else:
            df = pd.read_excel(data_file)
        st.dataframe(df)

    return df

# Following three funcitons update the x, y, and group variable columns in the home page
def add_x_column(columns, axis_type, agg_type):
    x_axis = st.selectbox("X Axis", columns)
    
    # Remove x axis column selected from column list
    columns.remove(x_axis)

    x_axis_type = st.selectbox("X Axis Type", axis_type)
    x_axis_agg = st.selectbox("X Aggregate Type", agg_type)

    # save x options in dict
    x_options = {}
    if x_axis_type != "Undefined":
        x_options["type"] = x_axis_type.lower()

    if x_axis_agg != "None":
        x_options["aggregate"] = x_axis_agg.lower()

    return x_axis, x_options

def add_y_column(columns, axis_type, agg_type):
    # columns.insert(0, "Count of X-axis")
    y_axis = st.selectbox("Y Axis", columns)

    # Remove y axis column selected from column list
    columns.remove(y_axis)

    y_axis_type = st.selectbox("Y axis Type", axis_type)
    y_axis_agg = st.selectbox("Y Aggregate Type", agg_type)

    # save y options in dict
    y_options = {}
    if y_axis_type != "Undefined":
        y_options["type"] = y_axis_type.lower()

    if y_axis_agg != "None":
        y_options["aggregate"] = y_axis_agg.lower()

    return y_axis, y_options

def add_group_var_column(columns, axis_type):
    # Add a None option to the column list since grouping varaible is optional
    columns.insert(0, "None")
    group_var = st.selectbox("Grouping Variable (optional)", columns)
    
    # Remove group_var column selected from column list
    columns = columns.remove(group_var)

    # Add a None option to the axis type list since grouping varaible is optional
    group_var_type = st.selectbox("Grouping Variable Type", axis_type)

    # save group_var options in dict
    group_var_options = {}
    if group_var_type != "Undefined":
        group_var_options["type"] = group_var_type.lower()

    return group_var, group_var_options

# These funcitons update the graph settings
def update_graph_type(c, graph_type_chosen, df):
    if graph_type_chosen == "Bar Chart":
        c = c.mark_bar()
    if graph_type_chosen == "Line Chart":
        c = c.mark_line()
    if graph_type_chosen == "Scatter Chart":
        c = c.mark_circle()
    return c


def add_graph_encodings(
    c, x_axis, x_options, y_axis, y_options, group_var, group_var_options, tooltips
):
    # Create an x and y encoding thats will be passed to altairs encode function
    # if x or y options are present, include them
    x_encode = alt.X(x_axis, **x_options) if x_options else alt.X(x_axis)
    y_encode = alt.Y(y_axis, **y_options) if y_options else alt.Y(y_axis)
    group_var_encode = (
        alt.Color(group_var, **group_var_options) if group_var != "None" else ""
    )

    # Combine all the encodings into one list
    encode_options = (
        [x_encode, y_encode, group_var_encode]
        if group_var_options
        else [x_encode, y_encode]
    )

    # Create chart with combined encoding options above by unpacking the list
    # Also add in tooltips to the x, y and group if tooltips are enabled by unpacking the dictionary
    if tooltips:
        if group_var == "None":
            tooltip_options = {"tooltip": [x_axis, y_axis]}
            c = c.encode(*encode_options, **tooltip_options)
        else:
            tooltip_options = {"tooltip": [x_axis, y_axis, group_var]}
            c = c.encode(*encode_options, **tooltip_options)
    else:
        c = c.encode(*encode_options)

    return c
