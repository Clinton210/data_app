import streamlit as st

def about_main():
    """function to display about information"""
    with st.beta_expander("App Details"):
        st.markdown("""
        Programming Language: [Python](https://www.python.org/)\n
        App Framework: [Streamlit](https://www.streamlit.io/)\n
        Chart Package: [Altair] (https://altair-viz.github.io/)\n
        Data Package: [Pandas] (https://pandas.pydata.org/)
        """)
    with st.beta_expander("Source Files"):
        st.markdown("[GitHub Page](https://github.com/Clinton210/data_app)")
    with st.beta_expander("Developer: Clinton Potter"):
        st.markdown("[LinkedIn](https://www.linkedin.com/in/clinton-potter-75487944/)")
