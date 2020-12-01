# Core Pkgs
import streamlit as st

from pages.home_page import home_main
from pages.about_page import about_main

# Data Pkgs
import pandas as pd


def main():
    """ Main programm"""
    # Create df
    df = pd.DataFrame()

    st.title("Python data vizulatization app")

    menu = ["Home", "About"]
    menu_choice = st.sidebar.selectbox("Menu", menu)

    if menu_choice == "Home":
        home_main()

    if menu_choice == "About":
        about_main()


if __name__ == "__main__":
    main()
