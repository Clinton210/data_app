import streamlit as st


def create_sidebar():
    """Function to create sidebar options besides the nav menu"""

    graph_types = ["None", "Bar Chart", "Line Chart", "Scatter Chart"]
    graph_type_chosen = st.sidebar.selectbox("Graph Type", graph_types)

    title = st.sidebar.text_input("Chart Title", "None", max_chars = 50)

    # Customize title settings
    title_settings = {}
    custom_title_settings = st.sidebar.checkbox("Customize Title")
    custom_x_axis = st.sidebar.checkbox("Customize X Axis")
    custom_y_axis = st.sidebar.checkbox("Customize Y Axis")
    tooltips = st.sidebar.checkbox("Use Tooltips")
    interactive = st.sidebar.checkbox("Add Interactivity (Zoom and Drag)")
    
    if custom_title_settings:
        with st.sidebar.beta_expander("Title Settings"):

            # Customize font size and add value to title settings
            title_font_size = st.slider(
                "Font Size", min_value = 10, max_value = 60, value = 10, step = 1
            )
            title_settings['fontSize'] = title_font_size

            # Customize color and add add value to title settings
            title_color = st.color_picker("Title Color")
            title_settings['color'] = title_color

            title_anchor = st.selectbox("Title Position", ["Start", "Middle", "End"], index = 1)
            title_settings['anchor'] = title_anchor.lower()

    # Customize x axis settings
    x_axis_settings = {}
    if custom_x_axis :
        with st.sidebar.beta_expander("X Axis Settings"):

            # Customize font size and add value to title settings
            x_axis_font_size = st.slider(
                "X Axis Font Size", min_value = 8, max_value = 40, value = 10, step = 1
            )
            x_axis_settings['titleFontSize'] = x_axis_font_size

            # Customize color and add add value to title settings
            x_axis_color = st.color_picker("X Axis Color")
            x_axis_settings['titleColor'] = x_axis_color

            x_axis_anchor = st.selectbox("X Axis Position", ["Start", "Middle", "End"], index = 1)
            x_axis_settings['titleAnchor'] = x_axis_anchor.lower()

    # Customize y axis settings
    y_axis_settings = {}

    if custom_y_axis :
        with st.sidebar.beta_expander("Y Axis Settings"):

            # Customize font size and add value to title settings
            y_axis_font_size = st.slider(
                "Y Axis Font Size", min_value = 8, max_value = 40, value = 10, step = 1
            )
            y_axis_settings['titleFontSize'] = y_axis_font_size

            # Customize color and add add value to title settings
            y_axis_color = st.color_picker("Y Axis Color")
            y_axis_settings['titleColor'] = y_axis_color

            y_axis_anchor = st.selectbox("Y Axis Position", ["Start", "Middle", "End"], index = 1)
            y_axis_settings['titleAnchor'] = y_axis_anchor.lower()

 

    return graph_type_chosen, title, title_settings, tooltips, x_axis_settings, y_axis_settings, interactive
