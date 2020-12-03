import streamlit as st
import pandas as pd
import altair as alt
import xlrd
from pages.home_page_helper_fxs import load_data_file, update_graph_type, add_graph_encodings


def home_main(graph_type_chosen, title, title_settings, tooltips, x_axis_settings, y_axis_settings, interactive):
    axis_type = ["Undefined", "Quantitative", "Ordinal", "Temporal", "Geojson"]
    agg_type = ["None", "Average", "Median", "Sum"]
    y_axis_agg = "Undefined" # Need to create and set to N/A in case user doesn't get the option to select y axis agg type
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
                x_axis = st.selectbox(
                    "X Axis", columns
                )
                # Remove x axis column selected from column list
                columns.remove(x_axis)

                x_axis_type = st.selectbox("X Axis Type", axis_type)
                x_axis_agg = st.selectbox("X Aggregate Type", agg_type)

                # save x options in dict
                x_options = {}
                if x_axis_type != "Undefined":
                    x_options['type'] = x_axis_type.lower()
                
                if x_axis_agg != "None":
                    x_options['aggregate'] = x_axis_agg.lower()

            with c2:
                #columns.insert(0, "Count of X-axis")
                y_axis = st.selectbox(
                    "Y Axis", columns
                )
                # Remove y axis column selected from column list
                columns.remove(y_axis)

                y_axis_type = st.selectbox("Y axis Type", axis_type)
                y_axis_agg = st.selectbox("Y Aggregate Type", agg_type)

                # save y options in dict
                y_options = {}
                if y_axis_type != "Undefined":
                    y_options['type'] = y_axis_type.lower()
    
                if y_axis_agg != "None":
                    y_options['aggregate'] = y_axis_agg.lower()

            with c3:
                # Add a None option to the column list since grouping varaible is optional
                columns.insert(0, "None")
                group_var = st.selectbox(
                    "Grouping Variable (optional)", columns
                )
                # Remove group_var column selected from column list
                columns = columns.remove(group_var)

                # Add a None option to the axis type list since grouping varaible is optional
                group_var_type = st.selectbox("Grouping Variable Type", axis_type)
               
                # save group_var options in dict
                group_var_options = {}
                if group_var_type!= "Undefined":
                    group_var_options['type'] = group_var_type.lower()

            ## Create and print chart ##

            # add dataframe and title to chart 
            c = alt.Chart(df, title = title) if title != "None" else alt.Chart(df)

            # Depending on type of chart, change the type of mark function and title of the graph
            c = update_graph_type(c, graph_type_chosen, df)

            # Add the encodings of x axis, y axis, and grouping variable 
            c = add_graph_encodings(
                c, x_axis, x_options, y_axis, y_options, group_var, group_var_options, tooltips
            )

            if title_settings: 
                c = c.configure_title(**title_settings)

            if x_axis_settings:
                c = c.configure_axisX(**x_axis_settings)

            if y_axis_settings:
                c = c.configure_axisY(**y_axis_settings)
            if interactive:
                c = c.interactive()
                
            # Create Graph
            try:
                st.altair_chart(c, use_container_width = True)
            except Exception as e:
                st.error(e)


