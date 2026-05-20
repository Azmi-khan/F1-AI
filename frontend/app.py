import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="F1 pitt wall AI", page_icon="🏎️", layout="centered")
st.title("/// RACE STRATEGY AI")
st.markdown("###Pit Wall Telemetry Dashboard")
BACKEND_URL = "http://127.0.0.1:8000"

f1_facts = [
    "📻 Pit Radio: An F1 car can go from 0 to 160 km/h and back to 0 in under 5 seconds.",
    "📻 Pit Radio: F1 steering wheels have over 20 buttons and cost around $50,000.",
    "📻 Pit Radio: Drivers lose up to 3kg of body weight in sweat during a single race.",
    "📻 Pit Radio: An F1 engine idles at around 5,000 RPM—most road cars max out there!",
    "📻 Pit Radio: Brake discs glow red at temperatures exceeding 1,000°C under heavy braking.",
    "📻 Pit Radio: A modern F1 car generates so much downforce it could theoretically drive upside down in a tunnel at 200 km/h."
]
with st.sidebar:
    st.header("Control Panel")
    upload_file = st.file_uploader("Upload Sporting Regulations (PDF)", type="pdf")
    if st.button("initialize Pitt Wall"):
        if upload_file is not None:
            with st.spinner("ingesting rule book..."):
                files = {"file": (upload_file.name, upload_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{BACKEND_URL}/api/upload", files=files)
                    if response.status_code == 200:
                        st.success(response.json().get("message"))
                    else:
                        st.error("Upload failed. Check backend logs.")
                except requests.exceptions.ConnectionError:
                        st.error("Radio failure: Cannot connect to FastAPI backend.")
        else:
            st.warning("No file uploaded.")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "system online. waiting for telemetry..."}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ask the cheif strategist a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    random_fact = random.choice(f1_facts)
    st.toast(random_fact, icon="🏎️")
    with st.chat_message("assistant"):
        with st.spinner("Analyzing parameters..."):
            try:
                response = requests.post(f"{BACKEND_URL}/api/ask", data={"question": prompt})

                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        answer = f" {data['error']}"
                    else:
                        answer = data["response"]
                else:
                    answer = "Radio failure: Backend returned an error."

            except requests.exceptions.ConnectionError:
                answer = "Radio failure: Cannot connect to FastAPI backend."

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

