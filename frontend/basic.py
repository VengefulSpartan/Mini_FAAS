import streamlit as st
import requests

st.title("Mini-FaaS Deployment 🚀")

# Using text_area so users can write multiple lines of code
code_input = st.text_area("Enter your Python code:", height=200, placeholder="print('Hello World')")

if st.button("Deploy"):
    if code_input.strip():
        try:
            # 1. We send a POST request to YOUR local FastAPI server
            # Notice the JSON structure matches your schemas/job.py exactly
            response = requests.post(
                "http://127.0.0.1:8000/submit",
                json={"code": code_input}
            )

            # 2. Check if the server accepted it
            if response.status_code == 200:
                data = response.json()
                st.success("Code successfully sent to the server!")
                st.info(f"**Job ID:** {data['job_id']}\n\n**Status:** {data['status']}")
            else:
                st.error(f"Server Error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("🚨 Could not connect to the API. Make sure your Uvicorn server is running!")
    else:
        st.warning("Please enter some code before submitting.")