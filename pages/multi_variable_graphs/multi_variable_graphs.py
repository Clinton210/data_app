
import streamlit as st
import altair as alt


from pages.multi_variable_graphs.mvg_helper_fxs import (
    update_graph_type,
    add_graph_encodings,
    add_x_column,
    add_y_column,
    add_group_var_column
)

from pages.multi_variable_graphs.mvg_sidebar import create_sidebar


def multi_variable_graphs_main(df):
    (
        graph_type_chosen,
        title,
        title_settings,
        tooltips,
        x_axis_setings,
        y_axis_settings,
        interactive,
        remove_grid,
        size_settings
    ) = create_sidebar()


    axis_type = ["Undefined", "Quantitative", "Ordinal", "Temporal", "Geojson"]
    agg_type = ["None", "Average", "Median", "Sum"]

    if df.empty:
        st.info("Use the file uploader to import a csv or excel data file to get started.")
    else:
        columns = list(df.columns)
        if graph_type_chosen == "None":
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
                if size_settings:
                    st.altair_chart(c)
                else:
                    st.altair_chart(c, use_container_width = True)
            except Exception as e:
                st.error(e)