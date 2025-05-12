import streamlit as st

st.title("Welcome")

name = st.text_input("Enter your name")

if st.button("Submit"):
    st.success(f"Hello, {name}!")
