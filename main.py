import streamlit as st

st.set_page_config(page_title="GTPR", layout="wide")

nav = st.navigation([home_page, team_creation_page], position="hidden")
nav.run()
