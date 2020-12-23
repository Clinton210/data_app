# Core Pkgs
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc

from pages.about_page import about_main
from pages.graph_pages import graphPages

HTML_BANNER = """
    <div style="background-color:whitesmoke;padding:10px;border-radius:10px">
    <h1 style="color:black;text-align:center;">Data Visualization App </h1>
    </div>
    """


class MainApp:
    def __init__(self):
        """ Main programm"""
        st.set_page_config(
            page_title="Data Visualization App",
            page_icon=None,
            layout="centered",
            initial_sidebar_state="expanded",
        )

        stc.html(HTML_BANNER)

        with st.beta_expander("File Uploader"):

            data_file = st.file_uploader(
                "Upload CSV or Excel Data Files", type=["csv", "xlsx"]
            )
            self.df = self.convert_to_df(data_file)
            if not self.df.empty:
                st.dataframe(self.df)
        
        if self.df.empty:
            st.info(
                "Use the file uploader to import a csv or excel data file to get started."
            )
            self.df = pd.DataFrame()

        menu = ["Home", "Multi-Variable Graphs", "About"]
        menu_choice = st.sidebar.selectbox("Menu", menu)

        if menu_choice == "Multi-Variable Graphs":
            graph_pages = graphPages(self.df)
            graph_pages.multi_variable_graphs_main()

        if menu_choice == "About":
            about_main()

    @st.cache
    def convert_to_df(self, data_file):
        """Method to load either an excel or csv file
        and return the dataframe"""
        if data_file:
            """Check if a data file has been uploaded
            If so, then check to see if it is a csv or xlsx
            then choose corresponding pandas data reader"""
            if data_file.name.endswith("csv"):
                df = pd.read_csv(data_file)
            else:
                df = pd.read_excel(data_file)
        else:
            df = pd.DataFrame()
        return df


if __name__ == "__main__":
    app = MainApp()
