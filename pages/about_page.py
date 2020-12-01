import streamlit as st


def about_main():
    st.subheader("This open source app is written in Python with Streamlit.")
    st.subheader("")
    with st.beta_expander("Source Files"):
        st.markdown("[GitHub Page](https://github.com/clinton210)")
    with st.beta_expander("Streamlit Info"):
        st.markdown("[Streamlit Website](https://www.streamlit.io/)")
    with st.beta_expander("Author: Clinton Potter"):
        st.markdown("[LinkedIn](https://www.linkedin.com/in/clinton-potter-75487944/)")