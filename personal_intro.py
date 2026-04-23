import streamlit as st

# Title
st.title(" Personal Introduction App")

st.write("Fill your details below ")

# Inputs
name = st.text_input("What is your name?")
age = st.number_input("How old are you?", min_value=1, step=1)
hobby = st.text_input("What is your favorite hobby?")

# Button
if st.button("Submit"):
    if name and hobby:
        st.success(f" Welcome {name}! ")
        st.write(f"You are {age} years old and love {hobby}.")
    else:
        st.warning("Please fill all fields!")