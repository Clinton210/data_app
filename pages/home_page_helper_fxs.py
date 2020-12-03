import streamlit as st
import pandas as pd
import altair as alt

# Helper Functions for the home page
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

# These funcitons update the graph settings
def update_graph_type(c, graph_type_chosen, df):
    if graph_type_chosen == "Bar Chart":
        c = c.mark_bar()
    if graph_type_chosen == "Line Chart":
        c = c.mark_line()
    if graph_type_chosen == "Scatter Chart":
       c = c.mark_circle()
    return c

def add_graph_encodings(c, x_axis, x_options, y_axis, y_options, group_var, group_var_options, tooltips):
    # Create an x and y encoding thats will be passed to altairs encode function
    # if x or y options are present, include them
    x_encode = alt.X(x_axis, **x_options) if x_options else alt.X(x_axis)
    y_encode = alt.Y(y_axis, **y_options) if y_options else alt.Y(y_axis)
    group_var_encode = alt.Color(group_var, **group_var_options) if group_var != "None" else ""
    
    # Combine all the encodings to one list
    encode_options = [x_encode, y_encode, group_var_encode] if group_var_options else [x_encode, y_encode]

    # Create chart with combined encoding options above by unpacking the list
    # Also add in tooltips to the x, y and group if tooltips are enabled by unpacking the dictionary
    if tooltips:
        if group_var == "None":
            tooltip_options = {'tooltip': [x_axis, y_axis]}
            c = c.encode(*encode_options, **tooltip_options)
        else:
            tooltip_options = {'tooltip': [x_axis, y_axis, group_var]}
            c = c.encode(*encode_options, **tooltip_options)
    else:
        c = c.encode(*encode_options)

    return c        

