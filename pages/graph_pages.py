import altair as alt
import pages.helper_functions as hf
import pandas as pd
import streamlit as st

from sidebar import customSidebar


class graphPages:
    """This class contains the logic for all graph pages (all pages except the about page)
    The graph pages use similar fuction to create and print the chart.
    The pages will be contained in this class with helper functions contained in helper_functions (hf) module."""

    def __init__(self, df):
        self.df = df
        self.axis_type = ["Undefined", "Quantitative", "Ordinal", "Temporal", "Geojson"]
        self.agg_type = ["None", "Average", "Median", "Sum"]

    #################################
    #### Single varaible graphs #####
    #################################

    def single_variable_graphs_main(self):
        graph_types = ["None", "Histogram"]
        self.agg_type = ""

        sidebar_args = [
            "adjust_size",
            "adjust_color",
            "custom_title",
            "custom_title_settings",
            "custom_x_axis",
            "custom_x_axis_title",
            "custom_y_axis",
            "custom_y_axis_title",
            # "tooltips",  # do not add tooltips to histogram
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
                x_axis, x_options = hf.add_x_column(
                    columns, self.axis_type, self.agg_type
                )
                x_options["bin"] = True  # add in a binning option for the histogram

                if x_axis == "None":
                    st.info("Select an X-Axis to create a chart.")
                else:  # Create and print chart
                    y_axis = "count()"  # set y-axis to count since there is no true y variable
                    y_options = ""  # need to define the variable and pass it below, so I set it to nothing
                    group_var = "None"  # Set group_var to none so it will not display
                    group_var_options = ""  # need to define the variable and pass it below, so I set it to nothing

                    self.c = hf.create_chart(
                        x_axis,
                        y_axis,
                        mvg_sidebar,
                        self.df,
                        x_options,
                        y_options,
                        group_var,
                        group_var_options,
                    )
                    hf.print_chart(mvg_sidebar, self.c)

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
                    x_axis, x_options = hf.add_x_column(
                        columns, self.axis_type, self.agg_type
                    )

                with c2:
                    y_axis, y_options = hf.add_y_column(
                        columns, self.axis_type, self.agg_type
                    )

                with c3:
                    group_var, group_var_options = hf.add_group_var_column(
                        columns, self.axis_type
                    )

                if x_axis == "None" or y_axis == "None":
                    st.info("Select an X-Axis and Y-Axis to create a chart.")
                else:  # Create and print chart
                    self.c = hf.create_chart(
                        x_axis,
                        y_axis,
                        mvg_sidebar,
                        self.df,
                        x_options,
                        y_options,
                        group_var,
                        group_var_options,
                    )
                    hf.print_chart(mvg_sidebar, self.c)
