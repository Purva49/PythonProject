import streamlit as st

st.title("Student Grade Calculator")

name = st.text_input("Enter your name")
marks = st.number_input("Enter marks", 0, 100)

if st.button("Calculate"):
    if marks >= 90:
        grade = "A"
    elif marks >= 80:
        grade = "B"
    elif marks >= 70:
        grade = "C"
    elif marks >= 60:
        grade = "D"
    else:
        grade = "F"

    st.success(f"{name}, your grade is {grade}")