import streamlit as st

st.title("Test Deployment")
st.write("If you see this, Streamlit Cloud is working!")

# Simple input to test
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}!")
