import streamlit as st
import streamlit.components.v1 as stc

class customSidebar():
    """class to create sidebar options other than the nav menu
    Pass in the setting to display to the constructor as args along with 
    the graph types as a keyword. Can access invidual attributes thrrough the class
    as well as dictionaries that save various values that align with Altair's settings.
    
    adjust_size: height, width
    title_settings: fontSize, color, anchor
    x_axis_settings: titleFontSize, titleColor, titleAnchor
    y_axis_settings: titleFontSize, titleColor, titleAnchor

    """

    def __init__(self, *args, **kwargs):
        """ 
        Send in the options to include in the sidebar as string args.
        Send in the graph types as a dictionary with 'graph_types' as key and values are strings of graphs types to choose
        
        Options available:
        adjust_size 
        custom_title_settings
        custom_x_axis
        custom_y_axis
        tooltips
        interactive
        remove_grid
        """

        # create a selectbox of different graph types passed into the constructor
        # graph_types = ["None", "Bar Chart", "Line Chart", "Scatter Chart"]
        self.graph_type_chosen = st.sidebar.selectbox("Graph Type", kwargs['graph_types'])

        self.title = st.sidebar.text_input("Chart Title", "None", max_chars=50)
        
        # Customize setting checkboxes which will either change the setting or open up expanders to choose more options
        self.adjust_size = st.sidebar.checkbox("Adjust Chart Size") if 'adjust_size' in args else None
        self.custom_title_settings = st.sidebar.checkbox("Customize Title") if 'custom_title_settings' in args else None
        self.custom_x_axis = st.sidebar.checkbox("Customize X Axis") if 'custom_x_axis' in args else None
        self.custom_y_axis = st.sidebar.checkbox("Customize Y Axis") if 'custom_y_axis' in args else None
        self.tooltips = st.sidebar.checkbox("Add Tooltips") if 'tooltips' in args else None
        self.interactive = st.sidebar.checkbox("Add Interactivity (Zoom and Drag)") if 'interactive' in args else None
        self.remove_grid = st.sidebar.checkbox("Remove Grid Lines") if 'remove_grid' in args else None


        # Customize size settings. Initialize empty settings dict to hold user settings
        if self.adjust_size:
            self.size_settings = {}
            with st.sidebar.beta_expander("Size Settings"):
                # Display size settings, customize height and width. Then add values in size setting
                self.size_settings = self._display_size_settings(self.size_settings)

        # Customize title settings. Initialize empty settings dict to hold user settings
        self.title_settings = {}
        if self.custom_title_settings:
            with st.sidebar.beta_expander("Title Settings"):
                # Display title settings, customize title font size, color, and position. Then add values in title settings
                self.title_settings = self._display_title_settings(self.title_settings)

        # Customize x axis settings. Initialize empty settings dict to hold user settings
        self.x_axis_settings = {}
        if self.custom_x_axis:
            with st.sidebar.beta_expander("X Axis Settings"):
                # Display x axis settings, customize title font size, color, and position, Then add values in x_axis_settings dict
                self.x_axis_settings = self._display_x_axis_settings(self.x_axis_settings)

        # Customize y axis settings. Initialize empty settings dict to hold user settings
        self.y_axis_settings = {}
        if self.custom_y_axis:
            with st.sidebar.beta_expander("Y Axis Settings"):
                # Display y axis settings, customize title font size, color, and position, Then add values in y_axis_settings dict
                self._display_y_axis_settings(self.y_axis_settings)

    # Methods 
    def _display_size_settings(self, size_settings):
        # Customize height and add value to size setting
        height = st.slider("Height", min_value=100, max_value=1000, value=150, step=20)
        size_settings["height"] = height

        # Customize height and add value to size settings
        width = st.slider("Width", min_value=100, max_value=1000, value=150, step=20)
        size_settings["width"] = width

        return size_settings


    def _display_title_settings(self, title_settings):
        # Customize font size and add value to title settings
        title_font_size = st.slider(
            "Font Size", min_value=10, max_value=60, value=10, step=1
        )
        title_settings["fontSize"] = title_font_size

        # Customize color and add add value to title settings
        title_color = st.color_picker("Title Color")
        title_settings["color"] = title_color
        title_anchor = st.selectbox("Title Position", ["Start", "Middle", "End"], index=1)
        title_settings["anchor"] = title_anchor.lower()
        
        return title_settings


    def _display_x_axis_settings(self, x_axis_settings):
        # Customize x axis title font size and add value to x axis settings
        x_axis_font_size = st.slider(
            "X Axis Title Font Size", min_value=8, max_value=40, value=10, step=1
        )
        x_axis_settings["titleFontSize"] = x_axis_font_size

        # Customize x axis title color and add add value to x axis settings
        x_axis_color = st.color_picker("X Axis Title olor")
        x_axis_settings["titleColor"] = x_axis_color
        x_axis_anchor = st.selectbox(
            "X Axis Title Position", ["Start", "Middle", "End"], index=1
        )
        x_axis_settings["titleAnchor"] = x_axis_anchor.lower()

        return x_axis_settings


    def _display_y_axis_settings(self, y_axis_settings):
        # Customize y axis title font size and add add value to y axis settings
        y_axis_font_size = st.slider(
            "Y Axis Title Font Size", min_value=8, max_value=40, value=10, step=1
        )
        y_axis_settings["titleFontSize"] = y_axis_font_size

        # Customize x axis title color and add add value to y axis settings
        y_axis_color = st.color_picker("Y Axis Title Color")
        y_axis_settings["titleColor"] = y_axis_color
        y_axis_anchor = st.selectbox(
            "Y Axis Title Position", ["Start", "Middle", "End"], index=1
        )
        y_axis_settings["titleAnchor"] = y_axis_anchor.lower()

        return y_axis_settings
