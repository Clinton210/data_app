import altair as alt
import pandas as pd
import streamlit as st

from pages.sidebar import customSidebar


class graphPages:
    """This class contains the logic for all graph pages (all pages except the about)
    The graph pages will use similar methods to create and print the chart.
    The pages will be contained at the top in thier own methods."""

    def __init__(self, df):
        self.df = df
        self.axis_type = ["Undefined", "Quantitative", "Ordinal", "Temporal", "Geojson"]
        self.agg_type = ["None", "Average", "Median", "Sum"]

    ################################
    #### Multi varaible graphs #####
    ################################

    def multi_variable_graphs_main(self):

        # create the graph_types that can be used in mvg. Will pass this to the customSidebar constructor
        graph_types = ["None", "Bar Chart", "Line Chart", "Scatter Chart"]

        # creating varaible to hold arguments I would like to display for the mvg sidebar
        sidebar_args = [
            "adjust_size",
            "adjust_color",
            "custom_title",
            "custom_title_settings",
            "custom_x_axis",
            "custom_x_axis_title",
            "custom_y_axis",
            "custom_y_axis_title",
            "tooltips",
            "interactive",
            "remove_grid",
        ]

        # instantiate customSidebar class for the multi_variable_graphs (mvg) page
        mvg_sidebar = customSidebar(*sidebar_args, graph_types=graph_types)

        

        if not self.df.empty:
            # create a list to hold all the column names
            columns = list(self.df.columns)

            # insert a "None" to the beggining, which will be the default choice.
            # User will need to select columns before a graph will generate.
            # This will prevent columns being selected as default that are hard to graph
            columns.insert(0, "None")

            if mvg_sidebar.graph_type_chosen == "None":
                st.info("Please select a graph type in the options menu to the left")
            else:
                c1, c2, c3 = st.beta_columns(3)
                with c1:
                    x_axis, x_options = self.add_x_column(columns, self.axis_type, self.agg_type)

                with c2:
                    # columns.insert(0, "Count of X-axis")
                    y_axis, y_options = self.add_y_column(columns, self.axis_type, self.agg_type)

                with c3:
                    # Add a None option to the column list since grouping varaible is optional
                    group_var, group_var_options = self.add_group_var_column(
                        columns, self.axis_type
                    )

                if x_axis == "None" or y_axis == "None":
                    st.info("Select an X-Axis and Y-Axis to create a chart.")
                else:  # Create and print chart
                    self.c = self.create_chart(
                        x_axis,
                        y_axis,
                        mvg_sidebar,
                        self.df,
                        x_options,
                        y_options,
                        group_var,
                        group_var_options,
                    )
                    self.print_chart(mvg_sidebar, self.c)

    ##################################
    ######### HELPER METHODS #########
    ##################################

    def create_chart(
        self,
        x_axis,
        y_axis,
        mvg_sidebar,
        df,
        x_options,
        y_options,
        group_var,
        group_var_options,
    ):

        # add dataframe and title to chart
        c = (
            alt.Chart(df, title=mvg_sidebar.title)
            if mvg_sidebar.title != "None"
            else alt.Chart(df)
        )

        # Depending on type of chart, change the type of mark function and title of the graph
        c = self.update_graph_type(c, mvg_sidebar.graph_type_chosen, self.df)

        # Add the encodings of x axis, y axis, and grouping variable
        c = self.add_multi_variable_graph_encodings(
            c,
            x_axis,
            x_options,
            y_axis,
            y_options,
            group_var,
            group_var_options,
            mvg_sidebar.tooltips,
        )

        # Change axis labels if supplied.
        c = self.update_axis_titles(mvg_sidebar, c)

        # Update various chart settings
        c = self.update_various_graph_settings(mvg_sidebar, c)

        # Create Graph

        return c

    def print_chart(self, mvg_sidebar, c):
        # Create Graph
        try:
            if mvg_sidebar.adjust_size:
                st.altair_chart(c)
            else:
                st.altair_chart(c, use_container_width=True)
        except Exception as e:
            st.error(e)

    # Following three fuctions update the x, y, and group variable columns
    # Do not cache this fuction unless you want an error.
    def add_x_column(self, columns, axis_type, agg_type):
        x_axis = st.selectbox("X Axis", columns)

        # Remove x axis column selected from column list unless it is None
        if x_axis != "None":
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

    # Do not cache this fuction unless you want an error.
    def add_y_column(self, columns, axis_type, agg_type):
        # columns.insert(0, "Count of X-axis")
        y_axis = st.selectbox("Y Axis", columns)

        # Remove y axis column selected from column list unless it is None
        if y_axis != "None":
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

    # Do not cache this fuction unless you want an error.
    def add_group_var_column(self, columns, axis_type):

        group_var = st.selectbox("Grouping Variable (optional)", columns)

        # Remove group_var column selected from column list unless it is None
        if group_var != "None":
            columns = columns.remove(group_var)

        # Add a None option to the axis type list since grouping varaible is optional
        group_var_type = st.selectbox("Grouping Variable Type", axis_type)

        # save group_var options in dict
        group_var_options = {}
        if group_var_type != "Undefined":
            group_var_options["type"] = group_var_type.lower()

        return group_var, group_var_options

    # Following methods update the graph settings
    # Do not cache this fuction unless you want an error.
    def update_graph_type(self, c, graph_type_chosen, df):
        if graph_type_chosen == "Bar Chart":
            c = c.mark_bar()
        if graph_type_chosen == "Line Chart":
            c = c.mark_line()
        if graph_type_chosen == "Scatter Chart":
            c = c.mark_circle()
        return c

    # Do not cache this fuction unless you want an error.
    def add_multi_variable_graph_encodings(
        self,
        c,
        x_axis,
        x_options,
        y_axis,
        y_options,
        group_var,
        group_var_options,
        tooltips,
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

    def update_various_graph_settings(self, mvg_sidebar, c):
        # Update various chart settings
        if mvg_sidebar.custom_title_settings:
            c = c.configure_title(**mvg_sidebar.title_settings)
        if mvg_sidebar.custom_x_axis_title:
            c = c.configure_axisX(**mvg_sidebar.x_axis_title_settings)
        if mvg_sidebar.custom_x_axis or mvg_sidebar.x_axis_title_off:
            c = c.configure_axisX(**mvg_sidebar.x_axis_settings)
        if mvg_sidebar.custom_y_axis_title:
            c = c.configure_axisY(**mvg_sidebar.y_axis_title_settings)
        if mvg_sidebar.custom_y_axis or mvg_sidebar.y_axis_title_off:
            c = c.configure_axisY(**mvg_sidebar.y_axis_settings)
        if mvg_sidebar.interactive:
            c = c.interactive()
        if mvg_sidebar.remove_grid:
            c = c.configure_axis(grid=False)
        if mvg_sidebar.adjust_size:
            c = c.properties(**mvg_sidebar.size_settings)
        if mvg_sidebar.color_settings:
            c = c.configure_mark(**mvg_sidebar.color_settings)
        return c

    def update_axis_titles(self, mvg_sidebar, c):
        # Change axis labels if supplied. Kind of pain to do it other ways.
        if mvg_sidebar.custom_x_axis_title and mvg_sidebar.x_axis_title != "Default":
            c.encoding.x.title = mvg_sidebar.x_axis_title

        if mvg_sidebar.custom_y_axis_title and mvg_sidebar.y_axis_title != "Default":
            c.encoding.y.title = mvg_sidebar.y_axis_title

        return c
