import streamlit as st

st.title("Message App")
message=st.text_input("ENTER UR MESSAGE:")

if st.button("Submit"):
   st.write("you entered:",message)