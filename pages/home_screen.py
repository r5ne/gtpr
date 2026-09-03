import streamlit as st

st.set_page_config(
    page_title="GTPR - Home"
)

st.title("GTPR - Genshin Team Power Ranking")

if st.button("Create a new team"):
    st.switch_page("pages/team_creation.py")
