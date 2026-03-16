import streamlit as st
import requests

st.title("Knowledge Graph AI")

question = st.text_input("Ask a question about the system")

if st.button("Ask"):

    response = requests.post(
        "http://127.0.0.1:8000/query",
        json={"question": question}
    )

    answer = response.json()

    st.write("Answer:")
    st.write(answer)