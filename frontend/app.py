import streamlit as st
import requests

API_URL = "http://localhost:8000/research"

st.set_page_config(page_title="AutoResearch Agent", layout="wide")
st.title("AutoResearch Agent")
st.caption("Powered by Claude Haiku 4.5 + Tavily Search")

query = st.text_area("Enter your research query", height=100, placeholder="e.g. What are the latest advancements in quantum computing?")

if st.button("Run Research", type="primary"):
    if not query.strip():
        st.warning("Please enter a research query.")
    else:
        with st.spinner("Researching... this may take a minute."):
            try:
                # 300s timeout — a full pipeline run typically takes 60-120s
                # depending on the topic and how many Tavily calls the researcher makes.
                response = requests.post(API_URL, json={"query": query}, timeout=300)
                response.raise_for_status()
                report = response.json()["report"]
                st.markdown(report)
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Make sure the FastAPI server is running on port 8000.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
