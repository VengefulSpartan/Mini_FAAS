import streamlit as st
import requests
import time

st.title("Mini-FaaS Deployment 🚀")
st.write("Write your code, select your language, and watch the cloud do the rest.")
lang_map = {
    "python": "python",
    "c": "c",
    "c++": "cpp",
    "java": "java"
}
# 1. Selection and Input must come BEFORE the button logic
lang_choice = st.selectbox("Select Language", list(lang_map.keys()))
# Update label dynamically based on language
code_input = st.text_area(f"Enter your {lang_choice.upper()} code:", height=200, placeholder="print('Hello World')")

if st.button("Deploy & Execute"):
    if code_input.strip():
        try:
            # 2. Submit both the code AND the language choice
            payload = {
                "code": code_input,
                "language": lang_map[lang_choice]
            }

            response = requests.post("http://127.0.0.1:8000/submit", json=payload)

            if response.status_code == 200:
                data = response.json()
                job_id = data['job_id']
                st.success(f"Code sent to waiting room! Job ID: `{job_id}`")

                with st.spinner(f"Spawning isolated {lang_choice} container and executing..."):
                    max_retries = 30
                    for _ in range(max_retries):
                        status_response = requests.get(f"http://127.0.0.1:8000/status/{job_id}")

                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            current_status = status_data['status']

                            if current_status in ["COMPLETED", "FAILED"]:
                                st.divider()
                                st.subheader("🎉 Execution Results")

                                if status_data['output']:
                                    st.success("Terminal Output:")
                                    # We match the code highlight to the language
                                    st.code(status_data['output'], language=lang_choice)

                                if status_data['error']:
                                    st.error("Execution Error:")
                                    st.code(status_data['error'], language='bash')
                                break

                        time.sleep(1)
                    else:
                        st.warning("Execution is taking a bit long.")

            else:
                st.error(f"Server Error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("🚨 Could not connect to the API. Make sure Uvicorn is running!")
    else:
        st.warning("Please enter some code before submitting.")