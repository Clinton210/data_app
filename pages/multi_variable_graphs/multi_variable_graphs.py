
import streamlit as st
import altair as alt


from pages.multi_variable_graphs.mvg_helper_fxs import (
    update_graph_type,
    add_graph_encodings,
    add_x_column,
    add_y_column,
    add_group_var_column
)

# from pages.multi_variable_graphs.mvg_sidebar import create_sidebar
from pages.sidebar.sidebar import customSidebar


def multi_variable_graphs_main(df):

    # create the graph_types that can be used in mvg. Will pass this to the customSidebar constructor
    graph_types = ["None", "Bar Chart", "Line Chart", "Scatter Chart"]

    # creating varaible to hold arguments I would like to display for the mvg sidebar
    sidebar_args = ['adjust_size', 'custom_title_settings', 'custom_x_axis', 'custom_y_axis', 'tooltips', 'interactive', 'remove_grid']

    # instantiate customSidebar class to create a unique sidebar for the multi_variable_graphs (mvg) page
    mvg_sidebar = customSidebar(*sidebar_args, graph_types = graph_types)

    axis_type = ["Undefined", "Quantitative", "Ordinal", "Temporal", "Geojson"]
    agg_type = ["None", "Average", "Median", "Sum"]

    if df.empty:
        st.info("Use the file uploader to import a csv or excel data file to get started.")
    else:
        columns = list(df.columns)
        if mvg_sidebar.graph_type_chosen == "None":
            st.info("Please select a graph type in the options menu to the left")
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
            c = alt.Chart(df, title=mvg_sidebar.title) if mvg_sidebar.title != "None" else alt.Chart(df)

            # Depending on type of chart, change the type of mark function and title of the graph
            c = update_graph_type(c, mvg_sidebar.graph_type_chosen, df)

            # Add the encodings of x axis, y axis, and grouping variable
            c = add_graph_encodings(
                c,
                x_axis,
                x_options,
                y_axis,
                y_options,
                group_var,
                group_var_options,
                mvg_sidebar.tooltips,
            )

            # Update various chart settings
            if mvg_sidebar.custom_title_settings:
                c = c.configure_title(**mvg_sidebar.title_settings)
            if mvg_sidebar.custom_x_axis:
                c = c.configure_axisX(**mvg_sidebar.x_axis_settings)
            if mvg_sidebar.custom_y_axis:
                c = c.configure_axisY(**mvg_sidebar.y_axis_settings)
            if mvg_sidebar.interactive:
                c = c.interactive()
            if mvg_sidebar.remove_grid:
                c = c.configure_axis(grid=False)
            if mvg_sidebar.adjust_size:
                c = c.properties(**mvg_sidebar.size_settings)

            # Create Graph
            try:
                if mvg_sidebar.adjust_size:
                    st.altair_chart(c)
                else:
                    st.altair_chart(c, use_container_width = True)
            except Exception as e:
                st.error(e)