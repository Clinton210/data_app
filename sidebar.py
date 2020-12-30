import streamlit as st
import streamlit.components.v1 as stc


class customSidebar:
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
        Send in the graph types as a keyword arg 'graph_types' with the graphs that the user can select

        Options available:
        adjust_size
        custom_title
        custom_title_settings
        custom_x_axis_title
        custom_x_axis
        custom_y_axis_title
        custom_y_axis
        tooltips
        interactive
        remove_grid
        """

        # initialize empty dicts for settings that require additional options. User settings will be stored inside the dicts.
        self.size_settings = {}
        self.color_settings = {}
        self.title_settings = {}
        self.x_axis_title = ""
        self.x_axis_title_settings = {}
        self.x_axis_settings = {}
        self.y_axis_title = ""
        self.y_axis_title_settings = {}
        self.y_axis_settings = {}

        # create a selectbox of different graph types passed into the constructor
        # graph_types = ["None", "Bar Chart", "Line Chart", "Scatter Chart"]
        self.graph_type_chosen = st.sidebar.selectbox(
            "Graph Type", kwargs["graph_types"]
        )

        # Customize setting checkboxes which will either change the setting or open up expanders to choose more options
        self.tooltips = (
            st.sidebar.checkbox("Add Tooltips") if "tooltips" in args else None
        )
        self.interactive = (
            st.sidebar.checkbox("Add Interactivity (Zoom and Drag)")
            if "interactive" in args
            else None
        )
        self.remove_grid = (
            st.sidebar.checkbox("Remove Grid Lines") if "remove_grid" in args else None
        )

        # Checkbox to turn off x-axis title
        self.x_axis_title_off = (
            st.sidebar.checkbox("Hide X-Axis Title")
            if "custom_x_axis_title" in args
            else False
        )
        if self.x_axis_title_off:
            self.x_axis_settings["title"] = None
            self.custom_x_axis = True
            self.custom_x_axis_title = False

        # Checkbox to turn off labels and grid
        self.x_axis_labels_grids_off = (
            st.sidebar.checkbox("Hide X-Axis Labels")
            if "custom_x_axis" in args
            else False
        )
        if self.x_axis_labels_grids_off:
            self.x_axis_settings["grid"] = False
            self.x_axis_settings["labels"] = False
            self.x_axis_settings["ticks"] = False
            self.custom_x_axis = True
            self.custom_x_axis_title = False

        # Checkbox to turn off y-axis title
        self.y_axis_title_off = (
            st.sidebar.checkbox("Hide Y-Axis Title")
            if "custom_y_axis_title" in args
            else False
        )
        if self.y_axis_title_off:
            self.y_axis_settings["title"] = None
            self.custom_y_axis = True
            self.custom_y_axis_title = False

        # Checkbox to turn off labels and grid
        self.y_axis_labels_grids_off = (
            st.sidebar.checkbox("Hide Y-Axis Labels")
            if "custom_y_axis" in args
            else False
        )
        if self.y_axis_labels_grids_off:
            self.y_axis_settings["grid"] = False
            self.y_axis_settings["labels"] = False
            self.y_axis_settings["ticks"] = False
            self.custom_y_axis = True
            self.custom_y_axis_title = False

        # Display default color and allow user to change
        if "adjust_color" in args:
            # Display size settings, customize height and width. Then add values in size setting
            self.color_settings = self._display_color_settings(self.color_settings)

        # Customize size settings.
        if "adjust_size" in args:
            with st.sidebar.beta_expander("Size Settings"):
                # Display size settings, customize height and width. Then add values in size setting
                self.adjust_size = st.checkbox("Adjust Chart Size")
                if self.adjust_size:
                    self.size_settings = self._display_size_settings(self.size_settings)

        # Customize title settings.
        if "custom_title" in args:
            with st.sidebar.beta_expander("Title Settings"):
                # Display title settings, customize title font size, color, and position. Then add values in title settings
                self.title = st.text_input("Chart Title", "None", max_chars=50)
                self.custom_title_settings = (
                    st.checkbox("Customize Title")
                    if "custom_title_settings" in args
                    else None
                )
                if self.custom_title_settings:
                    self.title_settings = self._display_title_settings(
                        self.title_settings
                    )

        # Customize x axis settings. Make sure that both the x axis labels and title are not turned off. If both are turned off, there is no reason to diplay X axis settings at all.
        if (
            "custom_x_axis_title" in args or "custom_x_axis" in args
        ) and not self._x_axis_lables_and_title_turned_off():
            with st.sidebar.beta_expander("X Axis Settings"):
                if (
                    not self.x_axis_title_off
                ):  # if x axis title turned off, no need to display the custom x axis title options
                    self.custom_x_axis_title = (
                        st.checkbox("Customize X Axis Title")
                        if "custom_x_axis_title" in args
                        else None
                    )
                    # Display x axis settings, customize title font size, color, and position, Then add values in x_axis_settings dict
                    if self.custom_x_axis_title:
                        (
                            self.x_axis_title,
                            self.x_axis_title_settings,
                        ) = self._display_x_axis_title_settings(
                            self.x_axis_settings
                        ) 
                if (
                    not self.x_axis_labels_grids_off
                ):  # if x axis labels turned off, no need to display the custom x axis labels options
                    self.custom_x_axis = (
                        st.checkbox("Customize X Axis")
                        if "custom_x_axis" in args
                        else None
                    )
                    if self.custom_x_axis:
                        returned_x_axis_settings = self._display_x_axis_settings(
                            self.x_axis_settings
                        ) 
                        self.x_axis_settings.update(returned_x_axis_settings)

        # Customize y axis settings. Make sure that both the y axis labels and title are not turned off. If both are turned off, there is no reason to diplay Y axis settings at all.
        if (
            ("custom_y_axis_title" in args) or ("custom_y_axis" in args)
        ) and not self._y_axis_lables_and_title_turned_off():
            with st.sidebar.beta_expander("Y Axis Settings"):
                if (
                    not self.y_axis_title_off
                ):  # if y axis title turned off, no need to display the custom y axis title options
                    self.custom_y_axis_title = (
                        st.checkbox("Customize Y Axis Title")
                        if "custom_y_axis_title" in args
                        else None
                    )
                    # Display x axis settings, customize title font size, color, and position, Then add values in x_axis_settings dict
                    if self.custom_y_axis_title:
                        (
                            self.y_axis_title,
                            self.y_axis_title_settings,
                        ) = self._display_y_axis_title_settings(
                            self.y_axis_settings
                        ) 
                if (
                    not self.y_axis_labels_grids_off
                ):  # if y axis labels turned off, no need to display the custom y axis labels options
                    self.custom_y_axis = (
                        st.checkbox("Customize Y Axis")
                        if "custom_y_axis" in args
                        else None
                    )
                    if self.custom_y_axis:
                        returned_y_axis_settings = self._display_y_axis_settings(
                            self.y_axis_settings
                        ) 
                        self.y_axis_settings.update(returned_y_axis_settings)

    # Methods
    # Do not cache this funciton unless you want an error.
    def _display_size_settings(self, size_settings):
        # Customize height and add value to size setting
        height = st.slider("Height", min_value=100, max_value=1000, value=500, step=20)
        size_settings["height"] = height

        # Customize height and add value to size settings
        width = st.slider("Width", min_value=100, max_value=1000, value=600, step=20)
        size_settings["width"] = width

        return size_settings

    def _display_color_settings(self, color_settings):
        # Customize general chart color
        color_chosen = st.sidebar.color_picker("Chart Color", value="#4682b4")
        color_settings["color"] = color_chosen

        return color_settings

    # Do not cache this funciton unless you want an error.
    def _display_title_settings(self, title_settings):
        # Customize font size and add value to title settings
        title_font_size = st.slider(
            "Font Size", min_value=10, max_value=60, value=14, step=1
        )
        title_settings["fontSize"] = title_font_size

        # Customize color and add add value to title settings
        title_color = st.color_picker("Title Color")
        title_settings["color"] = title_color
        title_anchor = st.selectbox(
            "Title Position", ["Start", "Middle", "End"], index=1
        )
        title_settings["anchor"] = title_anchor.lower()
        title_offset = st.slider(
            "Title Offset", min_value=0, max_value=40, value=5, step=1
        )
        title_settings['offset'] = title_offset

        return title_settings

    # Do not cache this funciton unless you want an error.
    def _display_x_axis_title_settings(self, x_axis_title_settings):
        # Customize x axis title
        x_axis_title = st.text_input("X-Axis Title", "Default", max_chars=50)

        # Customize x axis title font size and add value to x axis title settings
        x_axis_title_font_size = st.slider(
            "X Axis Title Font Size", min_value=8, max_value=40, value=10, step=1
        )
        x_axis_title_settings["titleFontSize"] = x_axis_title_font_size

        # Customize x axis title color and add add value to x axis title settings
        x_axis_title_color = st.color_picker("X Axis Title Color")
        x_axis_title_settings["titleColor"] = x_axis_title_color
        x_axis_title_anchor = st.selectbox(
            "X Axis Title Position", ["Start", "Middle", "End"], index=1
        )
        x_axis_title_settings["titleAnchor"] = x_axis_title_anchor.lower()

        x_axis_title_padding = st.slider(
            "X Axis Title Padding", min_value=0, max_value=40, value=5, step=1
        )
        x_axis_title_settings["titlePadding"] = x_axis_title_padding

        return x_axis_title, x_axis_title_settings

    def _display_x_axis_settings(self, x_axis_settings):
        # Customize x axis label color and add add value to x axis settings
        x_axis_label_color = st.color_picker("X Axis Label Color")
        x_axis_settings["labelColor"] = x_axis_label_color

        # Customize x axis label color and add add value to y axis settings
        x_axis_label_font_size = st.slider(
            "X Axis Label Font Size", min_value=6, max_value=20, value=8, step=1
        )
        x_axis_settings["labelFontSize"] = x_axis_label_font_size

        # Customize the offset value for the x axis
        x_axis_offset = st.slider(
            "X Axis Offset (offset to diplace the axis from the edge)",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
        )
        x_axis_settings["offset"] = x_axis_offset

        # Customize x axis grid color
        x_axis_tick_color = st.color_picker("X Axis Tick Color")
        x_axis_settings["tickColor"] = x_axis_tick_color

        # Customize x axis width
        x_axis_tick_width = st.slider(
            "X Axis Tick Size", min_value=0, max_value=30, value=2, step=1
        )
        x_axis_settings["tickSize"] = x_axis_tick_width

        return x_axis_settings

    # Do not cache this funciton unless you want an error.
    def _display_y_axis_title_settings(self, y_axis_title_settings):
        # Customize y axis title
        y_axis_title = st.text_input("Y-Axis Title", "Default", max_chars=50)

        # Customize y axis title font size and add add value to y axis settings
        y_axis_title_font_size = st.slider(
            "Y Axis Title Font Size", min_value=8, max_value=40, value=10, step=1
        )
        y_axis_title_settings["titleFontSize"] = y_axis_title_font_size

        # Customize y axis title color and add add value to y axis settings
        y_axis_title_color = st.color_picker("Y Axis Title Color")
        y_axis_title_settings["titleColor"] = y_axis_title_color
        y_axis_anchor = st.selectbox(
            "Y Axis Title Position", ["Start", "Middle", "End"], index=1
        )
        y_axis_title_settings["titleAnchor"] = y_axis_anchor.lower()

        y_axis_title_padding = st.slider(
            "Y Axis Title Padding", min_value=0, max_value=40, value=5, step=1
        )
        y_axis_title_settings["titlePadding"] = y_axis_title_padding

        return y_axis_title, y_axis_title_settings

    def _display_y_axis_settings(self, y_axis_settings):
        # Customize x axis label color and add add value to x axis settings
        y_axis_label_color = st.color_picker("Y Axis Label Color")
        y_axis_settings["labelColor"] = y_axis_label_color

        # Customize x axis label color and add add value to y axis settings
        y_axis_label_font_size = st.slider(
            "Y Axis Label Font Size", min_value=6, max_value=20, value=8, step=1
        )
        y_axis_settings["labelFontSize"] = y_axis_label_font_size

        # Customize the offset value for the x axis
        y_axis_offset = st.slider(
            "Y Axis Offset (offset to diplace the axis from the edge)",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
        )
        y_axis_settings["offset"] = y_axis_offset

        # Customize x axis grid color
        y_axis_tick_color = st.color_picker("Y Axis Tick Color")
        y_axis_settings["tickColor"] = y_axis_tick_color

        # Customize x axis width
        y_axis_tick_width = st.slider(
            "Y Axis Tick Size", min_value=0, max_value=30, value=2, step=1
        )
        y_axis_settings["tickSize"] = y_axis_tick_width

        return y_axis_settings

    def _x_axis_lables_and_title_turned_off(self):
        return True if self.x_axis_labels_grids_off and self.x_axis_title_off else False

    def _y_axis_lables_and_title_turned_off(self):
        return True if self.y_axis_labels_grids_off and self.y_axis_title_off else False
