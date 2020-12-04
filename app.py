# Core Pkgs
import streamlit as st
import streamlit.components.v1 as stc

from pages.home_page import home_main
from pages.about_page import about_main
from pages.sidebar import create_sidebar

HTML_BANNER = """
    <div style="background-color:whitesmoke;padding:10px;border-radius:10px">
    <h1 style="color:black;text-align:center;">Data Visualization App </h1>
    </div>
    """

def main():
    """ Main programm"""
    st.set_page_config(
        page_title = "Data Visualization App",
        page_icon = None,
        layout = "centered",
        initial_sidebar_state = "expanded"
    )

    # Create dfs
    stc.html(HTML_BANNER)
    
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
