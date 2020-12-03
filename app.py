# Core Pkgs
import streamlit as st

from pages.home_page import home_main
from pages.about_page import about_main
from pages.sidebar import create_sidebar

# Data Pkgs
import pandas as pd


def main():
    """ Main programm"""
    st.set_page_config(
        page_title = "Data Visualization App",
        page_icon = None,
        layout = "centered",
        initial_sidebar_state = "expanded"
    )

    # Create dfs
    st.title("Data Visualization App")
    
    menu = ["Home", "About"]
    menu_choice = st.sidebar.selectbox("Menu", menu)

    (
        graph_type_chosen,
        title,
        title_settings,
        tooltips,
        x_axis_setings,
        y_axis_settings,
        interactive,
        remove_grid,
        size_settings,
    ) = create_sidebar()

    if menu_choice == "Home":
        home_main(
            graph_type_chosen,
            title,
            title_settings,
            tooltips,
            x_axis_setings,
            y_axis_settings,
            interactive,
            remove_grid,
            size_settings,
        )

    if menu_choice == "About":
        about_main()


if __name__ == "__main__":
    main()
