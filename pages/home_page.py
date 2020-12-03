import streamlit as st
import pandas as pd
import altair as alt
import xlrd
from pages.home_page_helper_fxs import (
    load_data_file,
    update_graph_type,
    add_graph_encodings,
    add_x_column,
    add_y_column,
    add_group_var_column
)


def home_main(
    graph_type_chosen,
    title,
    title_settings,
    tooltips,
    x_axis_settings,
    y_axis_settings,
    interactive,
    remove_grid,
    size_settings,
):
    
    axis_type = ["Undefined", "Quantitative", "Ordinal", "Temporal", "Geojson"]
    agg_type = ["None", "Average", "Median", "Sum"]

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
        if graph_type_chosen == "None":
            st.info("Please select a graph type in the left menu")
        else:
            c1, c2, c3 = st.beta_columns(3)
            with c1:
                x_axis, x_options = add_x_column(columns, axis_type, agg_type)

            with c2:
                # columns.insert(0, "Count of X-axis")
                y_axis, y_options = add_y_column(columns, axis_type, agg_type)

            with c3:
                # Add a None option to the column list since grouping varaible is optional
                group_var, group_var_options = add_group_var_column(columns, axis_type)

            ############################
            ## Create and print chart ##
            ############################

            # add dataframe and title to chart
            c = alt.Chart(df, title=title) if title != "None" else alt.Chart(df)

            # Depending on type of chart, change the type of mark function and title of the graph
            c = update_graph_type(c, graph_type_chosen, df)

            # Add the encodings of x axis, y axis, and grouping variable
            c = add_graph_encodings(
                c,
                x_axis,
                x_options,
                y_axis,
                y_options,
                group_var,
                group_var_options,
                tooltips,
            )

            # Update various chart settings
            if title_settings:
                c = c.configure_title(**title_settings)
            if x_axis_settings:
                c = c.configure_axisX(**x_axis_settings)
            if y_axis_settings:
                c = c.configure_axisY(**y_axis_settings)
            if interactive:
                c = c.interactive()
            if remove_grid:
                c = c.configure_axis(grid=False)
            if size_settings:
                c = c.properties(**size_settings)

            # Create Graph
            try:
                st.altair_chart(c)
            except Exception as e:
                st.error(e)
