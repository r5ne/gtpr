import streamlit as st

home_page = st.Page("pages/home_screen.py")
team_creation_page = st.Page("pages/team_creation.py")

nav = st.navigation([home_page, team_creation_page], position="hidden")
nav.run()
