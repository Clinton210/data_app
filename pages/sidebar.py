import streamlit as st


def create_sidebar():
    """Function to create sidebar options besides the nav menu"""

    graph_types = ["None", "Bar Chart", "Line Chart", "Scatter Chart"]
    graph_type_chosen = st.sidebar.selectbox("Graph Type", graph_types)

    title = st.sidebar.text_input("Chart Title", "None", max_chars=50)

    # Customize setting checkboxes which will either change the setting or open up expanders to choose more options
    adjust_size = st.sidebar.checkbox("Adjust Chart Size")
    custom_title_settings = st.sidebar.checkbox("Customize Title")
    custom_x_axis = st.sidebar.checkbox("Customize X Axis")
    custom_y_axis = st.sidebar.checkbox("Customize Y Axis")
    tooltips = st.sidebar.checkbox("Add Tooltips")
    interactive = st.sidebar.checkbox("Add Interactivity (Zoom and Drag)")
    remove_grid = st.sidebar.checkbox("Remove Grid Lines")

    # Customize size settings. Initialize empty settings dict first
    size_settings = {}
    if adjust_size:
        with st.sidebar.beta_expander("Size Settings"):
            # Display size settings, customize height and width. Then add values in size setting
            size_settings = display_size_settings(size_settings)

    # Customize title settings. Initialize empty settings dict first
    title_settings = {}
    if custom_title_settings:
        with st.sidebar.beta_expander("Title Settings"):
            # Display title settings, customize title font size, color, and position. Then add values in title settings
            title_settings = display_title_settings(title_settings)

    # Customize x axis settings
    x_axis_settings = {}
    if custom_x_axis:
        with st.sidebar.beta_expander("X Axis Settings"):
            # Display x axis settings, customize title font size, color, and position, Then add values in x_axis_settings dict
            x_axis_settings = display_x_axis_settings(x_axis_settings)

    # Customize y axis settings
    y_axis_settings = {}
    if custom_y_axis:
        with st.sidebar.beta_expander("Y Axis Settings"):
            # Display y axis settings, customize title font size, color, and position, Then add values in y_axis_settings dict
            display_y_axis_settings(y_axis_settings)

    return (
        graph_type_chosen,
        title,
        title_settings,
        tooltips,
        x_axis_settings,
        y_axis_settings,
        interactive,
        remove_grid,
        size_settings,
    )


# Helper Functions
def display_size_settings(size_settings):
    # Customize height and add value to size setting
    height = st.slider("Height", min_value=100, max_value=1000, value=150, step=20)
    size_settings["height"] = height

    # Customize height and add value to size settings
    width = st.slider("Width", min_value=100, max_value=1000, value=150, step=20)
    size_settings["width"] = width

    return size_settings


def display_title_settings(title_settings):
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


def display_x_axis_settings(x_axis_settings):
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


def display_y_axis_settings(y_axis_settings):
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
